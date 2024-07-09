from sqlalchemy import  Column, Integer, String,ARRAY, ForeignKey, Date
from sqlalchemy.orm import declarative_base,relationship
from db import Base
# from schemas.credentials_schema import RazorpayCredential
# from schemas.orders_schema import Order
# from db import Base,engine
# Base =declarative_base()

class Merchants(Base):
    __tablename__ = 'merchants'
    userid = Column(Integer, primary_key=True, auto_increment=True)
    username = Column(String, nullable=False)
    password=Column(String, nullable=False)
    email=Column(String,nullable=False)
    phone=Column(String,nullable=False)
    payments_gateway=Column(ARRAY(String))
    orders = relationship('Order', back_populates='merchants')
    credentials=relationship('RazorpayCredential',uselist=False,back_populates='merchants')