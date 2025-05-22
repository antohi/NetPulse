class ScoreDevices:
    def __init__(self):
        self.trusted_macs = [ # Some sample trusted mac addresses to check against
            "00:1a:2b",  # Cisco
            "f4:5c:89",  # Apple
            "60:83:e7"   # TEST
        ]

    # Scores device based on if mac address appears in trusted mac addresses
    def score_device(self, mac) -> str:
        check_mac = mac.lower()[0:8] # Cuts down mac address and lowers to compare against trusted macs
        if check_mac in self.trusted_macs:
            return "TRUSTED"
        else:
            return "UNKNOWN"



