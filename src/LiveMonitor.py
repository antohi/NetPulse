import threading
import time
from colorama import Fore, Style
import csv
from DatabaseManager import DatabaseManager as db

class LiveMonitor:
    def __init__(self, scan_obj, interval=10):
        self.scanner = scan_obj
        self.interval = interval
        self.previous_scan = {}
        self.continue_monitoring = True
        self.thread = None
        self.scan_history = []

    # Starts live network monitoring in a background thread
    def start(self):
        self.continue_monitoring = True
        self.thread = threading.Thread(target=self.monitor)
        self.thread.start()

    # Continuously runs network scans until monitoring is stopped.
    def monitor(self):
        while self.continue_monitoring:
            current_scan = self.scanner.scan()

            # Log the entire scan to SQLite
            db.log_scan_to_db(current_scan)

            # Detect & display changes
            self.detect_changes(current_scan)

            # Keep old logic for in-memory history
            self.scan_history.append(current_scan)
            self.previous_scan = current_scan
            time.sleep(self.interval)

    # Compares the current scan to the previous one and prints any differences.
    # Highlights new devices, MAC changes, trust-score updates, or low-trust devices.
    def detect_changes(self, current_scan):
        print("-"*150)
        for ip, device in current_scan.items():
            if not db.device_exists(device.mac) and device.trust_score < 0:
                print(f"{Fore.CYAN}[+] [NEW DEVICE]{Style.RESET_ALL}{Fore.LIGHTYELLOW_EX} [LOW SCORE] {Style.RESET_ALL}{Fore.LIGHTWHITE_EX}{device}{Style.RESET_ALL}")
            elif not db.device_exists(device.mac):
                print(f"{Fore.CYAN}[+] [NEW DEVICE]{Style.RESET_ALL}{Fore.LIGHTWHITE_EX} {device}{Style.RESET_ALL}")
            else:
                prev_score = db.get_prev_dev_score(device.mac)
                if db.is_flagged(device.mac):
                    print(f"{Fore.RED}[!!!] [FLAGGED]{Style.RESET_ALL}{Fore.LIGHTWHITE_EX} {device} {Style.RESET_ALL}")
                elif device.trust_score != prev_score:
                    print(f"{Fore.LIGHTYELLOW_EX}[!] [SCORE CHANGE ({prev_score} ➝ {device.trust_score})]{Style.RESET_ALL}{Fore.LIGHTWHITE_EX} {device} {Style.RESET_ALL}")
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
        try:
            csv_path = "logs/net_log.csv"
            with open(csv_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Time", "IP", "MAC", "Device", "Score"])
                for scan in self.scan_history:
                    for rec in scan.values():
                        writer.writerow([rec.time_detected, rec.ip, rec.mac, rec.vendor, rec.trust_score])
        except Exception as e:
            return f"{Fore.LIGHTRED_EX} unable to write CSV network log: {e}"










