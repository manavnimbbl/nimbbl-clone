from sqlalchemy import  Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base,relationship
from db import Base
# Base =declarative_base()

class RazorpayCredential(Base):
    __tablename__="credentials"
    credid=Column(Integer,primary_key=True, auto_increment=True)
    user_id = Column(Integer, ForeignKey('merchants.userid'))
    keyid=Column(String)
    keysecret=Column(String)
    merchants = relationship('Merchants', back_populates='credentials')