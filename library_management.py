import tornado.ioloop
import tornado.web
from tornado import gen

from sqlalchemy import create_engine, Column, Integer, String ,URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class User(Base):
	__tablename__ = 'readers'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	bookTaken=Column(String)
	bookId=Column(Integer)
	Date=Column(Integer)
	
class Book(Base):
	__tablename__ ='books'
	book_id=Column(Integer,primary_key=True)
	bookName=Column(String)
	isAvailable=Column(String)
	DateofRelease=Column(Integer)
	
url_object = URL.create(
    "postgresql+psycopg2",
    username="manav",
    password="manav2002",  # plain (unescaped) text
    host="localhost",
    port="5432",
    database="mydb",
)
engine = create_engine(url_object)
SessionFactory = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

@gen.coroutine
def query_user_by_book(name):
	session = SessionFactory()

	try:
		result = session.query(Book).filter(Book.bookName == name).first()
		raise gen.Return(result)
	finally:
		session.close()

def allot_book(name):
	session = SessionFactory()
	try:
		session.query(Book).filter_by(bookName=name).update({Book.isAvailable:'False'})
		session.commit()
		# session.query(User).filter_by(id= 2).update({user.name:"Mr."+user.name}) 
	except:
		print("error")
	finally:
		session.close()
		
# async def getBookData():
# 	session = SessionFactory()
# 	try:
# 		result = await session.query(Book).all()
# 		for i in result:
# 			print(i.bookName," ",i.book_id," ",i.isAvailable," ",i.DateofRelease)
# 		print(type(result))
# 		raise gen.Return(result)
# 	finally:
		# session.close()
		



class BookHandler(tornado.web.RequestHandler):
	# async def get(self):
	# 	result = getBookData()
	# 	self.write(result)
	# 	# for i in result:
	# 	# 	self.write(i.bookName," ",i.book_id," ",i.isAvailable," ",i.DateofRelease)
		
	async def get(self, name):	
		book = await query_user_by_book(name)
		if book:
			self.write(f"Book found: {book.bookName}  \n")
			if book.isAvailable=='True':
				self.write(f"Book is also available")
			else:
				self.write("book is not available")
		else:
			self.write("Book not found")
	def put(self,name):
		session = SessionFactory()
		session.add(Book(bookName=name,book_id=13))
		session.commit()
		session.close()
		self.write("Data Inserted")
		


    		
	def delete(self,name):
		session = SessionFactory()
		session.query(Book).filter_by(bookName=name).delete()
		session.commit()
		session.close()
		self.write("Data Deleted")
	
	
	
	
			
class UserHandler(tornado.web.RequestHandler):
	async def post(self,name):
		book = await query_user_by_book(name)
		if book:
			self.write(f"Book found: {book.bookName}  \n")
			if book.isAvailable=='True':
				self.write(f"Book is also available")
				allot_book(name)
				self.write(" Book Alloted")
			else:
				self.write("book is not available")
		else:
			self.write("Book not found")
		
			
def make_app():
	return tornado.web.Application([
		# (r"/book/", BookHandler),
		(r"/book/([^/]+)", BookHandler),
		(r"/user/([^/]+)",UserHandler),
		
	])

if __name__ == "__main__":
	app = make_app()
	app.listen(8888)
	tornado.ioloop.IOLoop.current().start()

	
	
	