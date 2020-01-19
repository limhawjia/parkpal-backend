from .carpark import CarPark
from .source import Source
from .database import Database


def update_carpark_metadata(carpark_data_models):
    session = Database().get_instance().get_session()

    for carpark in carpark_data_models:
        query = session.query(CarPark) \
            .filter(CarPark.source == Source.HDB) \
            .filter(CarPark.third_party_id == carpark.third_party_id) \
            .first()

        if not query:
            session.add(carpark)
            session.commit()
            continue

        query.address = carpark.address
        query.longitude = carpark.longitude
        query.latitude = carpark.latitude
        session.commit()
