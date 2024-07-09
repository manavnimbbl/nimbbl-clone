import json
from tornado.web import RequestHandler
from tornado.httpclient import AsyncHTTPClient,HTTPRequest,HTTPError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from db import async_session
import uuid
from schemas.orders_schema import Order
# from authorization import validate_jwt_token
from utilities.merchants.merchant_authorization import validate_jwt_token


class OrderHandler(RequestHandler):
    async def post(self):
        # Creating new order using auth_keys
        auth=self.request.headers
        token=auth["Authorization"]
        token_trim=token[7:]
        print(token_trim)

        decoded_payload = validate_jwt_token(token_trim)
        if decoded_payload:
            print("Decoded Payload:", decoded_payload)
            data = json.loads(self.request.body)
            id=decoded_payload['user_id']
            amt=data['amount']
            cur=data['currency']
            url="https://api.razorpay.com/v1/orders"
            
            payload={
               "amount":amt,
               "currency":cur,
            }

            http_client=AsyncHTTPClient()
            try:
                request=HTTPRequest(url,method="POST",
                                    headers={"Content-Type":"application/json"},
                                    auth_username="rzp_live_sUYZntO7oZRQRj",
                                    auth_password="aGVgV3LcAGQsV4jxx7BtO7GX",
                                    body=json.dumps(payload))
                try:
                    response=await http_client.fetch(request)
                except HTTPError as e:
                    print("response error " , e)

                # self.write(response.body)
                result=json.loads(response.body)
                orderid=str(uuid.uuid4())
                updated_result={
                    "message :":"Order created successfully",
                    "orderid":orderid,
                    "userid":id,
                    "amount":result["amount"],
                    "currency":result["currency"],
                    "status":result["status"],
                    "created at":result["created_at"],
                    "payment_service_provider":"Razorpay"

                }
                self.write(updated_result)
                order_data=json.loads(response.body)
                new_order=Order(user_id=id,amount=amt,currency=cur,orderid=orderid,payment_service_provider="Razorpay",razorpay_orderid=result["id"],status=result["status"])
                async with async_session() as session:
                    async with session.begin():
                        session.add(new_order)
                        await session.commit()
                        # self.write({"message": "Order added successfully"})
                    
            except Exception as e:
                print(e)  