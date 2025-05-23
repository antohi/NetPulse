from manuf import manuf
from datetime import datetime

class ScoreDevices:
    def __init__(self):
        self.trusted_vendors = [
            "clevo",
            "dyson",
            "apple"
        ]
        self.parser = manuf.MacParser()
        self.vendor_trust = ""
        self.vendor_name = ""

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
    def get_trust_score(self, mac, all_scanned) -> int:
        trust_score = 0
        if mac.lower() in ["00:00:00:00:00:00", "ff:ff:ff:ff:ff:ff"]:
            trust_score -= 20
        if mac not in all_scanned:
            trust_score -= 10
        trust_score += self.score_vendor_trust()
        trust_score += self.score_connection_time()
        trust_score += self.score_vendor_classifier()
        return trust_score

    # Retrieves the time of the connection and calculates score based on if it was during business hours
    def score_connection_time(self):
        now = datetime.now()
        work_start = now.replace(hour=8, minute=0, second=0, microsecond=0)
        work_end = now.replace(hour=19, minute=0, second=0, microsecond=0)

        if now < work_start or now > work_end:
            return -20
        else:
            return 0

    # Scores the vendor based on if it is trusted or not
    def score_vendor_trust(self):
        if self.vendor_trust == "TRUSTED VENDOR":
            return 30
        elif self.vendor_trust == "UNTRUSTED VENDOR":
            return 20
        elif self.vendor_trust == "UNKNOWN":
            return 15
        else:
            return 0

    # Scores vendor based on classifiers that may be untrustworthy or trustworthy
    def score_vendor_classifier(self):
        if "camera" in self.vendor_name:
            return -15
        elif "laptop" in self.vendor_name or "intel" in self.vendor_name:
            return 10
        else:
            return 0



