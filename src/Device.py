class Device:
    def __init__(self, ip, mac, info, score, time_detected):
        # Basic identifiers
        self.ip = ip
        self.mac = mac

        # Metadata from the scoring module
        self.vendor = info.get("VENDOR NAME")
        self.vendor_type = info.get("VENDOR TYPE")
        self.vendor_trust = info.get("VENDOR TRUST")
        self.mac_type = info.get("MAC TYPE")
        self.known_device = info.get("KNOWN DEVICE")
        self.device_name = info.get("DEVICE NAME")

        # Scoring & timestamp
        self.trust_score = score
        self.time_detected = time_detected

        # Full info dictionary for reference or export
        self.info = info

    # Returns the full breakdown of how the device was scored.
    def explain_scr(self):
        return self.info

    # Returns a readable, one-line summary of the device.
    def __repr__(self):
        return f"TIME: {self.time_detected.strftime('%H:%M:%S')} | IP: {self.ip} | MAC: {self.mac} | VENDOR: {self.vendor} | KNOWN: {self.known_device} | DEV NAME: {self.device_name} | TS: {self.trust_score}"
