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
    print("Pulling carpark availability from LTA: " + current_datetime)


def pull():
    headers = {'AccountKey': access_key}
    response = requests.get(data_url, headers=headers)

    if not response.content:
        print("Empty response. LTA carpark availability not available")
        return

    raw_data = response.json()['value']

    transformations1 = itertools.islice(raw_data, 10)
    transformations2 = map(convert_to_data_set, transformations1)
    carpark_data_sets = list(transformations2)

    cu.update_carpark_availability(carpark_data_sets)


def convert_to_data_set(raw_data):
    source = Source.LTA
    third_party_id = raw_data["CarParkID"]
    lots_available = raw_data["AvailableLots"]

    return source, third_party_id, lots_available


def start():
    log_pull()
    pull()
    print("Pull succeeded.")
