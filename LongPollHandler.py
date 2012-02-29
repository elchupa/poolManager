"""
	LongPoolRequestHandler.py -- Handles long pool requests from miners.
	by elchupa
"""

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.ioloop
import json
import base64
import time
import threading
import functools
import logging

from datetime import datetime

class LongPollHandler( tornado.web.RequestHandler ):
	def initialize( self, pools,  users, poolname, longpoll ):
		self.users = users
		self.pools = pools
		self.poolname = poolname
		self.longpoll = longpoll
		self.thread = None
		
		self.logging = logging.getLogger( "PoolManager.Pool.LongPoolHandler" )
		
	@tornado.web.asynchronous
	def get( self ):
		self.thread = threading.Thread(target=self.getThread, args=(self.getFinish,) )
		self.thread.start()
		
	def getFinish( self, response ):
		self.write( response )
		self.finish()
		
		try:
			res = json.loads( response );
		
			if res['id'] != -1:
				self.pools.clearShares( self.poolname )
		except:
			pass
		
	def getThread( self, callback ):
		self.longpoll.register()
		
		while self.longpoll.currentBlock() == True:
			time.sleep( 5 )
			
		output = self.longpoll.deregister()
		
		tornado.ioloop.IOLoop.instance().add_callback(functools.partial(callback, output))