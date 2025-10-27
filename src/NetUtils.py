import ipaddress
import netifaces

class NetUtils:

    # Provides helper methods for retrieving subnet and addressing info.
    @staticmethod
    def get_local_subnet() -> str:
        # Determine which interface has the default IPv4 gateway
        iface = netifaces.gateways()['default'][netifaces.AF_INET][1]

        # Retrieve IPv4 address and netmask information for that interface
        addr_info = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]
        ip = addr_info['addr']
        netmask = addr_info['netmask']

        # Convert IP + netmask into a subnet object (e.g. 192.168.1.0/24)
        subnet = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)

        # Return subnet as a string
        return str(subnet)