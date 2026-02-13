from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Date, Time
from sqlalchemy.orm import relationship
from database import Base

class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String)
    price = Column(Integer)
    is_veg = Column(Boolean, default=True)
    available = Column(Boolean, default=True)
    description = Column(String, nullable=True)

class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    capacity = Column(Integer)

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)
    guests = Column(Integer)
    date = Column(Date)
    time = Column(Time)
    table_id = Column(Integer, ForeignKey("tables.id"))
    
    table = relationship("Table")
