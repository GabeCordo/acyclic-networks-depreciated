#####################################
#		   Python Imports
#####################################

from pynodetor.utils import linkerJSON

#####################################
#		   MANAKIN CONFIG
#####################################

class Config:
	
	def __init__(self, path):
		'''
			(Config, string) -> None
		'''
		self.l = linkerJSON.Handler(path)
		self.config = self.l.data[0]
	
	##		Config Settings		##
	
	def getPort(self):
		'''
			(Config) -> (int)
		'''
		return self.config['settings']['port']
	def setPort(self, port):
		'''
			(Config, int) -> None
		'''
		self.config['settings']['port'] = port
		self.l.push()
	
	def isIndexed(self):
		'''
			(Config) -> (boolean)
		'''
		return self.config['settings']['indexed']
	def setIndexed(self, index):
		'''
			(Config, boolean) -> None
		'''
		self.config['settings']['indexed'] = index
		self.l.push()
	
	def isIncoming(self):
		'''
			(Config) -> (boolean)
		'''
		return self.config['settings']['incoming']		
	def setIncoming(self, incoming):
		'''
			(Config, boolean) -> None
		'''
		self.config['settings']['incoming'] = incoming
		self.l.push()
	
	##		Caching Settings		##
	
	def isCaching(self):
		'''
			(Config) -> (boolean)
		'''
		return self.config['caching']['enabled']
	def setCaching(self, cache):
		'''
			(Config, boolean) -> None
		'''
		self.config['caching']['enabled'] = cache
		self.l.push()
		
	def directoryCaching(self):
		'''
			(Config) -> (string)
		'''
		return self.config['caching']['directory']
	def setDirectoryCaching(self, directory):
		'''
			(Config, string) -> None
		'''
		self.config['caching']['directory'] = directory
		self.l.push()
	
	##		Entry-Server		##
	
	def getEntryServer(self):
		'''
			(Config) -> (string)
		'''
		return self.config['entry-server']['ip-address']
	def setEntryServer(self, server):
		'''
			(Config, string) -> None
		'''
		self.config['entry-server']['ip-address'] = server
		self.l.push()
	
	##		Encryption Keys		##
	
	def getDirectoryPublicKey(self):
		'''
			(Config) -> (string)
		'''
		return self.config['encryption-keys']['public']
	def setDirectoryPublicKey(self, directory):
		'''
			(Config, string) -> None
		'''
		self.config['encryption-keys']['public'] = directory
		self.l.push()
	
	def getDirectoryPrivateKey(self):
		'''
			(Config, string) -> None
		'''
		return self.config['encryption-keys']['private']
	def setDirectoryPrivateKey(self, directory):
		'''
			(Config, string) -> None
		'''
		self.config['encryption-keys']['private'] = directory
		self.l.push()
	