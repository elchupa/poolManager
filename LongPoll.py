"""
	LongPoll.py -- Handles the long pool action with the mining pool.
		It will keep track of all clients and keep sending out the 
		same getwork untill all the clients have received it.
		
	by elchupathingy
"""

import threading
import re
import json

from tornado.httpclient import AsyncHTTPClient, HTTPRequest

class LongPoll:
	def __init__( self, pools, poolname ):
		self.pools = pools
		self.poolname = poolname
		self.count = 0
		
		self.url = ""
		
		try:
			pool = self.getPool( self.poolname )
			self.url = pool['longPollURl']
		except:
			pass
		
		self.lock = threading.RLock()
		self.newWork = ""
		self.running = False
		self.connected = False
		self.receivedBlockMsg = False
		self.request = json.dumps( { "method": "getwork", "params": [], "id": "json" } )
		
	def updateLongPollUrl( self, nUrl ):
		self.url = nUrl
		pool = self.pools.getPool( self.poolname )
		pool['longPollUrl'] = self.url
		
	def register( self ):
		self.lock.acquire()
		
		self.count += 1
		
		self.lock.release()
		
	def deregister( self ):
		self.lock.acquire()
		
		self.count -= 1
		
		if self.count < 0:
			self.count = 0
		
		self.lock.release()
		
		return self.newWork
		
	def conect( self, longPollUrl ):
		print longPollUrl
		
	def currentBlock( self ):
		if self.connected or not self.receivedBlockMsg:
			return True
		else:
			return False
			
	def start( self ):
		if self.count == 0:
			pool = self.pools.getPool( self.poolname )
			if not re.match( r"http:\/\/[\w\d\-\.]+(\:[\d]+)?(\/[\w\d\.\-]+)?", self.url ):
				self.url = "http://" + str( pool['address'] ) + ":" + str( pool['port'] ) + self.url
			print "Connecting to:", self.url	
			http = AsyncHTTPClient()
			request = HTTPRequest( self.url, "GET", auth_username = pool['username'], auth_password = pool['password'], follow_redirects = True, body=self.request, request_timeout=100000000 )
			http.fetch( request, self.gotBlockNotification )
		
			self.connected = True
		else:
			print "Not all Clients have gotten the new work"

	def gotBlockNotification( self, response ):
		if response.code != 200:
			pool = self.pools.getPool( self.poolname )
			http = AsyncHTTPClient()
			request = HTTPRequest( self.url, "GET", auth_username = pool['username'], auth_password = pool['password'], follow_redirects = True, body=self.request, request_timeout=100000000 )
			http.fetch( request, self.gotBlockNotification )
		else:
			self.connected = True
			self.connected = False
			self.receivedBlockMsg = True
			self.newWork = response
			
			print self.newWork
			print self.newWork