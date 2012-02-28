"""
	UserStore.py -- Handles the user information.
	
	by elchupathingy
"""

from Config import Config
from pymongo import Connection
from datetime import datetime
import time

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
	
	def getUser( self, username="", password="" ):
		return self.collection.find_one( { "username": username, "password": password } )
		
	def addUser( self, username, password, owner ):
		user = { "username": username, "password": password, "owner": owner, "shares": 0, "lastShare": datetime.now() }
		return self.collection.save( user )
		
	def getUsers( self, userids ):
		users = self.collection.find( { "_id": { "$in": userids } } )
		
		ret = []
		
		for u in users:
			ret.append( u )
			
		return ret
	
	def incShare( self, username, password ):
		user = self.getUser( username, password )
		
		lastTime = time.mktime( user['lastShare'].timetuple() )
		user['shares'] += 1
		user['lastShare'] = datetime.now()
		currentTime = time.mktime( user['lastShare'].timetuple() )
		
		if "hashrate" not in user:
			if currentTime - lastTime == 0:
				currentTime += 1
			user['hashrate'] = 4297.97 / ( currentTime - lastTime ) / 2
		else:
			if currentTime - lastTime == 0:
				currentTime += 1
			user['hashrate'] += 4297.97 / ( currentTime - lastTime ) / 2
			user['hashrate'] /= 2
		
		self.collection.save( user )
		#self.collection.update( { "username": username, "password":password }, user )
	
	def getAll( self ):
		return self.collection.find()
		
	def totalUsers( self ):
		return self.getAll().count()
	
if __name__ == "__main__":
	u = UserStore( "config.json" )
	
	print u.getUser( "test" )
	
