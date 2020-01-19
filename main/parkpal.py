from flask import Flask
from flask import request
from flask import abort
from main.database import Database
from main.database import CarPark
from decimal import Decimal
import math

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello world!!!'


@app.route('/availability')
def get_availability():
    latitude = request.args.get('latitude', default=None, type=float) or abort(400, 'latitude not specified')
    longitude = request.args.get('longitude', default=None, type=float) or abort(400, 'longitude not specified')
    # radius = request.args.get('radius', default=100.0, type=Decimal)
    # session = Database().get_session()
    # query_carparks_within(latitude, longitude, radius, session)
    f = distance_from(0.0, 0.0, latitude, longitude)
    app.logger.warning(str(f))
    return str(f)


def query_carparks_within(latitude, longitude, radius, session):
    queries = session.query(CarPark) \
        .order_by(CarPark.distance_from(latitude, longitude, app))

    for query in queries:
        app.logger.warning("query is %s", query)


def distance_from(latitude1, longitude1, latitude2, longitude2):
    lat_rad_diff = math.radians(latitude2 - latitude1)
    lon_rad_diff = math.radians(longitude2 - longitude1)
    a = math.sin(lat_rad_diff / 2) ** 2 + \
        math.cos(math.radians(latitude1)) * math.cos(math.radians(latitude2)) * \
        math.sin(lon_rad_diff / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = 6378.137 * c

    return d * 1000  # in meters

