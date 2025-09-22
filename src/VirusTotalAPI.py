import os
import requests
from dotenv import load_dotenv

class VirusTotalAPI:
    def __init__(self):
        load_dotenv()
        self.headers = {
            "accept": "application/json",
            "x-apikey":os.getenv("API_KEY")
        }
        self.ip = "1.1.1.1"

    def get_url(self):
        url = f"https://www.virustotal.com/api/v3/ip_addresses/{self.ip}"
        response = requests.get(url, headers=self.headers)
        return response.text
