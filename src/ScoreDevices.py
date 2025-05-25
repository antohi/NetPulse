from manuf import manuf
from datetime import datetime

class ScoreDevices:
    def __init__(self, mac):
        self.trusted_vendors = [
            "clevo",
            "dyson",
            "apple"
        ]
        self.parser = manuf.MacParser()
        self.vendor_trust = ""
        self.vendor_name = ""
        self.mac = mac

    # Collects vendor manufacturer info
    def get_vendor(self, mac) -> str:
        self.vendor_name = self.parser.get_manuf(mac) or "UNKNOWN"
        return self.vendor_name

    # Checks to see if vendor is in list of trusted vendors
    def check_vendor_trust(self, vendor: str) -> str:
        normalized = vendor.strip().lower()
        if normalized == "unknown":
            self.vendor_trust = "UNKNOWN"
        elif normalized in self.trusted_vendors:
            self.vendor_trust = "TRUSTED VENDOR"
        else:
            self.vendor_trust = "UNTRUSTED VENDOR"
        return self.vendor_trust

    # Creates a score based on a variety of factors
    def score_device(self) -> int:
        trust_score = 0

        trust_score += self.check_locally_administered()
        trust_score += self.check_vendor_trust()
        trust_score += self.check_connection_time()
        trust_score += self.check_vendor_classifier()
        return trust_score

    # Retrieves the time of the connection and calculates score based on if it was during business hours
    def check_connection_time(self):
        now = datetime.now()
        work_start = now.replace(hour=8, minute=0, second=0, microsecond=0)
        work_end = now.replace(hour=19, minute=0, second=0, microsecond=0)

        if now < work_start or now > work_end:
            return -20
        else:
            return 10

    # Scores the vendor based on if it is trusted or not
    def check_vendor_trust(self):
        if self.vendor_trust == "TRUSTED VENDOR":
            return 30
        elif self.vendor_trust == "UNTRUSTED VENDOR":
            return 20
        elif self.vendor_trust == "UNKNOWN":
            return 15
        else:
            return 0

    # Scores vendor based on classifiers that may be untrustworthy or trustworthy
    def check_vendor_classifier(self):
        if "camera" in self.vendor_name:
            return -15
        elif "laptop" in self.vendor_name or "intel" in self.vendor_name:
            return 10
        else:
            return 0

    # Checks if mac locally administered
    def check_locally_administered(self):
        if int(self.mac.split(':')[0], 16) & 2:
            return -30
        else:
            return 30

    # Checks for mac spoofing
    def check_spoofing(self):
        if self.mac.lower() in ["00:00:00:00:00:00", "ff:ff:ff:ff:ff:ff"]:
            return -25
        else:
            return 25


