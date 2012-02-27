"""
	UserStore.py -- Handles the user information.
	
	by elchupathingy
"""

from Config import Config
from pymongo import Connection
from datetime import datetime

class UserStore:
	def __init__( self, config ):
		self.config = Config( config )
		
		self.address = self.config['mongo']['address']
		self.port = self.config['mongo']['port']
		self.database = "poolManager"
		try:
			self.database = self.config['mongo']['database']
		except:
			pass
			
		self.collection = "users"
		
		try:
			self.collection = self.config['mongo']['collection']
		except:
			pass
			
		self.con = Connection( self.address, self.port )
		self.db = self.con[self.database]
		self.collection = self.db[self.collection]
		self.collection.ensure_index( "username", unique=True )
	
	def getUser( self, username="", password=None ):
	
		user = self.collection.find_one( { "username": username } )
		
		if user == None:
			user = { "username": username, "password": password, "shares": 0, "lastShare": datetime.now() }
			self.collection.save( user )
			user = self.collection.find_one( { "username": username } )

		return user
	
	def incShare( self, username="", password="" ):
		

if __name__ == "__main__":
	u = UserStore( "config.json" )
	
	print u.getUser( "test" )