import itertools
import os
from datetime import datetime

import pytz
import requests

from main.database import CarPark
from main.database.source import Source

import main.database.carpark_utils as cu

access_key = os.environ.get("LTA_API_ACCESS_KEY", None) or exit('LTA_API_ACCESS_KEY not defined.')
data_url = 'http://datamall2.mytransport.sg/ltaodataservice/CarParkAvailabilityv2?'


def log_pull():
    singapore_timezone = pytz.timezone('Asia/Singapore')
    current_datetime = datetime.now(singapore_timezone).strftime("%H:%M:%S")
    print("Pulling carpark metadata from LTA: " + current_datetime)


def pull():
    headers = {'AccountKey': access_key}
    response = requests.get(data_url, headers=headers)

    if not response.content:
        print("Empty response. LTA carpark metadata not available")
        return

    raw_carparks = response.json()['value']

    transformations1 = itertools.islice(raw_carparks, 10)
    transformations2 = map(convert_to_data_model, transformations1)
    carpark_data_models = list(transformations2)

    cu.update_carpark_metadata(carpark_data_models)


def get_lat_long(coordinates):
    lat_long = coordinates.split(' ')
    return lat_long[0], lat_long[1]


def convert_to_data_model(raw_carpark):
    address = raw_carpark["Development"]
    source = Source.LTA
    third_party_id = raw_carpark["CarParkID"]
    latitude, longitude = get_lat_long(raw_carpark['Location'])

    return CarPark(address=address,
                   source=source,
                   third_party_id=third_party_id,
                   longitude=longitude, latitude=latitude)


def start():
    log_pull()
    pull()
    print("Pull succeeded.")
