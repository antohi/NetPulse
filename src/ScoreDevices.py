from manuf import manuf
from datetime import datetime

class ScoreDevices:
    def __init__(self, mac):
        self.trusted_vendors = [
            "clevo",
            "dyson",
            "apple"
        ]

        self.vendor_trust_table = {
            "TRUSTED VENDOR": 30,
            "UNTRUSTED VENDOR": -30,
            "UNKNOWN": -10
        }

        self.vendor_type_table = {
            "camera": -20,
            "intel": 10,
            "laptop": 10,
            "": 0
        }

        self.mac_type_table = {
            "okay_mac": 10,
            "sketchy_mac": -25

        }

        self.time_table = {
            "off_hours": -20,
            "on_hours": 10
        }

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
        score = 0

        vendor = self.get_vendor(self.mac)
        ven_trust = self.check_vendor_trust(vendor)
        score += self.vendor_trust_table.get(ven_trust, 0)

        ven_type = self.check_vendor_classifier()
        score += self.vendor_type_table.get(ven_type, 0)

        mac_type = self.check_mac_type()
        score += self.mac_type_table.get(mac_type, 0)

        cx_time = self.check_connection_time()
        score += self.time_table.get(cx_time, 0)

        return score

    # Retrieves the time of the connection and calculates score based on if it was during business hours
    def check_connection_time(self):
        now = datetime.now()
        work_start = now.replace(hour=8, minute=0, second=0, microsecond=0)
        work_end = now.replace(hour=19, minute=0, second=0, microsecond=0)

        if now < work_start or now > work_end:
            return "off-hours"
        else:
            return "on-hours"

    # Scores vendor based on classifiers that may be untrustworthy or trustworthy
    def check_vendor_classifier(self):
        if "camera" in self.vendor_name:
            return "camera"
        elif "laptop" in self.vendor_name:
            return "laptop"
        elif "intel" in self.vendor_name:
            return "intel"
        else:
            return ""

    # Checks for mac spoofing
    def check_mac_type(self):
        if self.mac.lower() in ["00:00:00:00:00:00", "ff:ff:ff:ff:ff:ff"] or int(self.mac.split(':')[0], 16) & 2:
            return "sketchy_mac"
        else:
            return "okay_mac"


