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
import threading
import functools

from tornado.httputil import HTTPHeaders
from tornado.httpclient import AsyncHTTPClient, HTTPRequest

from GetWork import GetWork
from Config import Config

import logging

#Difficutly values.
#ffffffffffffffffffffffffffffffffffffffffffffffffffffffff00000000
#00000000000000000000000000000000000000000000000000a4362300000000

class GetWorkHandler( tornado.web.RequestHandler ):
	def initialize( self ):
		self.getwork = self.application.getwork
		self.users = self.application.users
		self.longpoll = self.application.longpoll
		self.threadpool = self.application.threadpool
		self.logger = logging.getLogger( "PoolManager.Pool.GetWorkHandler" )

	@tornado.web.asynchronous
	def post( self ):
		body = json.loads( self.request.body )
		username, password = base64.b64decode( self.request.headers['Authorization'][6:] ).split( ":" )
		extensions = self.parseExtensions( self.request.headers )
		self.logger.info( "Adding a new postThread job to thread pool" )
		self.threadpool.addJob( self.postThread, body, username, password, extensions )
		
	def postThread( self, body, username, password, extensions ):
		ret = None
		
		if body['method'] == "getwork" and body['params'] == []:
			self.logger.debug( "Get Work Request by: %s", username )
			#
			#TODO Covnert this to a tornado asynch request
			#
			work_tuple = self.getwork.getWork( username, password )
			work = work_tuple[0]
			work['target'] = self.getwork.target
			work['error'] = None
			work['id'] = body['id']
			if work['error'] == None:
				self.users.incShare( username, password )
			#
			#The above should be in the callback.
			#
			if "longpoll" in extensions:
				self.logger.debug( "Miner Supports Long Polling: %s", username )
				longpoll = "/LP"
				self.set_header( "X-Long-Polling", longpoll )
				
				if not self.longpoll.connected:
					self.logger.debug( "LongPoll class was not connected or started...starting now" )
					if self.longpoll.url == "":
						headers = work_tuple[1]
						if "x-long-polling" in headers:
							self.longpoll.updateLongPollUrl( headers['x-long-polling'] )
						elif "X-Long-Polling" in headers:
							self.longpoll.updateLongPollUrl( headers['X-Long-Polling'] )
					self.longpoll.start()
					
			ret = work
		elif body['method'] == "getwork" and body['params'] != []:
			self.logger.debug( "Work Submit Request by: %s", username )
			answer = self.getwork.submit( ( username, password ), body )
			ret = answer[0]
		
		#tornado.ioloop.IOLoop.instance().add_callback(functools.partial(callback, ret))
		self.users.con.end_request()

		self.write( ret )
		self.finish()
	#def postFinish( self, response ):
	#	self.write( response )
	#	self.finish()
		
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
