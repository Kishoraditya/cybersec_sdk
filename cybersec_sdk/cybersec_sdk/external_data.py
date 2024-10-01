# Copyright [2024] [Kishoraditya]
#
# Licensed under the Creative Commons Attribution-NonCommercial 4.0 International License. 
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc/4.0/

# cybersec_sdk/external_data.py

import requests

class ThreatIntelFeed:
    """
    Retrieves threat intelligence data from external sources.
    """

    def __init__(self, feed_url: str):
        self.feed_url = feed_url

    def get_threat_data(self):
        try:
            response = requests.get(self.feed_url)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                return []
        except Exception as e:
            print(f"Error fetching threat data: {e}")
            return []
