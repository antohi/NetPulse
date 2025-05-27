import Scan
from LiveMonitor import LiveMonitor
from colorama import Fore, Style

s = Scan.Scan()
lm = LiveMonitor(s)

def main_menu():
    print(f"{Fore.LIGHTWHITE_EX}==========")
    print(f"[{Style.RESET_ALL}{Fore.RED}NetPulse{Style.RESET_ALL}{Fore.LIGHTWHITE_EX}]")
    print(f"=========={Style.RESET_ALL}")

    print("[MENU]")
    print("1) Live Monitor")
    print("2) Exit")

    return input("> ")

def start_live_monitor():
    print("===[Live Monitor]===")
    print("Input 'x' at any time to return to main menu")
    lm.start()
    while True:
        user_input = input()
        if user_input.lower() == 'x':
            lm.stop_monitoring()
            print("[+] Stopped Live Monitor.")
            return False

exit = False
while exit == False:
    menu_choice = main_menu()
    if menu_choice == "1":
        if not start_live_monitor():
            continue
    elif menu_choice == "2":
        exit = True
        break
    else:
        "[ERROR] Invalid Menu Choice"



