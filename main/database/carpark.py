from .database import Base
from sqlalchemy import Column, Integer, String, DECIMAL, Enum
import enum


class Source(enum.Enum):
    HDB = 1,
    LTA = 2,
    URA = 3


class CarPark(Base):
    __tablename__ = 'carparks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String, nullable=False)
    price = Column(DECIMAL)
    longitude = Column(DECIMAL, nullable=False)
    latitude = Column(DECIMAL, nullable=False)
    lots_available = Column(Integer)
    source = Column(Enum(Source), nullable=False, )
    third_party_id = Column(String, nullable=False)
