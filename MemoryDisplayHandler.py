"""
"""

import tornado.web

class MemoryDisplayHandler( tornado.web.RequestHandler ):
	def initialize( self, hp ):
		self.hp = hp

	def get( self ):
		self.write( "<pre>" + self.hp.heap() + "</pre>" )
