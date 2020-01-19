import itertools
from datetime import datetime

import pytz
import requests

from main.database import CarPark
from main.database.source import Source

import main.database.carpark_utils as cu
import main.geocoding as gc

url = 'https://data.gov.sg/api/action/datastore_search?resource_id=139a3035-e624-4f56-b63f-89ae28d4ae4c'


def log_pull():
    singapore_timezone = pytz.timezone('Asia/Singapore')
    current_datetime = datetime.now(singapore_timezone).strftime("%H:%M:%S")
    print("Pulling carpark metadata from HDB: " + current_datetime)


def pull():
    response = requests.get(url)

    if not response.content:
        print("Empty response. HDB carpark metadata not available.")
        return

    raw_carparks = response.json()["result"]["records"]

    transformations1 = itertools.islice(raw_carparks, 100)
    transformations2 = map(convert_to_data_model, transformations1)
    transformations3 = map(gc.get_coordinate_from_address, transformations2)
    transformations4 = filter(lambda x: x is not None, transformations3)
    carpark_data_models = list(transformations4)

    cu.update_carpark_metadata(carpark_data_models)


def convert_to_data_model(raw_carpark):
    address = raw_carpark["address"]
    source = Source.HDB
    third_party_id = raw_carpark["car_park_no"]

    return CarPark(address=address, source=source, third_party_id=third_party_id)


def start():
    log_pull()
    pull()
    print("Pull succeeded.")
