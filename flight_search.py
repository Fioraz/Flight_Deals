import os
import requests
from flight_data import FlightData
from datetime import datetime, timedelta
from data_manager import DataManager


class FlightSearch:
    def __init__(self):
        self.API_KEY = os.environ["API_KEY"]
        self.SEARCH_ENDPOINT = os.environ["SEARCH_ENDPOINT"]
        self.FLY_FRM = "MAN"
        self.CURRENCY = "GBP"
        self.NIGHTS_FROM = 7
        self.NIGHTS_TO = 28
        self.SEARCH_LIMIT = 1
        self.flight_data = FlightData()
        self.data_manager = DataManager()
        self.data_dict = self.data_manager.read_price()

    def search_flight(self):
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%d/%m/%Y')
        date_to = (datetime.now() + timedelta(days=181)).strftime('%d/%m/%Y')
        iata_codes = [keys for keys in self.data_dict.keys()]
        lowest_prices = [values for values in self.data_dict.values()]
        results = []

        for x in range(len(self.data_dict)):
            header = {
                "apikey": self.API_KEY
            }

            parameters = {
                "fly_from": self.FLY_FRM,
                "fly_to": iata_codes[x],
                "date_from": tomorrow,
                "date_to": date_to,
                "nights_in_dst_from": self.NIGHTS_FROM,
                "nights_in_dst_to": self.NIGHTS_TO,
                "curr": self.CURRENCY,
                "price_to": lowest_prices[x],
                "limit": self.SEARCH_LIMIT
            }

            response = requests.get(url=self.SEARCH_ENDPOINT, headers=header, params=parameters)
            result = response.json()
            if result["data"]:
                results.append(response.json())
        return results
