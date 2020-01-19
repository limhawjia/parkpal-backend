from flask import Flask
from flask import request
from flask import abort
from main.database import Database
from main.database import CarPark
import math
import decimal

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello world!!!'


@app.route('/availability')
def get_availability():
    latitude = request.args.get('latitude', default=None, type=decimal) or abort(400, 'latitude not specified')
    longitude = request.args.get('longitude', default=None, type=decimal) or abort(400, 'longitude not specified')
    radius = request.args.get('radius', defaut=500, type=decimal)
    session = Database().get_session()


def query_carparks_within(x, y, radius_interval, session):
    queries = session.query(CarPark) \
        .order_by(CarPark.distance_from(x, y))
    results = []
    max_radius = radius_interval

    for query in queries:
        yield query

