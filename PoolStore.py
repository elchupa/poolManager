"""
	PoolStore.py -- Is a abstraction over the mongodb api
	to facilitate storing and upating of pool information
	in the database.
	
	by elchupathingy
"""

from Config import Config
from pymongo import Connection

class PoolStore:
	def __init__( self, config ):
		self.config = Config( config )
		
		self.address = self.config['mongo']['address']
		self.port = self.config['mongo']['port']
		self.database = "poolManager"
		try:
			self.database = self.config['mongo']['database']
		except:
			pass
			
		self.collection = "pools"
		
		try:
			self.collection = self.config['mongo']['collection']
		except:
			pass
		
		self.con = Connection( self.address, self.port )
		self.db = self.con[self.database]
		self.collection = self.db[self.collection]
		self.collection.ensure_index( "name", unique=True )
		
	def getPool( self, poolName ):
		return self.collection.find_one( { "name": poolName } )
		
	def updatePool( self, pool ):
		return self.collection.save( pool )
		
	def removePool( self, oid ):
		return self.collection.remove( oid )
		
if __name__ == "__main__":
	p = PoolStore( "config.json" )
	
	pool = p.getPool( "mine" )
	pool['timeout'] = 5
	pool['target'] = "ffffffffffffffffffffffffffffffffffffffffffffffffffffffff00000000"
	print p.updatePool( pool )
	
	print p.getPool( "mine" )
	
	print p.removePool( "4f4ad0d46ef9dc16c8000000" )