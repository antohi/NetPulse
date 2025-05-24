from datetime import datetime

class Device:
    def __init__(self, ip, mac, vendor, vendor_trust, trust_score, time_detected):
        self.ip = ip
        self.mac = mac
        self.vendor = vendor
        self.vendor_trust = vendor_trust
        self.trust_score = trust_score
        self.time_detected = time_detected

    # Turns info to a dict
    def to_dict(self):
        return {
            "ip": self.ip,
            "mac": self.mac,
            "vendor": self.vendor,
            "vendor_trust": self.vendor_trust,
            "trust_score": self.trust_score,
            "time_detected": self.time_detected.strftime("%H:%M:%S")
        }


    def __repr__(self):
        return f"TIME: {self.time_detected.strftime("%H:%M:%S")} | IP: {self.ip} | MAC: {self.mac} | VENDOR: {self.vendor} | VT: {self.vendor_trust} | TS: {self.trust_score}"
