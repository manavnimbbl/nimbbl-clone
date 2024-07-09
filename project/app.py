import tornado.ioloop
import tornado.web
import json
from handlers import MainHandler,ReadersHandler,BooksHandler,BorrowRecordsHandler
from datetime import datetime
from db import init_db


# from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date,URL
# from sqlalchemy.orm import declarative_base
# from sqlalchemy.orm import relationship, sessionmaker

# Base = declarative_base()

# class Reader(Base):
#     __tablename__ = 'readers'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     email = Column(String)
#     borrow_records = relationship('BorrowRecord', back_populates='reader')

# class Book(Base):
#     __tablename__ = 'books'
#     id = Column(Integer, primary_key=True)
#     title = Column(String)
#     author = Column(String)
#     borrow_records = relationship('BorrowRecord', back_populates='book')

# class BorrowRecord(Base):
#     __tablename__ = 'borrow_records'
#     id = Column(Integer, primary_key=True)
#     reader_id = Column(Integer, ForeignKey('readers.id'))
#     book_id = Column(Integer, ForeignKey('books.id'))
#     borrow_date = Column(Date)
#     return_date = Column(Date)
#     reader = relationship('Reader', back_populates='borrow_records')
#     book = relationship('Book', back_populates='borrow_records')

# # Create an engine and a session
# url_object = URL.create(
#     "postgresql+psycopg2",
#     username="manav",
#     password="manav2002",  # plain (unescaped) text
#     host="localhost",
#     port="5432",
#     database="db",
# )
# engine = create_engine(url_object)
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)


# # Create a session
# session = Session()

# class MainHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.write("Welcome to the Library Management System")

# class ReadersHandler(tornado.web.RequestHandler):
#     def get(self):
#         readers = session.query(Reader).all()
#         self.write({"readers": [{"id": r.id, "name": r.name, "email": r.email} for r in readers]})
    
#     def post(self):
#         data = json.loads(self.request.body)
#         new_reader = Reader(id=data['id'],name=data['name'], email=data['email'])
#         session.add(new_reader)
#         session.commit()
#         self.write({"message": "Reader added successfully", "reader": {"id": new_reader.id, "name": new_reader.name, "email": new_reader.email}})
    
#     def put(self, reader_id):
#         data = json.loads(self.request.body)
#         reader = session.query(Reader).get(reader_id)
#         if reader:
#             reader.name = data['name']
#             reader.email = data['email']
#             session.commit()
#             self.write({"message": "Reader updated successfully"})
#         else:
#             self.set_status(404)
#             self.write({"message": "Reader not found"})
    
#     def delete(self, reader_id):
#         reader = session.query(Reader).get(reader_id)
#         if reader:
#             session.delete(reader)
#             session.commit()
#             self.write({"message": "Reader deleted successfully"})
#         else:
#             self.set_status(404)
#             self.write({"message": "Reader not found"})

# class BooksHandler(tornado.web.RequestHandler):
#     def get(self):
#         books = session.query(Book).all()
#         self.write({"books": [{"id": b.id, "title": b.title, "author": b.author} for b in books]})
    
#     def post(self):
#         data = json.loads(self.request.body)
#         new_book = Book(title=data['title'], author=data['author'])
#         session.add(new_book)
#         session.commit()
#         self.write({"message": "Book added successfully", "book": {"id": new_book.id, "title": new_book.title, "author": new_book.author}})
    
#     def put(self, book_id):
#         data = json.loads(self.request.body)
#         book = session.query(Book).get(book_id)
#         if book:
#             book.title = data['title']
#             book.author = data['author']
#             session.commit()
#             self.write({"message": "Book updated successfully"})
#         else:
#             self.set_status(404)
#             self.write({"message": "Book not found"})
    
#     def delete(self, book_id):
#         book = session.query(Book).get(book_id)
#         if book:
#             session.delete(book)
#             session.commit()
#             self.write({"message": "Book deleted successfully"})
#         else:
#             self.set_status(404)
#             self.write({"message": "Book not found"})

# class BorrowRecordsHandler(tornado.web.RequestHandler):
#     def get(self):
#         borrow_records = session.query(BorrowRecord).all()
#         self.write({"borrow_records": [{"id": br.id, "reader_id": br.reader_id, "book_id": br.book_id,
#                                         "borrow_date": br.borrow_date.isoformat(), "return_date": br.return_date.isoformat()} for br in borrow_records]})
    
#     def post(self):
#         data = json.loads(self.request.body)
#         borrow_date = datetime.strptime(data['borrow_date'], '%Y-%m-%d')
#         return_date = datetime.strptime(data['return_date'], '%Y-%m-%d')
#         new_borrow_record = BorrowRecord(reader_id=data['reader_id'], book_id=data['book_id'], borrow_date=borrow_date, return_date=return_date)
#         session.add(new_borrow_record)
#         session.commit()
#         self.write({"message": "Borrow record added successfully", "borrow_record": {"id": new_borrow_record.id, "reader_id": new_borrow_record.reader_id, "book_id": new_borrow_record.book_id,
#                                                                                    "borrow_date": new_borrow_record.borrow_date.isoformat(), "return_date": new_borrow_record.return_date.isoformat()}})
    
#     def put(self, record_id):
#         data = json.loads(self.request.body)
#         borrow_record = session.query(BorrowRecord).get(record_id)
#         if borrow_record:
#             borrow_record.borrow_date = datetime.strptime(data['borrow_date'], '%Y-%m-%d')
#             borrow_record.return_date = datetime.strptime(data['return_date'], '%Y-%m-%d')
#             session.commit()
#             self.write({"message": "Borrow record updated successfully"})
#         else:
#             self.set_status(404)
#             self.write({"message": "Borrow record not found"})
    
#     def delete(self, record_id):
#         borrow_record = session.query(BorrowRecord).get(record_id)
#         if borrow_record:
#             session.delete(borrow_record)
#             session.commit()
#             self.write({"message": "Borrow record deleted successfully"})
#         else:
#             self.set_status(404)
#             self.write({"message": "Borrow record not found"})

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/readers", ReadersHandler),
        (r"/readers/([0-9]+)", ReadersHandler),
        (r"/books", BooksHandler),
        (r"/books/([0-9]+)", BooksHandler),
        (r"/borrow_records", BorrowRecordsHandler),
        (r"/borrow_records/([0-9]+)", BorrowRecordsHandler),
    ])




if __name__ == "__main__":
    tornado.ioloop.IOLoop.current().run_sync(init_db)
    app = make_app()
    app.listen(8887)
    tornado.ioloop.IOLoop.current().start()
    
    