import requests

class ApiFetcher:
    def __init__(self, api_url):
        self.api_url = api_url
    def fetch_nightscout_data(self):
        # Implement your API request logic here
        response = requests.get(self.api_url)
        return response.json()
