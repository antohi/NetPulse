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

def style_heading(heading):
    return f"{Fore.RED}{heading}{Style.RESET_ALL}"


def main_menu():
    print(f"\n{Fore.LIGHTWHITE_EX}==========")
    print(f"[{Style.RESET_ALL}{Fore.RED}NetPulse{Style.RESET_ALL}{Fore.LIGHTWHITE_EX}]")
    print(f"=========={Style.RESET_ALL}")

    print(f"\n{psob()}{style_heading("MENU")}{pscb()}")
    print(f"{Fore.LIGHTWHITE_EX}1) Live Monitor")
    print(f"2) Exit{Style.RESET_ALL}")

    return input("> ")

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
            return False
        else:
            print(f"\n{Fore.LIGHTRED_EX}[ERROR] Invalid input!{Style.RESET_ALL}")

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



