import os
import requests
from main.database import CarPark


def get_coordinate_from_address(data_model):
    address = data_model.address + 'Singapore'
    endpoint = 'https://maps.googleapis.com/maps/api/geocode/json'
    payload = {'address': address, 'key': os.environ['GOOGLE_GEOCODING_API_KEY']}
    results = requests.get(endpoint, params=payload).json()['results']

    if len(results) != 0:
        coordinates = requests.get(endpoint, params=payload).json()['results'][0]['geometry']['location']
        return CarPark(address=data_model.address,
                       source=data_model.source,
                       third_party_id=data_model.third_party_id,
                       longitude=coordinates['lng'], latitude=coordinates['lat'])

    return None