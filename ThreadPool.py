"""
	ThreadPool.py -- Implement a simple thread pool.
	
	by elchupa
"""

import threading
from Queue import Queue

import logging

class Worker( threading.Thread ):
	def __init__( self, event, jobs ):
		threading.Thread.__init__( self )

		self.jobs = jobs
		self.daemon = True
		self.event = event
		self.start()

		self.logger = logging.getLogger( "ThreadPool.Worker" )

	def run( self ):
		while not self.event.is_set():
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
		self.event = threading.Event()

		for _ in range( numThreads ):
			Worker( self.event, self.jobs )

		self.logger = logging.getLogger( "PoolManager.ThreadPool" )

	def addJob( self, func, *args, **kargs ):
		self.jobs.put( ( func, args, kargs ) )
		self.logger.info( "Added a new job" )
		self.logger.info( "Threads left in pool: " + str( self.jobs.qsize() ) )
		self.logger.info( "If the Queue full? : " + str( self.jobs.full() ) )
	
	def waitAll( self ):
		self.jobs.join()
	
	def killAll( self ):
		self.event.set();

if __name__ == "__main__":

	from time import sleep
	def test( t ):
		print "yay: " + str( t )
		sleep( 1 )
	def kill( event ):
		sleep( 5 )
		event.set()
	pool = ThreadPool( 10000 )

	for i in range( 100000 ):
		pool.addJob( test, i )

	pool.waitAll()
