"""
	GetWorkProxy.py -- Handles the clients connecting to and requesting work.
	Also handles passing Long-Polling to seperate threads and handlers.
	
	by elchupa
"""

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json
import base64
from tornado.httputil import HTTPHeaders

from GetWork import GetWork
from Config import Config

#ffffffffffffffffffffffffffffffffffffffffffffffffffffffff00000000
#00000000000000000000000000000000000000000000000000a4362300000000

class GetWorkHandler( tornado.web.RequestHandler ):
	def initialize( self, sharedb, usersdb, poolname, longpoll ):
		self.getwork = GetWork( sharedb, poolname )
		self.users = usersdb
		self.longpoll = longpoll
		
	def post( self ):
		body = json.loads( self.request.body )
		username, password = base64.b64decode( self.request.headers['Authorization'][6:] ).split( ":" )
			
		if body['method'] == "getwork" and body['params'] == []:
			extensions = self.parseExtensions( self.request.headers )

			work_tuple = self.getwork.getWork( username, password )
			work = work_tuple[0]
			work['target'] = self.getwork.target
			work['error'] = None
			work['id'] = body['id']
			if work['error'] == None:
				self.users.incShare( username, password )
			
			if "longpoll" in extensions:
				longpoll = "/LP"
				self.set_header( "X-Long-Polling", longpoll )
				
				if not self.longpoll.connected:
					if self.longpoll.url == "":
						headers = work_tuple[1]
						if "x-long-polling" in headers:
							self.longpoll.updateLongPollUrl( headers['x-long-polling'] )
						elif "X-Long-Polling" in headers:
							self.longpoll.updateLongPollUrl( headers['X-Long-Polling'] )
					
					print self.longpoll.url
					self.longpoll.start()
			
			self.write( work )
		elif body['method'] == "getwork" and body['params'] != []:
			answer = self.getwork.submit( ( username, password ), body )
			self.write( answer[0] )
		
	def parseExtensions( self, headers ):
		ext = []
		
		try:
			extensions = headers['X-Mining-Extensions']
			ext = extensions.split( " " )
		except:
			pass
		
		return ext

if __name__ == "__main__":
	from PoolStore import PoolStore
	from UserStore import UserStore
	
	p = PoolStore( "config.json" )
	u = UserStore( "config.json" )
	
	application = tornado.web.Application( [ (r"/", GetWorkHandler, dict(sharedb=p, usersdb=u, poolname="mine") ) ], debug=True )
	
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(8888)
	tornado.ioloop.IOLoop.instance().start()