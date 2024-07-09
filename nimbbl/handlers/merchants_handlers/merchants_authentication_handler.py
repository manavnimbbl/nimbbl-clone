import json
import jwt
import uuid
import bcrypt
from datetime import datetime, timedelta
from tornado.web import RequestHandler
# from tornado.httpclient import AsyncHTTPClient,HTTPRequest,HTTPError
from sqlalchemy.future import select
# from sqlalchemy.ext.asyncio import AsyncSession
from db import async_session
from schemas.merchant_schema import Merchants
from schemas.credentials_schema import RazorpayCredential

SECRET_KEY="MANAV"

class AuthHandler(RequestHandler):
    async def post(self):
        data = json.loads(self.request.body)
        print(data)
        
        username=data['username']
        password=data['password']
        if not username or not password:
            self.set_status(300)
            if not username:
                self.write({"Message":"Username is not given"})
            else:
                self.write({"Message":"Password is not given"})

        else:
            async with async_session() as session:
                async with session.begin():
                    user = await session.execute(select(Merchants).filter(Merchants.username==username))
                    merchantsdata = user.scalars().all()
                    print(merchantsdata)

                    # Check to see if username is invalid
                    if len(merchantsdata)==0:
                        self.write("Username is invalid")

                    else:
                        for r in merchantsdata:
                            original_id=r.userid
                            original_username=r.username
                            original_password=r.password

                        userBytes = password.encode('utf-8') 
                        # Check to see if password matches 
                        if bcrypt.checkpw(userBytes, original_password.encode('utf-8')):
                            # self.write("User is validated\n")
                            token = jwt.encode({'user_id': original_id,
                                                'exp' : datetime.now() + timedelta(minutes = 30)
                                                }, SECRET_KEY)
                            print(token)
                            key_id=str(uuid.uuid4())
                            key_secret=jwt.encode({'username': username,'exp': datetime.now() + timedelta(hours=1)},SECRET_KEY,algorithm="HS256")
                            
                            # This is to show how Razorpay take user credentials and give key secret and key id
                            # That is shared with nimbbl for creating order
                            
                            new_cred=RazorpayCredential(keyid=key_id,keysecret=key_secret,user_id=original_id)
                            async with async_session() as session:
                                async with session.begin():
                                    session.add(new_cred)
                                    await session.commit()
                                    self.write({"Message": "User is validate","token :":token})
                            # self.write({"token :":token})
                        

                        else:
                            self.set_status(404)
                            self.write({"Message": "User not found"})