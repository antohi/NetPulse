from scapy.all import *
from scapy.layers.l2 import ARP, Ether
from ScoreDevices import ScoreDevices
from NetUtils import NetUtils
from Device import Device

class Scan:
    def __init__(self):
        nu = NetUtils()
        self.target_ip = nu.get_local_subnet() # ex. "192.168.1.0/24"
        self.arp = ARP(pdst=self.target_ip) # ARP request targeting all hosts on subnet
        self.ether = Ether(dst="ff:ff:ff:ff:ff:ff")  # Ethernet broadcast (FF:FF:FF:FF:FF:FF)
        self.scanned = {} # Stores scan results keyed by IP
        self.sd = ScoreDevices() # Device scoring engine

    # Uses ARP and ETHER to create and broadcast packet to LAN and retrieve MAC addresses and score
    def scan(self) -> dict:
        current_scanned = {}

        # Combine Ether + ARP into one broadcast packet (Ether/ARP stack)
        pckt = self.ether / self.arp
        # Send broadcast packet and collect responses (timeout=1 sec)
        result = srp(pckt, timeout=1, verbose=0)[0]

        # Iterate through each (sent, received) pair and score the responding device
        for sent, received in result:
            scr = self.sd.score_device(received.hwsrc)
            info = self.sd.explain_score(received.hwsrc)
            dev = Device(received.psrc, received.hwsrc, info, scr, datetime.now())
            current_scanned[received.psrc] = dev

        return current_scanned




