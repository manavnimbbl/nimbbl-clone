from sqlalchemy import create_engine,URL
from sqlalchemy.orm import sessionmaker
from models import Base

# Base = declarative_base()


url_object = URL.create(
    "postgresql+psycopg2",
    username="manav",
    password="manav2002",  # plain (unescaped) text
    host="localhost",
    port="5432",
    database="db",
)
engine = create_engine(url_object)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session=Session()
