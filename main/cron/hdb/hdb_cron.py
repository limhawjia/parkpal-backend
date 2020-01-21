import itertools
from datetime import datetime

import pytz
import requests

from main.database.source import Source

import main.database.carpark_utils as cu

url = 'https://api.data.gov.sg/v1/transport/carpark-availability'


def log_pull():
    singapore_timezone = pytz.timezone('Asia/Singapore')
    current_datetime = datetime.now(singapore_timezone).strftime("%H:%M:%S")
    print("Pulling carpark availability from HDB: " + current_datetime)


def pull():
    response = requests.get(url)

    if not response.content:
        print("Empty response. HDB carpark availability not available.")
        return

    raw_data = response.json()["items"][0]["carpark_data"]

    transformations1 = map(convert_to_data_set, raw_data)
    carpark_data_sets = list(transformations1)

    cu.update_carpark_availability(data_sets=carpark_data_sets)


def convert_to_data_set(raw_data):
    source = Source.HDB
    third_party_id = raw_data["carpark_number"]
    lots_available = raw_data["carpark_info"][0]["lots_available"]

    return source, third_party_id, lots_available


def start():
    log_pull()
    pull()
    print("Pull succeeded.")


start()
