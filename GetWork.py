"""
	GetWork.py -- Gets work from a mining pool.
	
	by elchupa
"""

from Config import Config

import json, base64
import httplib2
import ResourcePool
from binascii import a2b_hex, b2a_hex
from Utils import swap32, sha2int, sha2x
from datetime import datetime

from tornado.httpclient import AsyncHTTPClient, HTTPRequest

import logging



class GetWork:
	def __init__( self, database, poolname ):
		self.db = database
		self.poolname = poolname
		self.config = self.db.getPool( self.poolname )
		self.address = self.config['address']
		self.port = self.config['port']
		self.username = self.config['username']
		self.password = self.config['password']
		self.timeout = int( self.config['timeout'] )
		
		self.authorizationStr = base64.b64encode(self.username + ":" + self.password).replace('\n','')	
		self.id = 0
		
		self.target = ""
		
		self.logger = logging.getLogger( "PoolManager.Pool.GetWork" )
		
		try:
			self.target = self.config['target']
		except:
			self.target = "ffffffffffffffffffffffffffffffffffffffffffffffffffffffff00000000"
			
		self.targetInt = sha2int( sha2x( self.target ) )
		
		self.header = { "X-Mining-Extensions": "longpoll", "Authorization": "Basic " + self.authorizationStr, "User-Agent": "polcbm", "Content-Type": "text/plain" }
		self.url = "http://" + self.address + ":" + str(self.port)
		
	def getWork( self, minerName, minerPassword ):
	
		request = json.dumps( { "method": "getwork", "params": [], "id": "json" } )
		self.id += 1
		message = {
				"result": None,
				"error": {
				"code": -1,
				"message": "unregistered miner"
				},
				"id": 1
				}
		try:
			http = httplib2.Http( timeout=self.timeout )
			ret, content = http.request( self.url, "POST", headers=self.header, body=request )
			
			miner = self.db.addUser( self.poolname, minerName, minerPassword )
		
			if miner:
				try:
					message = json.loads( content )
					self.db.incGetWork( self.poolname )
					del http
					return message, ret, minerName
				except:
					del http
					self.logger.warn( "Error decoding json" )
			else:
				del http
				return message, None, minerName
		except Exception, e:
			self.logger.warn( "Error getting work" )
		return message, None, minerName
	
	def submit( self, minerName, work):
	
		validity = self.checkWorkValidity( minerName, work )
			
		request = json.dumps( work )
		ret = ""
		content = ""
		message = {
					"version": "1.1",
					"id": 1,
					"error": None,
					"result": False
				}
		try:
			http = httplib2.Http( timeout=self.timeout )
			ret, content = http.request( self.url, "POST", headers=self.header, body=request )
			
			try:
				message = json.loads( content )
				
				#if message['result']:
				#	self.db.incBlocksFound( self.poolname )
				
				if validity['status']:
					message['result'] = False
					
				share = self.db.addShare( self.poolname, validity['share'] )
				
				if share:
					message['result'] = False
				else:
					self.db.incShares( self.poolname )
					message['result'] = True
				
				if not message['result']:
					self.db.incStales( self.poolname )
			 	del http
				return message, ret, minerName
			except Exception, e:
				del http
				self.logger.warn( "Error Decoding Json submit()" )
		except Exception, e:
			self.logger.warn( "Error submitting work" )
		
		return message, None, minerName
	
	def checkWorkValidity( self, minerName, work ):
		share = self.getShare( minerName, work )
		
		if share['data'][:4] != b'\1\0\0\0':
			{ "share": share, "status": False }
			
		hash = sha2x( share['data'] )
		
		if hash[28:] != b'\0\0\0\0':
			return { "share": share, "status": False }
			
		hashInt = sha2int( hash )
		
		if hashInt >= self.targetInt:
			return { "share": share, "status": False }
			
		return { "share": share, "status": True }
	
	def getShare( self, minerName, work ):
		return { "miner": minerName, "odata": work['params'][0], "data": swap32( a2b_hex( work['params'][0] ) )[:80], "time": datetime.now() }

if __name__ == "__main__":
	
	g = GetWork( "test.json" )
	
	print g.getWork( "test" )
