"""
	ResourcePool.py -- Provides a method to pool objects to improve concurrent
		requests for new objects, and hopefully remove the memory issue.
	by elchupa
"""
from Queue import Queue

class ResourcePool:
	def __init__( self, lambda, size=10 ):
		self.pool = Queue( size )

		for i in range( size ):
			self.pool.put( lambda() )
	def get( self ):
		return self.pool.get( True )

	def put( self, item ):
		self.pool.put( item )


if __name__ == "__main__":
	from tornado.httpclient import AsyncHTTPClient, HTTPRequest
	r = ResourcePool( AsyncHTTPClient )



