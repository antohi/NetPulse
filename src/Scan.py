from scapy.all import *
from scapy.layers.l2 import ARP, Ether, arping
import socket


class Scan:
    def __init__(self):
        self.target_ip = "192.168.0.0/24"
        self.arp = ARP(pdst=self.target_ip)
        self.ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        self.scanned = {}

    def scan(self) -> dict:
        current_scanned = {}
        pckt = self.ether / self.arp
        result = srp(pckt, timeout=1, verbose=0)[0]
        for sent, received in result:
            self.scanned[received.psrc] =  received.hwsrc
            current_scanned[received.psrc] = received.hwsrc
        return current_scanned

    def get_all_results(self):
        for ip, mac in self.scanned.items():
            print(f"{ip}: {mac}")

    def get_current_results(self, current_scanned):
        for ip, mac in current_scanned.items():
            print(f"{ip}: {mac}")



