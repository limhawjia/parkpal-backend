from .database import Base
from .source import Source
from sqlalchemy import Column, Integer, String, DECIMAL, Enum


class CarPark(Base):
    __tablename__ = 'carparks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String, nullable=False)
    price = Column(DECIMAL)
    longitude = Column(DECIMAL, nullable=False)
    latitude = Column(DECIMAL, nullable=False)
    lots_available = Column(Integer)
    source = Column(Enum(Source, name="source"), nullable=False, )
    third_party_id = Column(String, nullable=False)


    @hybrid_method
    def distance_from(self, latitude, longitude):
        return math.sqrt(math.fabs(self.latitude - latitude) ** 2 + math.fabs(self.longitude - longitude) ** 2)
