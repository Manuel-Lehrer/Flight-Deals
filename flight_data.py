import requests
from datetime import datetime, timedelta
import os

KIWI_ENDPOINT = "https://tequila-api.kiwi.com"

KIWI_KEY = os.environ["ENV_KIWI_KEY"]

HEADERS = {
            "apikey": KIWI_KEY
        }


class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self):
        self.price = {}
        self.departure_airport_code = "BKK"
        self.departure_city = "Bangkok"

    def get_price(self, destination):
        location_endpoint = f"{KIWI_ENDPOINT}/search"

        search_params = {
            "fly_from": self.departure_airport_code,
            "fly_to": destination,
            "date_from": (datetime.today() + timedelta(days=1)).strftime("%d/%m/%Y"),
            "date_to": (datetime.today() + timedelta(days=180)).strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "EUR"
        }

        response = requests.get(url=location_endpoint, params=search_params, headers=HEADERS)
        response.raise_for_status()

        try:
            data = response.json()["data"][0]
        except IndexError:
            print("There are no one way flights to this destination")
            # once the documentation is updated for this API you can try to implemetent stopovers
            # search_params["max_stopovers"] = 2
            # response = requests.get(url=location_endpoint, params=search_params, headers=HEADERS)
            # response.raise_for_status()
            # try:
            #     data = response.json()["data"]
            #     print(data)
            #     test = data["price"]
            #     print(test)
            #
            # except TypeError and IndexError:
            #     print(f"There are no flights to {destination}, not even with two stopover")
            #     return None
            # else:
            #     price = data["price"]
            #     origin_city = data["route"][0]["cityFrom"]
            #     destination_city = data["route"][0]["cityTo"]
            #     out_date = data["route"][0]["dTime"]
            #     out_date = datetime.fromtimestamp(out_date).strftime('%Y-%m-%d %H:%M')
            #     airline = data["route"][0]["airline"]
            #     via_city = data["route"][0]["cityTo"]
            #     print(f"{destination}: {price}€, Departure = {out_date}, Carrier = {airline}"
            #           f"There will be one stop over in {via_city}")
            #     flight_data = [price, origin_city, destination_city, out_date, airline, via_city]
            #     return flight_data
        else:
            price = data["price"]
            origin_city = data["route"][0]["cityFrom"]
            destination_city = data["route"][0]["cityTo"]
            out_date = data["route"][0]["dTime"]
            out_date = datetime.fromtimestamp(out_date).strftime('%Y-%m-%d %H:%M')
            airline = data["route"][0]["airline"]

            print(f"{destination}: {price}€, Departure = {out_date}, Carrier = {airline}")

            flight_data = [price, origin_city, destination_city, out_date, airline]

            return flight_data
