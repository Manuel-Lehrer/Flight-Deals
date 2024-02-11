import os
import requests

SHEETY_ENDPOINT = os.environ["ENV_SHEETY_ENDPOINT"]

MY_TOKEN = os.environ["ENV_SHEETY_TOKEN"]

CUSTOMERS_ENDPOINT = "https://api.sheety.co/05cef1f29d6db624cbd35e9f808553ae/flightDeals/users"

HEADERS = {
            "Authorization": f"Bearer {MY_TOKEN}"
        }


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):

        response = requests.get(url=SHEETY_ENDPOINT, headers=HEADERS)

        data = response.json()

        self.destination_data = data["prices"]

        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(url=f"{SHEETY_ENDPOINT}/{city["id"]}", json=new_data, headers=HEADERS)
            print(response.text)

    def get_emails(self):
        response = requests.get(url=CUSTOMERS_ENDPOINT, headers=HEADERS)

        data = response.json()["users"]
        emails = [rows["email"]for rows in data]
        return emails
