import json
from tornado.web import RequestHandler
from tornado.httpclient import AsyncHTTPClient,HTTPRequest,HTTPError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.orders_schema import  Order
from db import async_session
from utilities.merchants.merchant_authorization import validate_jwt_token
# from razorpay_order_handler import razorpay_order_fetch

class EnquiryHandler(RequestHandler):
    async def get(self,orderid):
        # Fetch all orders of users
        # async with async_session() as session:
        #             async with session.begin():
        #                  order = await session.execute(select(Order).filter(Order.orderid==orderid))
        #                  order_details=order.scalars().all()
        #                  print(order_details)
        #                  print(order_details[0].payment_service_provider)
        #                  if order_details[0].payment_service_provider=='Razorpay':
        #                        result=await razorpay_order_fetch(orderid)
        #                        self.write(result)
                               

                        
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
                    self.write(updated_result)
                # self.write(response.body)
            except Exception as e:
                print(e)
        
        # Fetch Particular order using orderid
        else:
            auth=self.request.headers
            token=auth["Authorization"]
            token_trim=token[7:]
            print(token_trim)

            decoded_payload = validate_jwt_token(token_trim)
            if decoded_payload:
                async with async_session() as session:
                    async with session.begin():
                        order = await session.execute(select(Order).filter(Order.orderid==orderid))
                        orderdata = order.scalars().all()
                        print(orderdata)
                        for i in orderdata:
                            self.write({
                                "orderid":i.orderid,
                                "amount":i.amount,
                                "currency":i.currency,
                                "payment_service_provider":i.payment_service_provider,
                                "userid":i.user_id,
                                "status":i.status
                            })






            # url=f"https://api.razorpay.com/v1/orders/{orderid}"
            # http_client=AsyncHTTPClient()
            # try:
            #     request=HTTPRequest(url,method="GET",
            #                         headers={"Content-Type":"application/json"},
            #                         auth_username="rzp_live_sUYZntO7oZRQRj",
            #                         auth_password="aGVgV3LcAGQsV4jxx7BtO7GX")
            #     try:
            #         response=await http_client.fetch(request)
            #     except HTTPError as e:
            #         print("response error " , e)

                
            #     # Customized Response
            #     result=json.loads(response.body)
            #     updated_result={
            #         "id":result["id"],
            #         "amount":result["amount"],
            #         "currency":result["currency"],
            #         "status":result["status"],
            #         "created at":result["created_at"]

            #     }
            #     # print(updated_result)  
                
            #     self.write(updated_result)
            #     # self.write(response.body)
            # except Exception as e:
            #     print(e)



     