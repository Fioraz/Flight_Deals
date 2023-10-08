from data_manager import DataManager
from flight_data import FlightData
from flight_search import FlightSearch
from twilio.rest import Client
import os

data_manager = DataManager()
flight_data = FlightData()
flight_search = FlightSearch()

# Get IATA Codes for the required locations
# iata_code_list = flight_data.get_iata_codes()

# Write IATA Codes to the spreadsheet
# data_manager.write_iata_codes(iata_code_list)

ACCOUNT_SID = os.environ['ACCOUNT_SID']
T_AUTH_TOKEN = os.environ['T_AUTH_TOKEN']
FROM = os.environ['FROM']
TO = os.environ['TO']
message_body = []

client = Client(ACCOUNT_SID, T_AUTH_TOKEN)
results = flight_search.search_flight()
if results[0]["data"]:
    for x in range(len(results)):
        price = results[x]["data"][0]["price"]
        city_from = results[x]["data"][0]["cityCodeFrom"]
        fly_from = results[x]["data"][0]["flyFrom"]
        city_to = results[x]["data"][0]["cityCodeTo"]
        fly_to = results[x]["data"][0]["flyTo"]
        first_departure_date = results[x]["data"][0]["route"][0]["local_departure"].split("T")[0]
        last_departure_date = results[x]["data"][0]["route"][-1]["local_departure"].split("T")[0]
        message_body.append(f"Low price alert! Only £{price} to fly from {city_from}-{fly_from} to {city_to}-{fly_to}, from {first_departure_date} to {last_departure_date}")

    message = "\n\n".join(str(message) for message in message_body)
    client.messages.create(
        body=message,
        from_=FROM,
        to=TO
    )
