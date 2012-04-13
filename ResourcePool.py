"""

	ResourcePool.py -- Provides a resource pool for objects.

	by elchupa

"""

import thread
import threading

import Queue

class ResourcePool:
	def __init__( self, generate, maxObjects=100 ):
		self.generate = generate
		self.pool = Queue.Queue()
		self.maxObjects = maxObjects
		self.lock = threading.RLock()
		
		for i in range( maxObjects ):
			self.pool.put( generate() )
	def __enter__( self ):
		self.obj = self.pool.get()

		return self.obj

	def __exit__( self, t, v, b ):
		self.pool.put( self.obj )










if __name__ == "__main__":
	import random
	def generateNums():          
		return random.random()	
        from time import sleep                                
	def threadingtest(id, pool ):           
		while True:                     
			with pool as i:         
				print id,"=>",i 
				sleep( 1 )
	pool = ResourcePool( generateNums )
	thread.start_new_thread( threadingtest, (6, pool, ) )
	thread.start_new_thread( threadingtest, (7, pool, ) )
	thread.start_new_thread( threadingtest, (8, pool, ) )
	thread.start_new_thread( threadingtest, (9, pool, ) )

	try:
		while 1:
			pass
	except:
		print "Done"
