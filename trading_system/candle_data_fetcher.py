import requests

class CandleDataFetcher:
    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_candle_data(self, timestamp):
        try:
            response = requests.get(f"{self.api_url}?timestamp={timestamp}")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to fetch data. Status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
