import requests
import os


KIWI_ENDPOINT = "https://tequila-api.kiwi.com"

KIWI_KEY = os.environ["ENV_KIWI_KEY"]


class FlightSearch:
    def get_destination_code(self, city_name):
        location_endpoint = f"{KIWI_ENDPOINT}/locations/query"
        headers = {
            "apikey": KIWI_KEY
        }

        query = {
            "term": city_name.lower(),
            "location_types": "city",
        }

        response = requests.get(url=location_endpoint, params=query, headers=headers)

        response.raise_for_status()

        results = response.json()["locations"]

        code = results[0]["code"]

        return code
