# cybersec_sdk/external_data.py

import requests

class ThreatIntelFeed:
    """
    Retrieves threat intelligence data from external sources.
    """

    def __init__(self, feed_url: str):
        self.feed_url = feed_url

    def get_threat_data(self):
        response = requests.get(self.feed_url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return []
