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

    responses = map(lambda x: to_carpark_response(x, latitude, longitude), queries)
    return jsonify(list(responses))


def query_carparks_within(latitude, longitude, radius, session):
    return session.query(CarPark) \
        .order_by(CarPark.great_circle_distance_from(latitude, longitude)) \
        .filter(CarPark.great_circle_distance_from(latitude, longitude) <= radius) \
        .all()


def to_carpark_response(carpark, curr_latitude, curr_longitude):
    return {'address': carpark.address,
            'price': carpark.price,
            'latitude': carpark.latitude,
            'longitude': carpark.longitude,
            'lots_available': carpark.lots_available,
            'curr_distance': carpark.great_circle_distance_from(curr_latitude, curr_longitude)
            }

