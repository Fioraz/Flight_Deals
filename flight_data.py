import os
import requests
from data_manager import DataManager


class FlightData:
    def __init__(self):
        self.API_KEY = os.environ["API_KEY"]
        self.location_endpoint = os.environ["LOCATION_ENDPOINT"]
        self.dict = {}
        self.iata_code = {}
        self.data_manager = DataManager()

    def get_iata_codes(self):
        self.dict = self.data_manager.read_cities()
        for x in self.data_manager.dict.keys():
            location_parameters = {
                "term": self.data_manager.dict[x],
                "locale": "en-US",
                "location_types": "airport",
                "limit": 1,
                "active_only": "true"
            }

            location_header = {
                "apikey": self.API_KEY
            }

            response = requests.get(url=self.location_endpoint, params=location_parameters, headers=location_header)
            self.iata_code[x] = response.json()["locations"][0]["city"]["code"]
        return self.iata_code

