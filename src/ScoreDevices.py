from manuf import manuf
class ScoreDevices:
    def __init__(self):
        self.trusted_vendors = [ # Some sample trusted mac addresses to check against
            "clevo",  # Cisco
            "dyson",  # Apple
            "apple"   # TEST
        ]
        self.parser = manuf.MacParser()

    # Locates vendor through manuf mac parser
    def get_vendor(self, mac) -> str:
        return self.parser.get_manuf(mac) or "UNKNOWN"

    # Gives score based on if vendor is trusted or unknown
    def score_vendor(self, v) -> str:
        vendor = v.strip().lower()
        if vendor == "UNKNOWN":
            return "UNKNOWN"
        elif vendor in self.trusted_vendors:
            return "TRUSTED VENDOR"
        elif vendor not in self.trusted_vendors:
            return "UNTRUSTED VENDOR"



