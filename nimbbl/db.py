import asyncpg
import asyncio

from sqlalchemy.ext.asyncio import create_async_engine ,AsyncSession
from sqlalchemy import URL
# from sqlalchemy import create_engine,URL
from sqlalchemy.orm import sessionmaker,declarative_base
# from models import Base

Base = declarative_base()


url_object = URL.create(
    "postgresql+asyncpg",
    username="manav",
    password="manav2002",  # plain (unescaped) text
    host="localhost",
    port="5432",
    database="nimbbl",
)

engine=create_async_engine(url_object, echo = False)
async_session=sessionmaker(engine,expire_on_commit=False,class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

