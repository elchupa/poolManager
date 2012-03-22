"""
	ThreadPool.py -- Implement a simple thread pool.
	
	by elchupa
"""

import threading
from Queue import Queue

import logging

class Worker( threading.Thread ):
	def __init__( self, jobs ):
		threading.Thread.__init__( self )

		self.jobs = jobs
		self.daemon = True
		self.work = True
		self.start()

		self.logger = logging.getLogger( "ThreadPool.Worker" )

	def run( self ):
		while self.work:
			func, args, kargs = self.jobs.get()
			self.logger.info( "Got Work" )
			try: 
				func( *args, **kargs )
			except Exception, e:
				self.logger.info( str( e ) )
			self.jobs.task_done()
class ThreadPool:
	def __init__( self, numThreads = 10 ):
		self.jobs = Queue( numThreads )
		
		for _ in range( numThreads ):
			Worker( self.jobs )

		self.logger = logging.getLogger( "ThreadPool.ThreadPool" )

	def addJob( self, func, *args, **kargs ):
		self.logger.info( "Added a new job" )
		self.jobs.put( ( func, args, kargs ) )
	
	def waitAll( self ):
		self.jobs.join()

if __name__ == "__main__":

	from time import sleep
	def test( t ):
		print "yay: " + str( t )
		sleep( 1 )

	pool = ThreadPool( 5 )

	for i in range( 100 ):
		pool.addJob( test, i )

	pool.waitAll()
