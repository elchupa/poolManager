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

from GetWork import GetWork
from Config import Config

#ffffffffffffffffffffffffffffffffffffffffffffffffffffffff00000000
#00000000000000000000000000000000000000000000000000a4362300000000

class GetWorkHandler( tornado.web.RequestHandler ):
	def initialize( self ):
		self.getwork = GetWork( "test.json" )
		self.config = Config( "test.json" )
		
	def post( self ):
		body = json.loads( self.request.body )
		username, password = base64.b64decode( self.request.headers['Authorization'][6:] ).split( ":" )
		if self.checkMiner( username, password ):
			print "Valid Miner"
		if body['method'] == "getwork" and body['params'] == []:
			work_tuple = self.getwork.getWork( "test" )
			work = work_tuple[0]
			work['target'] = self.getwork.target
			work['error'] = None
			work['id'] = body['id']
			print "getWork"
			self.write( work )
		elif body['method'] == "getwork" and body['params'] != []:
			answer = self.getwork.submit( username, body )
			if answer[0]['result']:
				print "Valid share"
			self.write( answer[0] )
			
	def checkMiner( self, username, password ):
		return True

if __name__ == "__main__":

	application = tornado.web.Application( [ (r"/", GetWorkHandler) ], debug=True )
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(8888)
	tornado.ioloop.IOLoop.instance().start()