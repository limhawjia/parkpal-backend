import itertools
import os
from datetime import datetime

import pytz
import requests

from main.database import CarPark
from main.database import Database
from main.database.carpark import Source

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
    transformations1 = map(convert_to_data_model, raw_carparks)
    transformations2 = map(get_coordinate_from_address, transformations1)
    transformations3 = itertools.islice(transformations2, 10)
    carpark_data_models = filter(None, transformations3)

    for carpark in carpark_data_models:
        print(carpark)

    session = Database().get_session()
    session.add_all(carpark_data_models)
    session.commit()


def convert_to_data_model(raw_carpark):
    address = raw_carpark["address"]
    source = Source.HDB
    third_party_id = raw_carpark["carpark_number"]

    return CarPark(address=address, source=source, third_party_id=third_party_id)


def get_coordinate_from_address(data_model):
    address = data_model.address
    print(address)
    endpoint = 'https://maps.googleapis.com/maps/api/geocode/json'
    payload = {'address': address, 'key': os.environ['GOOGLE_GEOCODING_API_KEY']}
    results = requests.get(endpoint, params=payload).json()['results']

    if len(results) != 0:
        coordinates = requests.get(endpoint, params=payload).json()['results'][0]['geometry']['location']
        return CarPark(address=data_model.address, longitude=coordinates['lng'], latitude=coordinates['lat'])

    return None


def start():
    log_pull()
    pull()
