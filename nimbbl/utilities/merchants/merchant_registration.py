import bcrypt
from db import async_session
from sqlalchemy.future import select
from schemas.merchant_schema import Merchants

# Encryption Method to convert raw password into Hash
def hash_password(password):
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt() 
    hash = bcrypt.hashpw(bytes, salt).decode('utf-8')
    return hash

# Check if username is existing
async def existing_username(username):
    async with async_session() as session:
        async with session.begin():
            user = await session.execute(select(Merchants).filter(Merchants.username==username))
            res=user.scalar()
            print(res)
            return res
    