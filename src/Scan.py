from scapy.all import *
from scapy.layers.l2 import ARP, Ether, arping
import socket

from src.ScoreDevices import ScoreDevices
from src.NetUtils import NetUtils
from src.Device import Device

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
            vendor = self.sd.get_vendor(received.hwsrc)
            vendor_trust = self.sd.check_vendor_trust(vendor)
            trust_score = self.sd.get_trust_score(received.hwsrc, self.scanned)
            dev = Device(received.psrc, received.hwsrc, vendor, vendor_trust, trust_score, datetime.now())

            self.scanned[received.psrc] = dev
            current_scanned[received.psrc] = dev
        return current_scanned

    # Gets all results from all scans completed
    def get_all_results(self):
        for ip, dev in self.scanned.items():
            print(f"{dev.ip}: {dev.mac}, VENDOR: {dev.vendor}, VT: {dev.vendor_trust}, SCORE: {dev.trust_score}")

    # Gets the results from only the current scan completed
    def get_current_results(self, current_scanned):
        for ip, dev in current_scanned.items():
            print(f"{dev.ip}: {dev.mac}, VENDOR: {dev.vendor}, VT: {dev.vendor_trust}, SCORE: {dev.trust_score}")






