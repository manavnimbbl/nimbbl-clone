import json
from datetime import datetime
from tornado.web import RequestHandler
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from db import async_session
from models import Reader, Book, BorrowRecord


class MainHandler(RequestHandler):
    def get(self):
        self.write("Welcome to the Library Management System")

        
class ReadersHandler(RequestHandler):
    async def get(self):
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(select(Reader))
                readers = result.scalars().all()
                self.write({"readers": [{"id": r.id, "name": r.name, "email": r.email} for r in readers]})
    
    async def post(self):
        data = json.loads(self.request.body)
        new_reader = Reader(id=data['id'],name=data['name'], email=data['email'])
        async with async_session() as session:
            async with session.begin():
                session.add(new_reader)
                await session.commit()
                self.write({"message": "Reader added successfully", "reader": {"id": new_reader.id, "name": new_reader.name, "email": new_reader.email}})
    
    async def put(self, reader_id):
        data = json.loads(self.request.body)
        async with async_session() as session:
            async with session.begin():
                reader = await session.get(Reader, reader_id)
                if reader:
                    reader.name = data['name']
                    reader.email = data['email']
                    await session.commit()
                    self.write({"message": "Reader updated successfully"})
                else:
                    self.set_status(404)
                    self.write({"message": "Reader not found"})
    
    async def delete(self, reader_id):
        async with async_session() as session:
            async with session.begin():
                reader = await session.get(Reader, reader_id)
                if reader:
                    await session.delete(reader)
                    await session.commit()
                    self.write({"message": "Reader deleted successfully"})
                else:
                    self.set_status(404)
                    self.write({"message": "Reader not found"})

class BooksHandler(RequestHandler):
    async def get(self):
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(select(Book))
                books = result.scalars().all()
                self.write({"books": [{"id": b.id, "title": b.title, "author": b.author} for b in books]})
    
    async def post(self):
        data = json.loads(self.request.body)
        new_book = Book(id=data['id'],title=data['title'], author=data['author'])
        async with async_session() as session:
            async with session.begin():
                session.add(new_book)
                await session.commit()
                self.write({"message": "Book added successfully", "book": {"id": new_book.id, "title": new_book.title, "author": new_book.author}})
    
    async def put(self, book_id):
        data = json.loads(self.request.body)
        async with async_session() as session:
            async with session.begin():
                book = await session.get(Book, book_id)
                if book:
                    book.title = data['title']
                    book.author = data['author']
                    await session.commit()
                    self.write({"message": "Book updated successfully"})
                else:
                    self.set_status(404)
                    self.write({"message": "Book not found"})
    
    async def delete(self, book_id):
        async with async_session() as session:
            async with session.begin():
                book = await session.get(Book, book_id)
                if book:
                    await session.delete(book)
                    await session.commit()
                    self.write({"message": "Book deleted successfully"})
                else:
                    self.set_status(404)
                    self.write({"message": "Book not found"})

class BorrowRecordsHandler(RequestHandler):
    async def get(self):
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(select(BorrowRecord))
                borrow_records = result.scalars().all()
                self.write({"borrow_records": [{"id": br.id, "reader_id": br.reader_id, "book_id": br.book_id,
                                                "borrow_date": br.borrow_date.isoformat(), "return_date": br.return_date.isoformat()} for br in borrow_records]})
    
    async def post(self):
        data = json.loads(self.request.body)
        borrow_date = datetime.strptime(data['borrow_date'], '%Y-%m-%d')
        return_date = datetime.strptime(data['return_date'], '%Y-%m-%d')
        new_borrow_record = BorrowRecord(id=data['id'],reader_id=data['reader_id'], book_id=data['book_id'], borrow_date=borrow_date, return_date=return_date)
        async with async_session() as session:
            async with session.begin():
                session.add(new_borrow_record)
                await session.commit()
                self.write({"message": "Borrow record added successfully", "borrow_record": {"id": new_borrow_record.id, "reader_id": new_borrow_record.reader_id, "book_id": new_borrow_record.book_id,
                                                                                             "borrow_date": new_borrow_record.borrow_date.isoformat(), "return_date": new_borrow_record.return_date.isoformat()}})
    
    async def put(self, record_id):
        data = json.loads(self.request.body)
        async with async_session() as session:
            async with session.begin():
                borrow_record = await session.get(BorrowRecord, record_id)
                if borrow_record:
                    borrow_record.borrow_date = datetime.strptime(data['borrow_date'], '%Y-%m-%d')
                    borrow_record.return_date = datetime.strptime(data['return_date'], '%Y-%m-%d')
                    await session.commit()
                    self.write({"message": "Borrow record updated successfully"})
                else:
                    self.set_status(404)
                    self.write({"message": "Borrow record not found"})
    
    async def delete(self, record_id):
        async with async_session() as session:
            async with session.begin():
                borrow_record = await session.get(BorrowRecord, record_id)
                if borrow_record:
                    await session.delete(borrow_record)
                    await session.commit()
                    self.write({"message": "Borrow record deleted successfully"})
                else:
                    self.set_status(404)
                    self.write({"message": "Borrow record not found"})