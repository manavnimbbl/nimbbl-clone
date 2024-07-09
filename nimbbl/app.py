import tornado.ioloop
import tornado.web
from db import init_db
from routing import merchant_routing,order_routing


if __name__ == "__main__":
    tornado.ioloop.IOLoop.current().run_sync(init_db)
    user_app = merchant_routing()
    order_app=order_routing()
    user_app.listen(8888)
    order_app.listen(8889)
    tornado.ioloop.IOLoop.current().start()