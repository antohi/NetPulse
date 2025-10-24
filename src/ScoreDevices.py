import json

from manuf import manuf
from datetime import datetime

class ScoreDevices:
    def __init__(self):
        # Loads trusted vendors list
        with open("src/trusted_vendors_config.json", "r") as f:
            trusted_vendors_config = json.load(f)

        self.trusted_vendors = {
            vendor.lower(): trust_level
            for vendor, trust_level in trusted_vendors_config.get("vendors_table", {}).items()
        }

        with open("src/known_devices_config.json", "r") as f:
            known_devices = json.load(f)
        self.known_devices = {
            device.lower(): name
            for device, name in known_devices.get("known_devices", {}).items()
        }

        # Load scoring config from external JSON file
        with open("src/score_config.json", "r") as f:
            score_config = json.load(f)

        self.vendor_trust_table = score_config.get("vendor_trust_table", {})
        self.vendor_type_table = score_config.get("vendor_type_table", {})
        self.mac_type_table = score_config.get("mac_type_table", {})
        self.time_table = score_config.get("time_table", {})
        self.known_device_table = score_config.get("known_device_table", {})

        self.parser = manuf.MacParser()

    # Collects vendor manufacturer info
    def get_vendor(self, mac) -> str:
        vendor_name = self.parser.get_manuf(mac) or "UNKNOWN"
        return vendor_name

    # Checks to see if vendor is in list of trusted vendors
    def check_vendor_trust(self, vendor: str) -> str:
        normalized = vendor.strip().lower()
        if normalized == "unknown":
            return "UNKNOWN"
        return self.trusted_vendors.get(normalized, "UNTRUSTED VENDOR")

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

        known_device, device_name = self.check_known_device(mac)
        score += self.known_device_table.get(known_device, 0)

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

    def check_known_device(self, mac):
        if mac.lower() in self.known_devices:
            return "Y", self.known_devices[mac.lower()] # Y = KNOWN DEVICE
        else:
            return "N", None # N = UNKNOWN DEVICE

    def explain_score(self, mac):
        vendor_name = self.get_vendor(mac)
        ven_trust = self.check_vendor_trust(vendor_name)
        vendor_type = self.check_vendor_classifier(vendor_name)
        mac_type = self.check_mac_type(mac)
        cx_time = self.check_connection_time()
        known_device, device_name = self.check_known_device(mac)

        return {
            "VENDOR NAME": vendor_name,
            "VENDOR TYPE": vendor_type,
            "VENDOR TRUST": ven_trust,
            "MAC TYPE": mac_type,
            "CONNECTION TIME": cx_time,
            "KNOWN DEVICE": known_device,
            "DEVICE NAME": device_name or "N/A"
        }


