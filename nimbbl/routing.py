import tornado.ioloop
import tornado.web
# from handlers import OrderHandler,EnquiryHandler
from handlers.merchants_handlers.merchants_register_handler import UserHandler
from handlers.merchants_handlers.merchants_authentication_handler import AuthHandler
from handlers.orders_handlers.create_order_handler import OrderHandler
from handlers.orders_handlers.order_enquiry_handlers import EnquiryHandler


def merchant_routing():
    return tornado.web.Application([

        (r"/merchant-data", UserHandler),
        (r"/merchant/register",UserHandler),
        (r"/authenticate-merchant",AuthHandler),
          
    ])

def order_routing():
    return tornado.web.Application([

        (r"/create-order",OrderHandler),
        (r"/orders/([^/]+)", EnquiryHandler),
    
    ])