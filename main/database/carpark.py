from .database import Base
from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.ext.hybrid import hybrid_method
import math


class CarPark(Base):
    __tablename__ = 'carparks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String, nullable=False)
    price = Column(DECIMAL)
    longitude = Column(DECIMAL, nullable=False)
    latitude = Column(DECIMAL, nullable=False)
    lots_available = Column(Integer)

    @hybrid_method
    def distance_from(self, latitude, longitude):
        return math.sqrt(math.fabs(self.latitude - latitude) ** 2 + math.fabs(self.longitude - longitude) ** 2)
