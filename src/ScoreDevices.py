from manuf import manuf
from datetime import datetime

class ScoreDevices:
    def __init__(self):
        self.trusted_vendors = [ # Known trusted vendors to check vendor against
            "clevo",
            "dyson",
            "apple"
        ]

        # Tables to check MAC information in order to create a score
        self.vendor_trust_table = {
            "TRUSTED VENDOR": 30,
            "UNTRUSTED VENDOR": -30,
            "UNKNOWN": 0
        }

        self.vendor_type_table = {
            "camera": -20,
            "intel": 20,
            "laptop": 20,
            "": 0
        }

        self.mac_type_table = {
            "okay_mac": 20,
            "sketchy_mac": -25

        }

        self.time_table = {
            "off_hours": -20,
            "on_hours": 10
        }

        self.parser = manuf.MacParser() # Manuf name

    # Collects vendor manufacturer info
    def get_vendor(self, mac) -> str:
        vendor_name = self.parser.get_manuf(mac) or "UNKNOWN"
        return vendor_name

    # Checks to see if vendor is in list of trusted vendors
    def check_vendor_trust(self, vendor: str) -> str:
        normalized = vendor.strip().lower()
        if normalized == "unknown":
            vendor_trust = "UNKNOWN"
        elif normalized in self.trusted_vendors:
            vendor_trust = "TRUSTED VENDOR"
        else:
            vendor_trust = "UNTRUSTED VENDOR"
        return vendor_trust

    # Creates a score based on a variety of factors
    def score_device(self, mac) -> int:
        score = 0

        vendor = self.get_vendor(mac)
        ven_trust = self.check_vendor_trust(vendor)
        score += self.vendor_trust_table.get(ven_trust, 0)

        ven_type = self.check_vendor_classifier(vendor)
        score += self.vendor_type_table.get(ven_type, 0)

        mac_type = self.check_mac_type(mac)
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
            return "off_hours"
        else:
            return "on_hours"

    # Scores vendor based on classifiers that may be untrustworthy or trustworthy
    def check_vendor_classifier(self, vendor_name):
        if "camera" in vendor_name:
            return "camera"
        elif "laptop" in vendor_name:
            return "laptop"
        elif "intel" in vendor_name:
            return "intel"
        else:
            return ""

    # Checks for mac spoofing
    def check_mac_type(self, mac):
        if mac.lower() in ["00:00:00:00:00:00", "ff:ff:ff:ff:ff:ff"] or int(mac.split(':')[0], 16) & 2:
            return "sketchy_mac"
        else:
            return "okay_mac"


    def explain_score(self, mac):
        vendor_name = self.get_vendor(mac)
        ven_trust = self.check_vendor_trust(vendor_name)
        vendor_type = self.check_vendor_classifier(vendor_name)
        mac_type = self.check_mac_type(mac)
        cx_time = self.check_connection_time()

        return {
            "VENDOR NAME": vendor_name,
            "VENDOR TYPE": vendor_type,
            "VENDOR TRUST": ven_trust,
            "MAC TYPE": mac_type,
            "CONNECTION TIME": cx_time,
        }


