import threading
import time
from datetime import datetime, timedelta
from colorama import Fore, Style

class LiveMonitor:
    def __init__(self, scan_obj, interval=10):
        self.scanner = scan_obj
        self.interval = interval
        self.previous_scan = {}
        self.continue_monitoring = True
        self.thread = None

    # Starts and initializes live monitoring
    def start(self):
        self.continue_monitoring = True
        self.thread = threading.Thread(target=self.monitor)
        self.thread.start()

    def monitor(self):
        while self.continue_monitoring:
            current_scan = self.scanner.scan()
            self.detect_changes(current_scan)
            self.previous_scan = current_scan
            time.sleep(self.interval)

    # Detects changes in the current scan and previous scan
    def detect_changes(self, current_scan):
        print("-"*120)
        for ip, device in current_scan.items():
            if ip not in self.previous_scan:
                print(f"{Fore.LIGHTWHITE_EX}[!] {Fore.RED}[NEW DEVICE]:{Style.RESET_ALL}{Fore.LIGHTWHITE_EX} {device}{Style.RESET_ALL}")
            else:
                prev = self.previous_scan[ip]
                if device.mac != prev.mac:
                    print(f"{Fore.RED}[!!!] [MAC CHANGE]{Style.RESET_ALL}{Fore.LIGHTWHITE_EX} on {ip}: {prev.mac} → {device.mac}{Style.RESET_ALL}")
                elif device.trust_score != prev.trust_score:
                    print(f"{Fore.RED}[!!!] [SCORE CHANGE]{Style.RESET_ALL}{Fore.LIGHTWHITE_EX} {ip} → {prev.trust_score} ➝ {device.trust_score}{Style.RESET_ALL}")
                elif device.trust_score < 0:
                    print(f"{Fore.LIGHTWHITE_EX}[!] [NO CHANGE]{Style.RESET_ALL} {Fore.RED}[LOW SCORE] {Style.RESET_ALL}{Fore.LIGHTWHITE_EX}{device}{Style.RESET_ALL}")
                else:
                    print(f"[-] [No Change] {device}")
            print("-" * 120)

    def stop_monitoring(self):
        self.continue_monitoring = False
        if self.thread:
            self.thread.join()
