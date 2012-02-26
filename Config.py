import json

class Config:
	def __init__( self, file ):
		jsonfile = open( file );
		
		self.data = json.load( jsonfile );
	
	def __getitem__( self, name ):
		if name in self.data:
			return self.data[name]
		else:
			return None
			
if __name__ == "__main__":
	cc = Config( "test.json" )
	
	print cc['http']
	print cc['bitcoind']