from sqlalchemy import Column, Integer, Text, Enum, Date, Boolean, ForeignKey, create_engine, Float
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

DB_URI = os.getenv("DB_URI", "postgres://postgres:qwedsazxc123@localhost:5000/carrentaldb")
engine = create_engine(DB_URI)
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)

Base = declarative_base()


class user_table(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    username = Column(Text)
    firstName = Column(Text)
    lastName = Column(Text)
    email = Column(Text)
    password = Column(Text)
    phone = Column(Text)
    accessLevel = Column(Enum('admin', 'passenger', name='User_access'))


class car_table(Base):
    __tablename__ = 'Car'
    name = Column(Text)
    carId = Column(Integer, primary_key=True)
    price = Column(Float)


class order_table(Base):
    __tablename__ = 'Order'
    id = Column(Integer, primary_key=True)
    carId = Column(Integer, ForeignKey(car_table.carId))
    shipDate = Column(Date)
    returnDate = Column(Date)
    userId = Column(Integer, ForeignKey(user_table.id))
    status = Column(Enum('placed', 'approved', 'delivered', name='Order_status'))
    complete = Column(Boolean)
