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


class GetWork:
	def __init__( self, config ):
		self.config = Config( config )
		
		self.address = self.config['address']
		self.port = self.config['port']
		self.username = self.config['username']
		self.password = self.config['password']
		self.timeout = int( self.config['timeout'] )
		
		self.authorizationStr = base64.b64encode(self.username + ":" + self.password).replace('\n','')
		self.http_pool = httplib2.Http( timeout=self.timeout )		
		self.id = 0
		
		self.target = ""
		
		try:
			self.target = self.config['target']
		except:
			self.target = "ffffffffffffffffffffffffffffffffffffffffffffffffffffffff00000000"
			
		self.targetInt = sha2int( sha2x( self.target ) )
		
		self.header = { "Authorization": "Basic " + self.authorizationStr, "user-agent": "curl", "content-type": "text/plain" }
		self.url = "http://" + self.address + ":" + str(self.port)
		
	def getWork( self, minerName ):
	
		request = json.dumps( { "method": "getwork", "params": [], "id": self.id } )
		self.id += 1
	
		try:
			ret, content = self.http_pool.request( self.url, "post", headers=self.header, body=request )
		except Exception, e:
			print "Error getting work: " + str(e )
			
		try:
			message = json.loads( content )
		except:
			print "Error decoding json:", content
			
		return message['result'], ret, minerName
	
	def submit( self, minerName, work):
	
		validity = self.checkWorkValidity( minerName, work )
		
		if validity['status']:
			print "Valid share"
			
		request = json.dumps( work )
		try:
			ret, content = self.http_pool.request( self.url, "post", headers=self.header, body=request )
		except Exception, e:
			print "Error submitting work: " + str( e )
		
		try:
			message = json.loads( content )
		except Exception, e:
			print "Error decoding json:", content
		
		if validity['status']:
			message['result'] = True
		
		return message, ret, minerName
	
	def checkWorkValidity( self, minerName, work ):
		share = self.getShare( minerName, work )
		
		if share['data'][:4] != b'\1\0\0\0':
			{ "share": share, "status": False }
			
		hash = sha2x( share['data'] )
		
		if hash[28:] != b'\0\0\0\0':
			return { "share": share, "status": False }
			
		hashInt = sha2int( hash )
		
		if hashInt > self.targetInt:
			return { "share": share, "status": False }
			
		return { "share": share, "status": True }
	
	def getShare( self, minerName, work ):
		return { "miner": minerName, "odata": work['params'][0], "data": swap32( a2b_hex( work['params'][0] ) )[:80], "time": datetime.now() }

if __name__ == "__main__":
	
	g = GetWork( "test.json" )
	
	print g.getWork( "test" )