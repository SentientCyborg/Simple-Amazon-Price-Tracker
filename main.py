from bs4 import BeautifulSoup
import requests
import smtplib
import os


def send_email(price: str) -> None:
    """Sends an email"""
    with smtplib.SMTP(host=MY_RELAY, port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=SEND_TO,
                            msg=f"Subject:Buy The Thing!\n\nThe price of the thing is {price}."
                            )


# URL of the item to track--this is for an Instant Pot bundle
URL = "https://www.amazon.com/Instant-Pot-Multi-Use-Programmable-Pressure/dp/B0BNPWHCW1?th=1"

# Get your values from http://myhttpheader.com/
HEADERS = {
    "User-Agent": "YOUR VALUES HERE",
    "Accept-Language": "YOUR VALUES HERE",
}

# Target price
MY_PRICE = 125.0

# -----Your Values Here----- #
MY_EMAIL = os.environ.get("YOUR EMAIL")
PASSWORD = os.environ.get("YOUR PASSWORD")
MY_RELAY = "YOUR EMAIL RELAY"
SEND_TO = "DESTINATION EMAIL ADDRESS"
# --------------------------- #

# Get soup
response = requests.get(URL, headers=HEADERS)
response.raise_for_status()
response_text = response.text
soup = BeautifulSoup(response_text, "html.parser")

# Parse price
price = soup.find(name="span", class_="apexPriceToPay").find(class_="a-offscreen").getText()

# Convert price to float
float_price = float(price.lstrip("$"))

if float_price <= MY_PRICE:
    send_email(price)
