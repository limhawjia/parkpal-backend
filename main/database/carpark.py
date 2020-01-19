from .database import Base
from sqlalchemy import Column, Integer, String, DECIMAL


class CarPark(Base):
    __tablename__ = 'carparks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String, nullable=False)
    price = Column(DECIMAL)
    longitude = Column(DECIMAL, nullable=False)
    latitude = Column(DECIMAL, nullable=False)
    lots_available = Column(Integer)