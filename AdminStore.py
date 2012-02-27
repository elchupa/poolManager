"""
	AdminStore.py -- Deals with admin credentials
	
	by elchupathingy
"""

from Config import Config
from pymongo import Connection
from datetime import datetime
import time
from Utils import swap32, sha2int, sha2x
import base64

class AdminStore:
	def __init__( self, config ):
		self.config = Config( config )
		
		self.address = self.config['mongo']['address']
		self.port = self.config['mongo']['port']
		self.database = "poolManager"
		try:
			self.database = self.config['mongo']['database']
		except:
			pass
			
		self.collection = "admins"
		
		try:
			self.collection = self.config['mongo']['collection']
		except:
			pass
		
		self.con = Connection( self.address, self.port )
		self.db = self.con[self.database]
		self.collection = self.db[self.collection]
		self.collection.ensure_index( "username", unique=True )
		
	def addUser( self, username, password ):
		user = {}
		user['username'] = username
		user['password'] = base64.b64encode( sha2x( password ) )
		user['miners'] = []
		user['hashrate'] = 0
		user['shares'] = 0
		user['payoutAddress'] = ""
		
		print user
		
		return self.collection.save( user )
		
	def getUser( self, username, password ):
		if password == "": 
			return None
			
		return self.collection.find_one( { "username": username, "password": base64.b64encode( sha2x( password ) ) } )
		
	def totalAdmins( self ):
		return self.collection.find().count()

if __name__ == "__main__":
	a = AdminStore( "config.json" )
	
	print a.addUser( "elchupa", "elchupa" )
	
	print a.getUser( "elchupa", "elchupa" )

	