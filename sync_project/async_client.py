import tornado.ioloop
import tornado.web
from  tornado.httpclient import AsyncHTTPClient
import json

httpClient=AsyncHTTPClient()
class AsyncHttpClientReadersHandler(tornado.web.RequestHandler):
    async def get(self):
        url="http://localhost:8888/readers"
        response=await httpClient.fetch(url)
        data=json.loads(response.body)
        self.write(data)

    # async def post(self,reader_id):
    #     url=f"http://localhost:8887/readers/{reader_id}"
    #     response=await httpClient.fetch(url)
    #     data=json.loads(response.body)
    #     self.write(data)

class AsyncHttpClientBooksHandler(tornado.web.RequestHandler):
    async def get(self):
        url="http://localhost:8888/books"
        response=await httpClient.fetch(url)
        data=json.loads(response.body)
        self.write(data)
    

class AsyncHttpClientBorrowHandler(tornado.web.RequestHandler):
    async def get(self):
        url="http://localhost:8888/borrow_records"
        response=await httpClient.fetch(url)
        data=json.loads(response.body)
        self.write(data)

def make_app():
    return tornado.web.Application([
        (r"/fetchReadersData",AsyncHttpClientReadersHandler),
        # (r"/fetchReadersData/([0-9]+)",AsyncHttpClientReadersHandler),
        (r"/fetchBookData",AsyncHttpClientBooksHandler),
        (r"/fetchBorrowData",AsyncHttpClientBorrowHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()