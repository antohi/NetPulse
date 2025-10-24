from datetime import datetime
from VirusTotalAPI import VirusTotalAPI

class Device:
    def __init__(self, ip, mac, info, score, time_detected):
        self.ip = ip
        self.mac = mac
        self.vendor = info.get("VENDOR NAME")
        self.vendor_type = info.get("VENDOR TYPE")
        self.vendor_trust = info.get("VENDOR TRUST")
        self.mac_type = info.get("MAC TYPE")
        self.known_device = info.get("KNOWN DEVICE")
        self.device_name = info.get("DEVICE NAME")

        self.trust_score = score
        self.time_detected = time_detected

        vt = VirusTotalAPI()
        self.vt_score = vt.virus_total_scan(self.ip)

        self.info = info


    def explain_scr(self):
        return self.info

    def __repr__(self):
        return f"TIME: {self.time_detected.strftime('%H:%M:%S')} | IP: {self.ip} | MAC: {self.mac} | VENDOR: {self.vendor} | KNOWN: {self.known_device} | DEV NAME: {self.device_name} | TS: {self.trust_score} "
