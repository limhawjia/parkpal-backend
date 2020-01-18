from main.database import Base
from sqlalchemy import Column, Integer, String, DECIMAL


class CarPark(Base):
    __tablename__ = 'carparks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String)
    price = Column(DECIMAL)
    longitude = Column(DECIMAL)
    latitude = Column(DECIMAL)
    lots_available = Column(Integer)
