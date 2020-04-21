import json

class Index(Node):
	
	def __init__(self, directoryLookup):
		'''(Index, string) -> None
		'''
		self.directoryLookup = directoryLookup
		#check to see that the directory given for the JSON file is valid
		try:
			pathwayCheck = open(directoryLookup, 'r')
			pathwayCheck.close()
		except:
			raise FileNotFoundError('Indexing Error: the JSON directory was INVALID')
	
	def lookupIndex(self):
		'''(Index, string) -> (string)
		'''
		pass
	
	def addIndex(self):
		'''(Index, string) -> (boolean)
		'''
		pass
	
	def deleteIndex(self):
		'''(Index, string) -> (boolean)
		'''
		pass
		
	def cleaner(self):
		'''(Index) -> None
		'''
		pass