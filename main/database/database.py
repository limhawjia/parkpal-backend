import os
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from main.database import CarPark
from main.database.source import Source

Base = declarative_base()


def get_connection_string():
    db_user = os.environ.get('DB_USER', None) or exit('DB_USER environment variable not defined.')
    db_password = os.environ.get('DB_PASSWORD', None) or exit('DB_PASSWORD environment variable not defined.')
    db_host = os.environ.get('DB_HOST', None) or exit('DB_HOST environment variable not defined.')
    db_port = os.environ.get('DB_PORT', None) or exit('DB_PORT environment variable not defined.')
    db_name = os.environ.get('DB_NAME', None) or exit('DB_NAME environment variable not defined.')
    connection_string = f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    return connection_string


class Database:
    engine = db.create_engine(get_connection_string())
    __instance = None

    @staticmethod
    def get_instance():
        if Database.__instance is None:
            Database()
        return Database.__instance

    def __init__(self):
        if Database.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Base.metadata.create_all(self.engine)
            self.session = sessionmaker(bind=self.engine)
            Database.__instance = self

    def get_session(self):
        return self.session()

    def update_carpark_metadata(self, carpark_data_models):
        session = self.session()

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
