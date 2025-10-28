import ipaddress
import os
import requests
from dotenv import load_dotenv

class VirusTotalAPI:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("API_KEY")
        self.headers = {
            "accept": "application/json",
            "x-apikey": self.api_key
        }

    def get_virus_total_safety_level(self, response: dict) -> str:
        try:
            a = response.get("data", {}).get("attributes", {})
            stats = a.get("last_analysis_stats", {})
            votes = a.get("total_votes", {})
            rep = a.get("reputation", 0)
            malicious = int(stats.get("malicious", 0))
            suspicious = int(stats.get("suspicious", 0))
            positives = malicious + suspicious
            vote_mal = int(votes.get("malicious", 0))
            vote_har = int(votes.get("harmless", 0))

            if positives > 0:
                return "UNSAFE"
            if vote_mal > 20 and vote_mal > vote_har + 10:
                return "UNSAFE"
            if rep < -50:
                return "UNSAFE"
            return "SAFE"

        except (KeyError, AttributeError, ValueError):
            # The JSON wasnt in the expected format
            return "N/A"

    def virus_total_scan(self, ip: str) -> str:

        # Case 1: No API key provided
        if not self.api_key:
            return "N/A"

        if ipaddress.ip_address(ip).is_private:
            return "N/A (private IP)"

        url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
        try:
            response = requests.get(url, headers=self.headers, timeout=8)

            # Invalid API key (401 unauthorized)
            if response.status_code == 401:
                return "N/A"

            # other errors
            response.raise_for_status()
            return self.get_virus_total_safety_level(response.json())

        except requests.exceptions.RequestException:
            return "N/A"
