import json
from tornado.web import RequestHandler
# from tornado.httpclient import AsyncHTTPClient,HTTPRequest,HTTPError
from sqlalchemy.future import select
# from sqlalchemy.ext.asyncio import AsyncSession
from db import async_session
# from models import Merchants
from schemas.merchant_schema import Merchants
# from resource import hash_password,existing_username
from utilities.merchants.merchant_registration import hash_password,existing_username



class UserHandler(RequestHandler):
    # Fetching all merchants data
    async def get(self):
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(select(Merchants))
                merchantsdata = result.scalars().all()
                for r in merchantsdata:
                    print(r.userid,r.username)
                self.write({"Merchants": [{"id": r.userid, "username": r.username,"email":r.email,"phone number":r.phone,"payment_gateway":r.payments_gateway} for r in merchantsdata]})
    
    # Creating new merchant
    async def post(self):
        data = json.loads(self.request.body)
        print(data)
        password=data['password']
        username=data['username']
        email=data['email']
        phone=data['phone']
        # payment_gateway=data['payment_gateway']
        print(username," ",password)

        #  Check for empty username or password
        if not username or not password:
            self.set_status(300)
            if not username:
                self.write({"Message":"Username is not given"})
            else:
                self.write({"Message":"Password is not given"})

        else:
            check = await existing_username(username)
            print(check)

            # Check if user exists
            if check:
                self.write({"Message":"Username is existing"})

            # Check if password is of minimum length 8
            elif len(password)<8:
                self.write({"Message":"Password is too small"})

            else:
                hash =hash_password(password)
                new_merchant = Merchants(username=username, password=hash,email=email,phone=phone)
                async with async_session() as session:
                    async with session.begin():
                        session.add(new_merchant)
                        await session.commit()
                        self.write({"message": "Merchant registered successfully", "merchant": {"username": new_merchant.username}})