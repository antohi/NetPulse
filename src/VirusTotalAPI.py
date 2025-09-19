import requests

class VirusTotalAPI:
    def __init__(self):
        self.headers = {
            "accept": "application/json",
            "x-apikey": "APIKEY"
        }
        self.ip = "1.1.1.1"

    def get_url(self):
        url = f"https://www.virustotal.com/api/v3/ip_addresses/{self.ip}"
        response = requests.get(url, headers=self.headers)
        return response.text
