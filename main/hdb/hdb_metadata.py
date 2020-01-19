# Python program to pull, normalize and store carpark data.

# Python program to pull, normalize and store parking data.

import os
import pytz
import requests
import itertools
from datetime import datetime
from main.database import CarPark
from main.database import Database

url = 'https://data.gov.sg/api/action/datastore_search?resource_id=139a3035-e624-4f56-b63f-89ae28d4ae4c'


def main():
    log_cron()
    cron()


def log_cron():
    singapore_timezone = pytz.timezone('Asia/Singapore')
    current_datetime = datetime.now(singapore_timezone).strftime("%H:%M:%S")
    print("Pulling carpark metadata from HDB: " + current_datetime)


def cron():
    print("Pulling HDB carpark metadata...")

    raw_carparks = requests.get(url).json()["result"]["records"]
    transformations = map(convert_to_data_model, raw_carparks)
    carpark_data_models = map(get_coordinate_from_address, transformations)

    session = Database().get_session()
    session.bulk_save_objects(carpark_data_models)
    session.commit()


def convert_to_data_model(raw_carpark):
    address = raw_carpark["address"]
    return CarPark(address=address)


def get_coordinate_from_address(data_model):
    address = data_model.address
    print(address)
    endpoint = 'https://maps.googleapis.com/maps/api/geocode/json'
    payload = {'address': address, 'key': os.environ['GOOGLE_GEOCODING_API_KEY']}
    results = requests.get(endpoint, params=payload).json()['results']

    if len(results) != 0:
        coordinates = requests.get(endpoint, params=payload).json()['results'][0]['geometry']['location']
        return CarPark(address=data_model.address, longitude=coordinates['lng'], latitude=coordinates['lat'])


main()
