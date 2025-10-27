import json
from unicodedata import category

import Scan
from LiveMonitor import LiveMonitor
from colorama import Fore, Style
import requests
from VirusTotalAPI import VirusTotalAPI
from src.ScoreConfigManager import ScoreConfigManager

s = Scan.Scan()
lm = LiveMonitor(s)
vt = VirusTotalAPI()
sc = ScoreConfigManager()

# Place styled opening bracket (for UI headings)
def psob():
    return f"{Fore.LIGHTWHITE_EX}[{Style.RESET_ALL}"

# Place styled closing bracket (for UI headings)
def pscb():
    return f"{Fore.LIGHTWHITE_EX}]{Style.RESET_ALL}"

# Styles title heading using colorama
def style_heading(heading):
    return f"{Fore.RED}{heading}{Style.RESET_ALL}"

# Public IP scoring w/ VT API
def public_ip_score():
    try:
        public_ip = requests.get("https://api.ipify.org").text
        rep = vt.virus_total_scan(public_ip)
        print(f"\nPublic Network IP: {Fore.CYAN}{public_ip}{Style.RESET_ALL} | VirusTotal Score: {Fore.GREEN if 'SAFE' in rep else Fore.RED}{rep}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.YELLOW}[!] Could not fetch public IP: {e}{Style.RESET_ALL}")

# Main menu of program
def main_menu():
    print(f"\n{Fore.LIGHTWHITE_EX}==========")
    print(f"[{Style.RESET_ALL}{Fore.RED}NetPulse{Style.RESET_ALL}{Fore.LIGHTWHITE_EX}]")
    print(f"=========={Style.RESET_ALL}")

    print(f"\n{psob()}{style_heading('MENU')}{pscb()}")
    print(f"{Fore.LIGHTWHITE_EX}1) Live Monitor")
    print(f"2) Scan History")
    print(f"3) Configuration Settings")
    print(f"4) Exit")
    return input("> ")

# Starts live monitoring
def start_live_monitor():
    print(f"\n{Fore.LIGHTWHITE_EX}===[{Style.RESET_ALL}{Fore.BLUE}Live Monitor{Style.RESET_ALL}{Fore.LIGHTWHITE_EX}]==={Style.RESET_ALL}")
    public_ip_score()
    print(f"\n{psob()}{Fore.LIGHTBLUE_EX}Input{Style.RESET_ALL} {Fore.LIGHTWHITE_EX}'x'{Style.RESET_ALL}{Fore.LIGHTBLUE_EX} at any time to return to main menu{Style.RESET_ALL}{pscb()}"
          f"\n{psob()}{Fore.LIGHTBLUE_EX}Input {Fore.LIGHTWHITE_EX}'s'{Style.RESET_ALL}{Fore.LIGHTBLUE_EX} to begin scan{Style.RESET_ALL}{pscb()}")
    while True:
        user_input = input("> ")
        if user_input == "s":
            print(f"\n{Fore.LIGHTGREEN_EX}[SUCCESS] Starting scan...{Style.RESET_ALL}")
            lm.start()
        elif user_input.lower() == 'x':
            print(f"\n{Fore.LIGHTGREEN_EX}[SUCCESS] Exiting...{Style.RESET_ALL}")
            lm.stop_monitoring()
            print(f"\n{Fore.LIGHTWHITE_EX}[+] Stopped Live Monitor.{Style.RESET_ALL}")
            lm.log_results()
            return False
        else:
            print(f"\n{Fore.LIGHTRED_EX}[ERROR] Invalid input!{Style.RESET_ALL}")

# Scan History menu from main menu option
def scan_history_menu():
    print(f"\n{Fore.LIGHTWHITE_EX}===[{Style.RESET_ALL}{Fore.BLUE}Scan History{Style.RESET_ALL}{Fore.LIGHTWHITE_EX}]==={Style.RESET_ALL}")
    print(f"{psob()}{style_heading("MENU")}{pscb()}")
    print(f"{Fore.LIGHTWHITE_EX}1) Show Previous 20 Scans")
    print(f"2) Show All Previous Scans {Style.RESET_ALL}")

    return input("> ")

# Show previous 20 scans option in scan history
def show_previous_20_scans():
    print(f"\n{Fore.LIGHTWHITE_EX}==== Showing Last 20 Scans ===={Style.RESET_ALL}")
    if not lm.scan_history:
        print(f"{Fore.YELLOW}[!] No scan history found.{Style.RESET_ALL}")
        return

    for i, scan in enumerate(lm.scan_history[-20:], 1):
        print(f"\n{Fore.CYAN}-- Scan #{i} --{Style.RESET_ALL}")
        for ip, dev in scan.items():
            print(dev)

# Show all previous  scans option in scan history
def show_all_scans():
    print(f"\n{Fore.LIGHTWHITE_EX}==== Full Scan History ===={Style.RESET_ALL}")
    if not lm.scan_history:
        print(f"{Fore.YELLOW}[!] No scan history found.{Style.RESET_ALL}")
        return

    for i, scan in enumerate(lm.scan_history, 1):
        print(f"\n{Fore.CYAN}-- Scan #{i} --{Style.RESET_ALL}")
        for ip, dev in scan.items():
            print(dev)

# Menu for Configuration Settings
def configuration_settings_menu():
    print(f"\n{Fore.LIGHTWHITE_EX}===[{Style.RESET_ALL}{Fore.BLUE}Configuration Settings{Style.RESET_ALL}{Fore.LIGHTWHITE_EX}]==={Style.RESET_ALL}")
    print(f"{psob()}{style_heading("MENU")}{pscb()}")
    print(f"{Fore.LIGHTWHITE_EX}1) Score Configuration{Style.RESET_ALL}")
    print(f"{Fore.LIGHTWHITE_EX}2) Known Devices Configuration{Style.RESET_ALL}")
    print(f"{Fore.LIGHTWHITE_EX}3) Trusted Vendors Configuration{Style.RESET_ALL}")
    print(f"{Fore.LIGHTWHITE_EX}4) Exit{Style.RESET_ALL}")

    return input("> ")

# Shows current config
def config_settings(config):
    for key, table in config.items():
        print(f"\n{Fore.GREEN}[{key.upper()}]{Style.RESET_ALL}")
        for k, v in table.items():
            print(f"  {Fore.LIGHTWHITE_EX}{k}: {v}{Style.RESET_ALL}")

# Submenu options for Score Configurations settings
def score_config_options():
    print(f"{Fore.LIGHTWHITE_EX}\n1) Edit Configuration")
    print(f"2) Exit{Style.RESET_ALL}")

    return input("> ")

# Edits score config and saves JSON
def edit_score_config(score_config):
    category_selection = input(f"{Fore.LIGHTWHITE_EX}Select Category: ").lower().strip()
    config_selection = input(f"Select Config: ").lower().strip()
    value = input(f"New score value: {Style.RESET_ALL}").lower().strip()
    score_config[category_selection][config_selection] = value
    sc.save_config(sc.score_config_path, score_config)
    print(f"\n{Fore.LIGHTGREEN_EX}[SUCCESS] Score Configuration has been updated{Style.RESET_ALL}")

# Submenu options for Known Devices Configurations settings
def known_dev_config_options():
    print(f"\n{Fore.LIGHTWHITE_EX}1) Add Known Device")
    print("2) Remove Known Device ")
    print(f"3) Exit{Style.RESET_ALL}")
    return input("> ")

# Prompts user for new known device and adds to JSON
def add_known_dev(known_dev_config):
    new_device = input(f"{Fore.LIGHTWHITE_EX}Known Device Mac Address: ").lower().strip()
    value = input(f"Known Device Name (ex. Bob's Macbook): {Style.RESET_ALL}")
    known_dev_config["known_devices"][new_device] = value
    sc.save_config(sc.known_devices_config_path, known_dev_config)
    print(f"\n{Fore.LIGHTGREEN_EX}[SUCCESS] Known Devices Configuration has been updated{Style.RESET_ALL}")

# Prompts user to remove existing known device and removes from JSON
def remove_known_dev(known_dev_config):
    dev_to_remove = input(f"{Fore.LIGHTWHITE_EX}Known Device Mac Address: {Style.RESET_ALL}").lower().strip()
    del known_dev_config["known_devices"][dev_to_remove]
    sc.save_config(sc.known_devices_config_path, known_dev_config)
    print(f"\n{Fore.LIGHTGREEN_EX}[SUCCESS] Known Devices Configuration has been updated{Style.RESET_ALL}")

# Submenu options for Trusted Vendors Configurations settings
def trusted_vendors_config_options():
    print(f"\n{Fore.LIGHTWHITE_EX}1) Add Trusted Vendor")
    print("2) Remove Trusted Vendor")
    print(f"3) Exit{Style.RESET_ALL}")
    return input("> ")

# Prompts user for new trusted vendor and adds to JSON
def add_trusted_vendor(trusted_vendors_config):
    new_vendor = input(f"{Fore.LIGHTWHITE_EX}Vendor Name: {Style.RESET_ALL}").lower().strip()
    trusted_vendors_config["vendors_table"][new_vendor] = "trusted"
    sc.save_config(sc.trusted_vendors_config_path, trusted_vendors_config)
    print(f"\n{Fore.LIGHTGREEN_EX}[SUCCESS] Trusted Vendors Configuration has been updated{Style.RESET_ALL}")

# Prompts user to remove existing trusted vendor and removes from JSON
def remove_trusted_vendor(trusted_vendors_config):
    vendor_to_remove = input(f"{Fore.LIGHTWHITE_EX}Vendor Name: {Style.RESET_ALL}").lower().strip()
    del trusted_vendors_config["vendors_table"][vendor_to_remove]
    sc.save_config(sc.trusted_vendors_config_path, trusted_vendors_config)
    print(f"\n{Fore.LIGHTGREEN_EX}[SUCCESS] Trusted Vendors Configuration has been updated{Style.RESET_ALL}")

# UI
exit = False
while exit == False:
    # Live Monitor
    menu_choice = main_menu()
    if menu_choice == "1":
        if not start_live_monitor():
            continue

    # Scan History
    elif menu_choice == "2":
        submenu_choice = scan_history_menu()
        if submenu_choice == "1":
            show_previous_20_scans()
        elif submenu_choice == "2":
            show_all_scans()
        else:
            continue

    # Configuration Settings
    elif menu_choice == "3":
        submenu_choice = configuration_settings_menu()
        if submenu_choice == "1": # Score Config Options
            score_config = sc.load_json(sc.score_config_path)
            config_settings(score_config)
            submenu_choice = score_config_options()
            if submenu_choice== "1": # Edit Score Config
                edit_score_config(score_config)
            else:
                continue

        elif submenu_choice == "2": # Known Devices Config Options
            known_dev_config = sc.load_json(sc.known_devices_config_path)
            config_settings(known_dev_config)
            submenu_choice = known_dev_config_options()
            if submenu_choice == "1": # Add known vendor
                add_known_dev(known_dev_config)
            elif submenu_choice == "2": # Remove known vendor
                remove_known_dev(known_dev_config)
            elif submenu_choice == "3":
                continue

        elif submenu_choice == "3": # Known Devices Config Options
            trusted_vendors_config = sc.load_json(sc.trusted_vendors_config_path)
            config_settings(trusted_vendors_config)
            submenu_choice = trusted_vendors_config_options()
            if submenu_choice == "1": # Add trusted vendor
                add_trusted_vendor(trusted_vendors_config)
            elif submenu_choice == "2": # Remove trusted vendor
                remove_trusted_vendor(trusted_vendors_config)
            elif submenu_choice == "3":
                continue
        else:
            continue
    # Exit
    elif menu_choice == "4":
        exit = True
        break

    # Invalid menu option
    else:
        print(f"{Fore.RED}Invalid menu option!{Style.RESET_ALL}")





