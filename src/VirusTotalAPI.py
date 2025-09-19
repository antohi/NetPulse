import requests

class VirusTotalAPI:
    def __init__(self):
        self.headers = {"accept": "application/json"}

    def get_url(self,ip ):
        ip = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
        return requests.get(ip, headers=self.headers)
