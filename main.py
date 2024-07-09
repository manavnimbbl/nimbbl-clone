# import asyncio

# async def fn():
# 	print('This is ')
# 	await asyncio.sleep(1)
# 	print('asynchronous programming')
# 	await asyncio.sleep(1)
# 	print('and not multi-threading')

# asyncio.run(fn())
# import asyncio

# async def fn():
	
# 	print("one")
# 	await asyncio.sleep(1)
# 	await fn2()
# 	print('four')
# 	await asyncio.sleep(1)
# 	print('five')
# 	await asyncio.sleep(1)

# async def fn2():
# 	await asyncio.sleep(1)
# 	print("two")
# 	await asyncio.sleep(1)
# 	print("three")
# asyncio.run(fn())

# import asyncio
# async def fn():
# 	task=asyncio.create_task(fn2())
# 	print("one")
# 	#await asyncio.sleep(1)
# 	#await fn2()
# 	print('four')
# 	await asyncio.sleep(1)
# 	print('five')
# 	await asyncio.sleep(1)

# async def fn2():
# 	#await asyncio.sleep(1)
# 	print("two")
# 	await asyncio.sleep(1)
# 	print("three")
	
# asyncio.run(fn())

# Importing module 
# import asyncio
# import aiomysql

# async def s():
#     conn=await aiomysql.connect(user='myuser',password='mypass',db='mydb',host='127.0.0.1',port=3306)
#     cur=await conn.cursor()
#     await cur.execute('CREATE TABLE IF NOT EXISTS user2 (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)')
#     await cur.execute("INSERT INTO user2 VALUES(1,'Manav',18)")
#     await cur.execute("INSERT INTO user2 VALUES(2,'Rohit',21)")
#     await cur.execute("INSERT INTO user2 VALUES(3,'Raghav',20)")
#     await cur.execute('SELECT * FROM user2')
#     res=await cur.fetchall()
#     await conn.commit()
#     await conn.close()
#     return res
    
# async def main():
#     data=await s()
#     print(data)
    
# asyncio.run(main())


# import tornado.ioloop
# import tornado.web

# class MainHandler(tornado.web.RequestHandler):
# 	def get(self):
# 		self.write("Pong!")

# def make_app():
# 	return tornado.web.Application([(r"/ping", MainHandler)])

# if __name__ == "__main__":
# 	app = make_app()
# 	app.listen(8089)
	# tornado.ioloop.IOLoop.current().start()

  
#  *** Understanding diff between sync and async in tornado

#  Synchronous way

# import tornado.ioloop
# import tornado.web
# import time

# class Blocking(tornado.web.RequestHandler):
#     def get(self):
#         time.sleep(10)
#         self.write("Done with blocking")

# def make_app():
#     return tornado.web.Application([
#         (r"/block",Blocking)
#     ])

# if __name__ =="__main__":
#     app=make_app()
#     app.listen(8898)
#     tornado.ioloop.IOLoop.current().start()


#  Asynchronous way 

# import tornado.ioloop
# import tornado.web
# import time
# import asyncio

# class Blocking(tornado.web.RequestHandler):
#     async def get(self):
#         await asyncio.sleep(5)
#         self.write("Done with blocking")

# def make_app():
#     return tornado.web.Application([
#         (r"/block",Blocking)
#     ])

# if __name__ =="__main__":
#     app=make_app()
#     app.listen(8896)
#     print("server started")
#     tornado.ioloop.IOLoop.current().start()



#  Third party api

import tornado.ioloop
import tornado.web
import tornado.httpclient
import time
import asyncio

class synchronous(tornado.web.RequestHandler):
    def get(self):
        http_client = tornado.httpclient.HTTPClient()
        try:
            response = http_client.fetch("https://jsonplaceholder.typicode.com/posts/1")
            self.write(response.body)
        except tornado.httpclient.HTTPError as e:
            print("Error: " + str(e))
        except Exception as e:
            print("Error: " + str(e))
        finally:
            http_client.close()



# class asynchronous(tornado.web.RequestHandler):
#     async def get(self):
#         http_client = tornado.httpclient.AsyncHTTPClient()
#         try:
#             response = await http_client.fetch("https://jsonplaceholder.typicode.com/posts/1")
#             self.write(response.body)
#         except tornado.httpclient.HTTPError as e:
#             self.write("Error: " + str(e))
#         except Exception as e:
#             self.write("Error: " + str(e))
#         finally:
#             http_client.close()

def make_app():
    return tornado.web.Application([
        (r"/block",synchronous),
        # (r"/noblock",asynchronous)
    ])

if __name__ =="__main__":
    app=make_app()
    app.listen(8075)
    print("server started")
    tornado.ioloop.IOLoop.current().start()




# import tornado.ioloop
# import tornado.web
# import tornado.httpclient
# import time
# import asyncio

# class synchronous(tornado.web.RequestHandler):
#     def get(self):
#         http_client = tornado.httpclient.HTTPClient()
#         try:
#             response = httpclient.fetch("https://jsonplaceholder.typicode.com/posts/1")
#             self.write(response.body)
#         except tornado.httpclient.HTTPError as e:
#             print("Error: " + str(e))
#         except Exception as e:
#             print("Error: " + str(e))
#         finally:
#             http_client.close()


# def make_app():
#     return tornado.web.Application([
#         (r"/block",synchronous)
#     ])

# if __name__ =="__main__":
    app=make_app()
    app.listen(8876)
    print("server started")
    tornado.ioloop.IOLoop.current().start()