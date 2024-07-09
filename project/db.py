import asyncpg
import asyncio

from sqlalchemy.ext.asyncio import create_async_engine ,AsyncSession
from sqlalchemy import URL
# from sqlalchemy import create_engine,URL
from sqlalchemy.orm import sessionmaker
from models import Base

# Base = declarative_base()


url_object = URL.create(
    "postgresql+asyncpg",
    username="manav",
    password="manav2002",  # plain (unescaped) text
    host="localhost",
    port="5432",
    database="db",
)

engine=create_async_engine(url_object)
async_session=sessionmaker(engine,expire_on_commit=False,class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)




# engine=create_async_engine(url_object,echo=True)
# async def connect():
#     engine=create_async_engine(url_object,echo=True)
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadate.create_all)
#     return engine

# async def get_async_session(engine):
#     async_session=sessionmaker(engine,class_=AsyncSession)
#     async with async_session() as session:
#         return session


# engine = create_engine(url_object)
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session=Session()
