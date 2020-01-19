from .database import Base
from .source import Source
from sqlalchemy import Column, Integer, Float, String, DECIMAL, Enum, func
from sqlalchemy.ext.hybrid import hybrid_method
import math

EARTH_RADIUS = 6378.137  # in km


class CarPark(Base):
    __tablename__ = 'carparks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String, nullable=False)
    price = Column(DECIMAL)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    lots_available = Column(Integer)
    source = Column(Enum(Source, name="source"), nullable=False, )
    third_party_id = Column(String, nullable=False)

    @hybrid_method
    def distance_from(self, latitude, longitude):
        lat_rad_diff = math.radians(latitude - self.latitude)
        lon_rad_diff = math.radians(longitude - self.longitude)
        a = math.sin(lat_rad_diff / 2) ** 2 + \
            math.cos(math.radians(self.latitude)) * math.cos(math.radians(latitude)) * \
            math.sin(lon_rad_diff / 2) ** 2

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = EARTH_RADIUS * c

        return d * 1000  # in meters

    @distance_from.expression
    def distance_from(cls, latitude, longitude, app):
        a = func.power(func.abs(cls.latitude - latitude), 2)
        b = func.power(func.abs(cls.longitude - longitude), 2)
        return func.sqrt(a + b)
