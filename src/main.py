import Scan
from LiveMonitor import LiveMonitor
from colorama import Fore, Style

s = Scan.Scan()
lm = LiveMonitor(s)

# Place styled opening bracket (for UI headings)
def psob():
    return f"{Fore.LIGHTWHITE_EX}[{Style.RESET_ALL}"

# Place styled closing bracket (for UI headings)
def pscb():
    return f"{Fore.LIGHTWHITE_EX}]{Style.RESET_ALL}"

# Styles title heading using colorama
def style_heading(heading):
    return f"{Fore.RED}{heading}{Style.RESET_ALL}"

# Main menu of program
def main_menu():
    print(f"\n{Fore.LIGHTWHITE_EX}==========")
    print(f"[{Style.RESET_ALL}{Fore.RED}NetPulse{Style.RESET_ALL}{Fore.LIGHTWHITE_EX}]")
    print(f"=========={Style.RESET_ALL}")

    print(f"\n{psob()}{style_heading("MENU")}{pscb()}")
    print(f"{Fore.LIGHTWHITE_EX}1) Live Monitor")
    print(f"2) Scan History")
    print(f"3) Exit{Style.RESET_ALL}")

    return input("> ")

# Starts live monitoring
def start_live_monitor():
    print(f"\n{Fore.LIGHTWHITE_EX}===[{Style.RESET_ALL}{Fore.BLUE}Live Monitor{Style.RESET_ALL}{Fore.LIGHTWHITE_EX}]==={Style.RESET_ALL}")
    print(f"{psob()}{Fore.LIGHTBLUE_EX}Input{Style.RESET_ALL} {Fore.LIGHTWHITE_EX}'x'{Style.RESET_ALL}{Fore.LIGHTBLUE_EX} at any time to return to main menu{Style.RESET_ALL}{pscb()}"
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
# UI
exit = False
while exit == False:
    menu_choice = main_menu()
    if menu_choice == "1":
        if not start_live_monitor():
            continue
    elif menu_choice == "2":
        submenu_choice = scan_history_menu()
        if submenu_choice == "1":
            show_previous_20_scans()
        elif submenu_choice == "2":
            show_all_scans()
        else:
            continue
    elif menu_choice == "3":
        exit = True
        break
    else:
        "[ERROR] Invalid Menu Choice"





