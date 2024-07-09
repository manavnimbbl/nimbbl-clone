import tornado.ioloop
import tornado.web
from tornado import gen
# import sqltor as sqlalchemy_package
from sqlalchemy import create_engine, Column, Integer, String ,URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Define the SQLAlchemy model
Base = declarative_base()

class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	name = Column(String)

# Configure SQLAlchemy
url_object = URL.create(
    "postgresql+psycopg2",
    username="manav",
    password="manav2002",  # plain (unescaped) text
    host="localhost",
    port="5432",
    database="postgres",
)
engine = create_engine(url_object)
SessionFactory = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
# Define asynchronous SQLAlchemy query
@gen.coroutine
def query_user_by_name(name):
	session = SessionFactory()

	try:
		result = session.query(User).filter(User.name == name).first()
		raise gen.Return(result)
	finally:
		session.close()

# Tornado request handler
class UserHandler(tornado.web.RequestHandler):
	async def get(self, name):
		user = await query_user_by_name(name)
		if user:
			self.write(f"User found: {user.name}")
		else:
			self.write("User not found")

def make_app():
	return tornado.web.Application([
		(r"/user/([^/]+)", UserHandler),
	])

if __name__ == "__main__":
	app = make_app()
	app.listen(8888)
	tornado.ioloop.IOLoop.current().start()
