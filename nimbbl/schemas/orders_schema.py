from sqlalchemy import  Column, Integer, String, ForeignKey,ARRAY, Date
from sqlalchemy.orm import declarative_base,relationship
from schemas.merchant_schema import Merchants
from db import Base
# Base =declarative_base()

class Order(Base):
    __tablename__="orders"
    orderid=Column(String,primary_key=True)
    razorpay_orderid=Column(String ,nullable=False)
    amount=Column(Integer, nullable=False)
    currency=Column(String, nullable=False)
    payment_service_provider=Column(String , nullable=False)
    status=Column(String,nullable=False)
    user_id = Column(Integer, ForeignKey('merchants.userid'))
    merchants = relationship('Merchants', back_populates='orders')