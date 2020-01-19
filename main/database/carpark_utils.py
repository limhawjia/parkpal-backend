from .carpark import CarPark
from .source import Source
from .database import Database


def update_carpark_metadata(carpark_data_models):
    session = Database.get_instance().get_session()

    for carpark in carpark_data_models:
        query = session.query(CarPark) \
            .filter(CarPark.source == carpark.source) \
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

    session.close()


def update_carpark_availability(data_sets):
    session = Database.get_instance().get_session()

    for data in data_sets:
        source = data[0]
        third_party_id = data[1]
        lots_available = data[2]

        query = session.query(CarPark) \
            .filter(CarPark.source == source) \
            .filter(CarPark.third_party_id == third_party_id) \
            .first()

        if not query:
            continue

        query.lots_available = lots_available
        session.commit()

    session.close()
