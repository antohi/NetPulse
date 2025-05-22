import ipaddress
import netifaces

class NetUtils:

    @staticmethod
    def get_local_subnet() -> str:
        iface = netifaces.gateways()['default'][netifaces.AF_INET][1]
        addr_info = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]
        ip = addr_info['addr']
        netmask = addr_info['netmask']
        subnet = ipaddress.IPv4Network(f"{ip}/{netmask}", strict=False)
        return str(subnet)