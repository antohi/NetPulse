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

    # Determines safety level of IP address based on parsed API response
    def get_virus_total_safety_level(self, response: dict) -> str:
        a = response.get("data", {}).get("attributes", {})
        stats = a.get("last_analysis_stats", {})
        votes = a.get("total_votes", {})
        tags = set(a.get("tags", []))
        rep = a.get("reputation", 0)

        malicious = int(stats.get("malicious", 0))
        suspicious = int(stats.get("suspicious", 0))
        positives = malicious + suspicious
        harmless = int(stats.get("harmless", 0))
        vote_mal = int(votes.get("malicious", 0))
        vote_har = int(votes.get("harmless", 0))

        # Rules to determine safety based on parsed API response

        # if engines flag it, trust that
        if positives > 0:
            return "UNSAFE"

        # otherwise, consider community votes
        vote_mal = int(votes.get("malicious", 0))
        vote_har = int(votes.get("harmless", 0))

        if vote_mal > 20 and vote_mal > vote_har + 10:
            return "UNSAFE"

        if rep < -50:  # only if reputation is *heavily* negative
            return "UNSAFE"

        # Default: clean
        return "SAFE"

    # Sends API request for specified IP
    def virus_total_scan(self, ip):
        url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
        response = requests.get(url, headers=self.headers)
        return self.get_virus_total_safety_level(response.json())




