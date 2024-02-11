from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
import smtplib


my_email = "myemail"
pw = "mypw"


data_manager = DataManager()
sheet_data = data_manager.get_destination_data()

if sheet_data[0]["iataCode"] == "":
    flight_search = FlightSearch()
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    print(sheet_data)

    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

for destinations in sheet_data:
    flight_data = FlightData()
    flights = flight_data.get_price(destinations["iataCode"])
    if flights is None:
        continue
    price = int(flights[0])
    if price < int(destinations["lowestPrice"]):
        destination = flights[2]
        date = flights[3]
        airline = flights[4]
        emails = data_manager.get_emails()
        for email in emails:
            with (smtplib.SMTP("smtp.gmail.com") as connection):
                connection.starttls()
                connection.login(user=my_email, password=pw)
                if len(flights) > 5:
                    # this will only be applicable once I implement the multiple stopovers after doc update from API
                    via_city = flights[5]
                    message = (f"Low price Alert! Fly to {destination} on the {date} for only {price}€ with {airline}\n"
                               f"There will be two stops over in {via_city}")

                else:
                    message = (f"Low price Alert! Fly to {destination} on the {date} for only {price}EURO "
                               f"with {airline} airline")
                connection.sendmail(from_addr=my_email, to_addrs=email, msg=f"Subject: Low Price Alert!\n\n{message}")
