import itertools
import os
from datetime import datetime

import pytz
import requests

from main.database import CarPark
from main.database.source import Source

import main.database.carpark_utils as cu
import main.geocoding as gc

token_url = 'https://www.ura.gov.sg/uraDataService/insertNewToken.action'
access_key = os.environ["URA_API_ACCESS_KEY"]
data_url = 'https://www.ura.gov.sg/uraDataService/invokeUraDS?service=Car_Park_Details'


def log_pull():
    singapore_timezone = pytz.timezone('Asia/Singapore')
    current_datetime = datetime.now(singapore_timezone).strftime("%H:%M:%S")
    print("Pulling carpark metadata from URA: " + current_datetime)


def get_token():
    headers = {'AccessKey': access_key}
    token = requests.get(token_url, headers=headers).json()['Result']
    return token


def pull():
    access_token = get_token()
    headers = {'AccessKey': access_key, 'Token': access_token}
    response = requests.get(data_url, headers=headers)

    if not response.content:
        print("Empty response. URA carpark metadata not available")
        return

    raw_carparks = response.json()['Result']

    transformations1 = map(convert_to_data_model, raw_carparks)
    transformations2 = itertools.islice(transformations1, 10)
    transformations3 = itertools.groupby(transformations2, lambda x: x.third_party_id)
    transformations4 = map(lambda x: x[1], transformations3)
    transformations5 = map(lambda x: list(x), transformations4)
    transformations6 = map(lambda x: x[0], transformations5)
    transformations7 = map(gc.get_coordinate_from_address, transformations6)
    transformations8 = filter(None, transformations7)
    carpark_data_models = list(transformations8)

    cu.update_carpark_metadata(carpark_data_models)


def convert_to_data_model(raw_carpark):
    address = raw_carpark["ppName"]
    source = Source.URA
    third_party_id = raw_carpark["ppCode"]

    return CarPark(address=address, source=source, third_party_id=third_party_id)


def start():
    log_pull()
    pull()
    print("Pull succeeded.")
