import datetime
import os
import threading
import time
from colorama import Fore, Style
import csv
import sqlite3

class LiveMonitor:
    def __init__(self, scan_obj, interval=10):
        self.scanner = scan_obj
        self.interval = interval
        self.previous_scan = {}
        self.continue_monitoring = True
        self.thread = None
        self.scan_history = []



    # Starts live network monitoring in a background thread
    def start(self):
        self.continue_monitoring = True
        self.thread = threading.Thread(target=self.monitor)
        self.thread.start()

    # Continuously runs network scans until monitoring is stopped.
    def monitor(self):
        while self.continue_monitoring:
            current_scan = self.scanner.scan()

            # Detect & display changes
            self.detect_changes(current_scan)

            # Log the entire scan to SQLite
            self.log_scan_to_db(current_scan)

            # Keep old logic for in-memory history
            self.scan_history.append(current_scan)
            self.previous_scan = current_scan
            time.sleep(self.interval)

    # Compares the current scan to the previous one and prints any differences.
    # Highlights new devices, MAC changes, trust-score updates, or low-trust devices.
    def detect_changes(self, current_scan):
        print("-"*150)
        for ip, device in current_scan.items():
            if not self.device_exists(device.mac) and device.trust_score < 0:
                print(f"{Fore.BLUE}[+] [NEW DEVICE]{Style.RESET_ALL}{Fore.RED} [LOW SCORE] {Style.RESET_ALL}{Fore.LIGHTWHITE_EX}{device}{Style.RESET_ALL}")
            elif not self.device_exists(device.mac):
                print(f"{Fore.BLUE}[+] [NEW DEVICE]{Style.RESET_ALL}{Fore.LIGHTWHITE_EX} {device}{Style.RESET_ALL}")
            else:
                prev_score = self.get_prev_dev_score(device.mac)
                if device.trust_score != prev_score:
                    print(f"{Fore.RED}[!] [SCORE CHANGE ({prev_score} ➝ {device.trust_score})]{Style.RESET_ALL}{Fore.LIGHTWHITE_EX} {device} {Style.RESET_ALL}")
                elif device.trust_score < 0:
                    print(f"{Fore.LIGHTWHITE_EX}[-] [NO CHANGE]{Style.RESET_ALL}{Fore.RED} [LOW SCORE] {Style.RESET_ALL}{Fore.LIGHTWHITE_EX}{device}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.LIGHTWHITE_EX}[-] [No Change] {device}{Style.RESET_ALL}")
            print("-" * 150)

    # Stops the monitoring loop and waits for the thread to exit cleanly.
    def stop_monitoring(self):
        self.continue_monitoring = False
        if self.thread:
            self.thread.join()

    # Saves all scan history to a CSV file for later review.
    # Each row includes timestamp, IP, MAC, vendor, and trust score.
    def log_results(self):
        try:
            csv_path = "logs/net_log.csv"
            with open(csv_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Time", "IP", "MAC", "Device", "Score"])
                for scan in self.scan_history:
                    for rec in scan.values():
                        writer.writerow([rec.time_detected, rec.ip, rec.mac, rec.vendor, rec.trust_score])
        except Exception as e:
            return f"{Fore.LIGHTRED_EX} unable to write CSV network log: {e}"

    def log_scan_to_db(self, scan):
        DB_PATH = "logs/netpulse.db"
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Make sure table exists
        c.execute("""
        CREATE TABLE IF NOT EXISTS device_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_time TEXT,
            ip TEXT,
            mac TEXT,
            vendor TEXT,
            trust_score INTEGER,
            flagged INTEGER
        )
        """)

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for dev in scan.values():
            c.execute("""
            INSERT INTO device_history (scan_time, ip, mac, vendor, trust_score, flagged)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (now, dev.ip, dev.mac, dev.vendor, dev.trust_score, int(getattr(dev, "flagged", False))))

        conn.commit()
        conn.close()

    def device_exists(self, mac):
        conn = sqlite3.connect("logs/netpulse.db")
        c = conn.cursor()
        c.execute("SELECT 1 FROM device_history WHERE mac = ? LIMIT 1;", (mac,))
        exists = c.fetchone() is not None
        conn.close()
        return exists

    def get_prev_dev_score(self, mac):
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






