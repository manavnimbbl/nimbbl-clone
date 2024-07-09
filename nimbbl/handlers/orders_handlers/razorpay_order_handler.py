import json
from tornado.web import RequestHandler
from tornado.httpclient import AsyncHTTPClient,HTTPRequest,HTTPError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.orders_schema import  Order
from db import async_session



async def razorpay_order_fetch(orderid):
     # Fetch all orders of users
        async with async_session() as session:
                    async with session.begin():
                         order = await session.execute(select(Order).filter(Order.orderid==orderid))
                         order_details=order.scalars().all()
                         print(order_details)
                        #  print(order_details[0].payment_service_provider)

                        
        if orderid=='all':
            url="https://api.razorpay.com/v1/orders"
            http_client=AsyncHTTPClient()
            try:
                request=HTTPRequest(url,method="GET",
                                    headers={"Content-Type":"application/json"},
                                    auth_username="rzp_live_sUYZntO7oZRQRj",
                                    auth_password="aGVgV3LcAGQsV4jxx7BtO7GX")
                try:
                    response=await http_client.fetch(request)
                except HTTPError as e:
                    print("response error " , e)

                #  Customizing Response
                data=json.loads(response.body)
                for order in data["items"]:
                    updated_result={
                    "id":order["id"],
                    "amount":order["amount"],
                    "currency":order["currency"],
                    "status":order["status"],
                    "created at":order["created_at"]
                    }
                    print(updated_result) 
                    return updated_result 
                #     self.write(updated_result)
                # self.write(response.body)
            except Exception as e:
                print(e)
        
        # Fetch Particular order using orderid
        else:
            url=f"https://api.razorpay.com/v1/orders/{orderid}"
            http_client=AsyncHTTPClient()
            try:
                request=HTTPRequest(url,method="GET",
                                    headers={"Content-Type":"application/json"},
                                    auth_username="rzp_live_sUYZntO7oZRQRj",
                                    auth_password="aGVgV3LcAGQsV4jxx7BtO7GX")
                try:
                    response=await http_client.fetch(request)
                except HTTPError as e:
                    print("response error " , e)

                
                # Customized Response
                result=json.loads(response.body)
                updated_result={
                    "id":result["id"],
                    "amount":result["amount"],
                    "currency":result["currency"],
                    "status":result["status"],
                    "created at":result["created_at"]

                }
                print(updated_result)  
                return updated_result
                # self.write(updated_result)
                # self.write(response.body)
            except Exception as e:
                print(e)