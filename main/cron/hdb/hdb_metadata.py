import itertools
from datetime import datetime

import pytz
import requests

from main.cron import MetadataQueryLimit
from main.database import CarPark
from main.database.source import Source
from main.tmpc import Svy21Converter

import main.database.carpark_utils as cu

url = 'https://data.gov.sg/api/action/datastore_search?resource_id=139a3035-e624-4f56-b63f-89ae28d4ae4c&limit=4254'


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

    transformations1 = itertools.islice(raw_carparks, MetadataQueryLimit)
    transformations2 = map(convert_to_data_model, transformations1)
    carpark_data_models = list(transformations2)

    cu.update_carpark_metadata(carpark_data_models)


def convert_to_data_model(raw_carpark):
    address = raw_carpark["address"]
    source = Source.HDB
    third_party_id = raw_carpark["car_park_no"]
    northing = float(raw_carpark["y_coord"])
    easting = float(raw_carpark["x_coord"])

    latitude, longitude = Svy21Converter.convert_to_geographic(northing, easting)

    return CarPark(address=address, source=source,
                   third_party_id=third_party_id, latitude=latitude,
                   longitude=longitude)


def start():
    log_pull()
    pull()
    print("Pull succeeded.")
