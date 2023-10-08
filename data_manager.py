import os
import requests


class DataManager:
    def __init__(self):
        self.AUTH_TOKEN = os.environ["AUTH_TOKEN"]
        self.SHEETY_ENDPOINT = os.environ["SHEETY_ENDPOINT"]
        self.dict = {}
        self.flight_data = {}
        self.sheety_headers = {
            "Authorization": self.AUTH_TOKEN
        }

    def read_cities(self):
        response = requests.get(url=self.SHEETY_ENDPOINT, headers=self.sheety_headers)
        results = response.json()["prices"]
        for x in range(len(results)):
            self.dict[results[x]["id"]] = results[x]["city"]
        return self.dict

    def write_iata_codes(self, iata_codes):
        for x in iata_codes.keys():
            sheety_parameters = {
                "price": {
                    "iataCode": iata_codes[x]
                }
            }
            requests.put(url=f"{self.SHEETY_ENDPOINT}/{x}", json=sheety_parameters, headers=self.sheety_headers)

    def read_price(self):
        response = requests.get(url=self.SHEETY_ENDPOINT, headers=self.sheety_headers)
        results = response.json()["prices"]
        for x in range(len(results)):
            self.flight_data[results[x]["iataCode"]] = results[x]["lowestPrice"]
        return self.flight_data
