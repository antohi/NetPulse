import json
import threading
import time
from colorama import Fore, Style
import csv

class LiveMonitor:
    def __init__(self, scan_obj, interval=10):
        self.scanner = scan_obj
        self.interval = interval
        self.previous_scan = {}
        self.continue_monitoring = True
        self.thread = None
        self.scan_history = []
        self.flagged_devices = []

    # Starts live network monitoring in a background thread
    def start(self):
        self.continue_monitoring = True
        self.thread = threading.Thread(target=self.monitor)
        self.thread.start()

    # Continuously runs network scans until monitoring is stopped.
    def monitor(self):
        while self.continue_monitoring:
            current_scan = self.scanner.scan()
            self.detect_changes(current_scan)
            self.scan_history.append(current_scan)
            self.previous_scan = current_scan
            time.sleep(self.interval)

    # Compares the current scan to the previous one and prints any differences.
    # Highlights new devices, MAC changes, trust-score updates, or low-trust devices.
    def detect_changes(self, current_scan):
        print("-"*150)
        for ip, device in current_scan.items():
            if ip not in self.previous_scan and device.trust_score < 0:
                print(f"{Fore.BLUE}[-] [NEW DEVICE]{Style.RESET_ALL}{Fore.LIGHTYELLOW_EX} [LOW SCORE] {Style.RESET_ALL}{Fore.LIGHTWHITE_EX}{device}{Style.RESET_ALL}")
            elif ip not in self.previous_scan:
                print(f"{Fore.BLUE}[-] [NEW DEVICE]{Style.RESET_ALL}{Fore.LIGHTWHITE_EX} {device}{Style.RESET_ALL}")
            else:
                prev = self.previous_scan[ip]
                if device.ip in self.flagged_devices:
                    print(f"{Fore.RED}[!] [FLAGGED]{Style.RESET_ALL}{Fore.LIGHTYELLOW_EX} [LOW SCORE] {Style.RESET_ALL}{Fore.LIGHTWHITE_EX}{device}{Style.RESET_ALL}")
                elif device.mac != prev.mac:
                    print(f"{Fore.LIGHTYELLOW_EX}[!] [MAC CHANGE]{Style.RESET_ALL}{Fore.LIGHTWHITE_EX} on {ip}: {prev.mac} → {device.mac}{Style.RESET_ALL}")
                elif device.trust_score != prev.trust_score:
                    print(f"{Fore.LIGHTYELLOW_EX}[!] [SCORE CHANGE]{Style.RESET_ALL}{Fore.LIGHTWHITE_EX} {ip} → {prev.trust_score} ➝ {device.trust_score}{Style.RESET_ALL}")
                elif device.trust_score < 0:
                    print(f"{Fore.LIGHTWHITE_EX}[-] [NO CHANGE]{Style.RESET_ALL}{Fore.LIGHTYELLOW_EX} [LOW SCORE] {Style.RESET_ALL}{Fore.LIGHTWHITE_EX}{device}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.LIGHTWHITE_EX}[-] [NO CHANGE] {device}{Style.RESET_ALL}")
            print("-" * 150)

    # Stops the monitoring loop and waits for the thread to exit cleanly.
    def stop_monitoring(self):
        self.continue_monitoring = False
        if self.thread:
            self.thread.join()

    # Saves all scan history to a CSV file for later review.
    # Each row includes timestamp, IP, MAC, vendor, and trust score.
    def log_results(self):
        # Build a clean list of all recorded devices across scans
        history_data = []
        for scan in self.scan_history:
            timestamp_batch = []
            for rec in scan.values():
                record = {
                    "time_detected": rec.time_detected.strftime("%Y-%m-%d %H:%M:%S"),
                    "ip": rec.ip,
                    "mac": rec.mac,
                    "vendor": rec.vendor,
                    "trust_score": rec.trust_score,
                    "flagged": rec.flagged if hasattr(rec, "flagged") else False
                }
                timestamp_batch.append(record)
            history_data.append(timestamp_batch)

        filename = "logs/scan_history.json"
        try:
            with open(filename, "w") as json_file:
                json.dump(history_data, json_file, indent=4)
            print(f"{Fore.LIGHTGREEN_EX}[SUCCESS] Scan history written to {filename}{Style.RESET_ALL}")
        except IOError as e:
            print(f"{Fore.LIGHTRED_EX}[ERROR] Unable to write scan history: {e}{Style.RESET_ALL}")

    def flag_device(self, ip):
        self.flagged_devices.append(ip)






