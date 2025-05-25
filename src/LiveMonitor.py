import threading
import time
from datetime import datetime, timedelta

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
        for ip, device in current_scan.items():
            if ip not in self.previous_scan:
                print(f"[!] [NEW DEVICE]: {device}")
            else:
                prev = self.previous_scan[ip]
                if device.mac != prev.mac:
                    print(f"[!!!] [MAC CHANGE] on {ip}: {prev.mac} → {device.mac}")
                if device.trust_score != prev.trust_score:
                    print(f"[!!!] [SCORE CHANGE] {ip} → {prev.trust_score} ➝ {device.trust_score}")
                else:
                    print(f"[-] [No Change] {device}")

    def stop_monitoring(self):
        self.continue_monitoring = False
        if self.thread:
            self.thread.join()
