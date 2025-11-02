import sqlite3

class DatabaseManager:

    # Exports current scan to netpulse.db
    @staticmethod
    def log_scan_to_db(scan):
        import os
        os.makedirs("logs", exist_ok=True)
        DB_PATH = "logs/netpulse.db"
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Ensure table and index
        c.execute("""
        CREATE TABLE IF NOT EXISTS device_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_time TEXT,
            ip TEXT,
            mac TEXT,
            vendor TEXT,
            vendor_type TEXT,
            vendor_trust TEXT,
            mac_type TEXT,
            known_device TEXT,
            device_name TEXT,
            trust_score INTEGER,
            flagged INTEGER
        )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_mac ON device_history(mac);")

        # Checks if mac has been flagged before
        for dev in scan.values():
            # If MAC was ever flagged before, keep it flagged
            c.execute("SELECT 1 FROM device_history WHERE mac = ? AND flagged = 1 LIMIT 1;", (dev.mac,))
            previously_flagged = c.fetchone() is not None

            c.execute("""
            INSERT INTO device_history (scan_time, ip, mac, vendor, vendor_type, vendor_trust, mac_type, known_device, device_name, trust_score, flagged)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                dev.time_detected,
                dev.ip,
                dev.mac,
                dev.vendor,
                dev.vendor_type,
                dev.vendor_trust,
                dev.mac_type,
                dev.known_device,
                dev.device_name,
                dev.trust_score,
                int(previously_flagged or getattr(dev, "flagged", False))
            ))

        conn.commit()
        conn.close()

    # Flags device in DB
    @staticmethod
    def flag_device(mac):
        conn = sqlite3.connect("logs/netpulse.db")
        c = conn.cursor()

        # Find the latest row ID for this MAC
        c.execute("""
            SELECT id FROM device_history
            WHERE mac = ?
            ORDER BY scan_time DESC
            LIMIT 1;
        """, (mac,))
        row = c.fetchone()

        if row:
            row_id = row[0]
            c.execute("""
                UPDATE device_history
                SET flagged = 1
                WHERE id = ?;
            """, (row_id,))
            conn.commit()
        else:
            print(f"[DB] No device found for MAC {mac}.")

        conn.close()

    # Checks whether this is a new device or if it has been scanned before
    @staticmethod
    def device_exists(mac):
        conn = sqlite3.connect("logs/netpulse.db")
        c = conn.cursor()
        c.execute("SELECT 1 FROM device_history WHERE mac = ? LIMIT 1;", (mac,))
        exists = c.fetchone() is not None
        conn.close()
        return exists

    # Retrieves previous device score
    @staticmethod
    def get_prev_dev_score(mac):
        conn = sqlite3.connect("logs/netpulse.db")
        c = conn.cursor()
        c.execute("""
            SELECT trust_score
            FROM device_history
            WHERE mac = ?
            ORDER BY scan_time DESC
            LIMIT 1;
        """, (mac,))
        row = c.fetchone()
        conn.close()
        return row[0] if row else None

    # Prints all flagged devices
    @staticmethod
    def get_all_flagged_devices():
        conn = sqlite3.connect("logs/netpulse.db")
        c = conn.cursor()
        c.execute("""
            SELECT scan_time, ip, mac, vendor, vendor_type, vendor_trust, mac_type, known_device, device_name, trust_score
            FROM device_history
            WHERE flagged = 1
            ORDER BY scan_time DESC;
        """)
        rows = c.fetchall()
        conn.close()
        return rows

    # Checks whether perviously scanned device has already been flagged
    @staticmethod
    def is_flagged(mac) -> bool:
        conn = sqlite3.connect("logs/netpulse.db")
        c = conn.cursor()
        c.execute("""
        SELECT flagged
        FROM device_history
        WHERE mac = ?
        ORDER BY scan_time DESC
        LIMIT 1;
        """,(mac,))

        row = c.fetchone()
        conn.close()

        if row is None:  # no record found
            return False
        return row[0] == 1
