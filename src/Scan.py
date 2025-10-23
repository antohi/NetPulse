from scapy.all import *
from scapy.layers.l2 import ARP, Ether
from ScoreDevices import ScoreDevices
from NetUtils import NetUtils
from Device import Device

class Scan:
    def __init__(self):
        nu = NetUtils()
        self.target_ip = nu.get_local_subnet()
        self.arp = ARP(pdst=self.target_ip)
        self.ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        self.scanned = {}
        self.sd = ScoreDevices()

    # Uses ARP and ETHER to create and broadcast packet to LAN and retrieve MAC addresses and score
    def scan(self) -> dict:
        current_scanned = {}
        pckt = self.ether / self.arp # Sets up packet to be sent out
        result = srp(pckt, timeout=1, verbose=0)[0]
        for sent, received in result:
            scr = self.sd.score_device(received.hwsrc)
            info = self.sd.explain_score(received.hwsrc)
            device_trust = self.sd.check_device_trust(received.hwsrc)
            dev = Device(received.psrc, received.hwsrc, info, scr, datetime.now(), device_trust)
            current_scanned[received.psrc] = dev

        return current_scanned




