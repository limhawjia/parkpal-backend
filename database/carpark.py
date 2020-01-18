from database.database import Base
from sqlalchemy import Column, Integer, String, DECIMAL


class CarPark(Base):
    __tablename__ = 'carparks'
    id = Column(Integer, primary_key=True)
    address = Column(String)
    x_coordinate = Column(DECIMAL)
    y_coordinate = Column(DECIMAL)
    lots_available = Column(Integer)
