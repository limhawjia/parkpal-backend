from flask import Flask
from flask import request
from flask import abort
from main.database import Database
from main.database import CarPark
import decimal

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello world!!!'
#
#
# @app.route('/availability')
# def get_availability():
#     latitude = request.args.get('latitude', default=None, type=decimal) or abort(400, 'latitude not specified')
#     longitude = request.args.get('longitude', default=None, type=decimal) or abort(400, 'longitude not specified')
#     radius = request.args.get('radius', defaut=100.0, type=decimal)
#     session = Database().get_session()
#     query_carparks_within(latitude, longitude)
#
#
# def query_carparks_within(latitude, longitude, radius, session):
#     queries = session.query(CarPark) \
#         .order_by(CarPark.distance_from(latitude, longitude))
#
#     for query in queries:
#         print(query)
