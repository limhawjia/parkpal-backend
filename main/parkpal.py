from flask import Flask, request, abort, jsonify
from main.database import Database
from main.database import CarPark

app = Flask(__name__)
db = Database()


@app.route('/')
def hello():
    return 'Hello world!!!'


@app.route('/availability')
def get_availability():
    latitude = request.args.get('latitude', default=None, type=float) or abort(400, 'latitude not specified')
    longitude = request.args.get('longitude', default=None, type=float) or abort(400, 'longitude not specified')
    radius = request.args.get('radius', default=500.0, type=float)
    session = db.get_session()
    queries = query_carparks_within(latitude, longitude, radius, session)
    session.close()

    responses = map(to_carpark_response, queries)
    return jsonify(responses)


def query_carparks_within(latitude, longitude, radius, session):
    return session.query(CarPark) \
        .order_by(CarPark.great_circle_distance_from(latitude, longitude)) \
        .filter(CarPark.great_circle_distance_from(latitude, longitude) <= radius) \
        .all()


def to_carpark_response(carpark, curr_latitude, curr_longitude):
    return CarParkResponse(carpark.address, carpark.price, carpark.latitude, carpark.longitude, carpark.lots_available,
                           carpark.great_circle_distance_from(curr_latitude, curr_longitude))


class CarParkResponse:
    def __init__(self, address, price, latitude, longitude, lots_available, curr_distance):
        self.address = address
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.lots_available = lots_available
        self.curr_distance = curr_distance
