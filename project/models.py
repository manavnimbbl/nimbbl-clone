from sqlalchemy import  Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base,relationship

# from db import Base,engine
Base =declarative_base()
class Reader(Base):
    __tablename__ = 'readers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    borrow_records = relationship('BorrowRecord', back_populates='reader')

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    borrow_records = relationship('BorrowRecord', back_populates='book')

class BorrowRecord(Base):
    __tablename__ = 'borrow_records'
    id = Column(Integer, primary_key=True)
    reader_id = Column(Integer, ForeignKey('readers.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    borrow_date = Column(Date)
    return_date = Column(Date)
    reader = relationship('Reader', back_populates='borrow_records')
    book = relationship('Book', back_populates='borrow_records')