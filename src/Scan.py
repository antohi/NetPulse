from scapy.all import *
from scapy.layers.l2 import ARP, Ether, arping
import socket


class Scan:
    def __init__(self):
        self.target_ip = "192.168.0.0/24"
        self.arp = ARP(pdst=self.target_ip)
        self.ether = Ether(dst="ff:ff:ff:ff:ff:ff")

    def scan(self):
        pckt = self.ether / self.arp
        result = srp(pckt, timeout=1, verbose=0)[0]
        print(f"SCAN")
        for sent, received in result:
            print(received.psrc, received.hwsrc)

