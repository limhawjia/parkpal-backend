import itertools
import os
from datetime import datetime

import pytz
import requests

from main.cron import MetadataQueryLimit
from main.database import CarPark
from main.database.source import Source

import main.database.carpark_utils as cu

token_url = 'https://www.ura.gov.sg/uraDataService/insertNewToken.action'
access_key = os.environ.get("URA_API_ACCESS_KEY", None) or exit('URA_API_ACCESS_KEY not defined.')
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

    transformations1 = itertools.islice(raw_carparks, MetadataQueryLimit)
    transformations2 = filter(lambda x: x['vehCat'] == 'Car', transformations1)
    transformations3 = map(convert_to_data_model, transformations2)
    carpark_data_models = list(transformations3)

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
