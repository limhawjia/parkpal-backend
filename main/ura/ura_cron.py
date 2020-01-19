import itertools
import os
from datetime import datetime

import pytz
import requests

from main.database.source import Source

import main.database.carpark_utils as cu

token_url = 'https://www.ura.gov.sg/uraDataService/insertNewToken.action'
access_key = os.environ.get("URA_API_ACCESS_KEY", None) or exit('URA_API_ACCESS_KEY not defined.')
data_url = 'https://www.ura.gov.sg/uraDataService/invokeUraDS?service=Car_Park_Availability'


def log_pull():
    singapore_timezone = pytz.timezone('Asia/Singapore')
    current_datetime = datetime.now(singapore_timezone).strftime("%H:%M:%S")
    print("Pulling carpark availability from URA: " + current_datetime)


def get_token():
    headers = {'AccessKey': access_key}
    token = requests.get(token_url, headers=headers).json()['Result']
    return token


def pull():
    access_token = get_token()
    headers = {'AccessKey': access_key, 'Token': access_token}
    response = requests.get(data_url, headers=headers)

    if not response.content:
        print("Empty response. URA carpark availability not available")
        return

    raw_data = response.json()['Result']

    transformations1 = itertools.islice(raw_data, 100)
    transformations2 = filter(lambda x: x["lotType"] == 'C', transformations1)
    transformations3 = map(convert_to_data_set, transformations2)
    carpark_data_sets = list(transformations3)

    cu.update_carpark_availability(carpark_data_sets)


def convert_to_data_set(raw_data):
    source = Source.URA
    third_party_id = raw_data["carparkNo"]
    lots_available = int(raw_data["lotsAvailable"])

    return source, third_party_id, lots_available


def start():
    log_pull()
    pull()
    print("Pull succeeded.")


start()
