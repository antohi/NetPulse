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

    def get_vendor(self, mac) -> str:
        return self.parser.get_manuf(mac) or "UNKNOWN"

    def score_vendor(self, vendor: str) -> str:
        normalized = vendor.strip().lower()
        if normalized == "unknown":
            self.vendor_trust = "UNKNOWN"
        elif normalized in self.trusted_vendors:
            self.vendor_trust = "TRUSTED VENDOR"
        else:
            self.vendor_trust = "UNTRUSTED VENDOR"
        return self.vendor_trust

    def get_trust_score(self, mac, all_scanned) -> int:
        trust_score = 0
        now = datetime.now()
        work_start = now.replace(hour=8, minute=0, second=0, microsecond=0)
        work_end = now.replace(hour=19, minute=0, second=0, microsecond=0)

        if self.vendor_trust == "TRUSTED VENDOR":
            trust_score += 30
        elif self.vendor_trust == "UNTRUSTED VENDOR":
            trust_score -= 20
        elif self.vendor_trust == "UNKNOWN":
            trust_score -= 15

        if mac.lower() in ["00:00:00:00:00:00", "ff:ff:ff:ff:ff:ff"]:
            trust_score -= 20

        if mac not in all_scanned:
            trust_score -= 10

        if now < work_start or now > work_end:
            trust_score -= 20

        return trust_score
