
class Handler:
	def __init__(self, directoryKeys, directoryLocks):
		self.directoryKeys = directoryKeys
		self.directoryLocks = directoryLocks
	def getLock(self):
		pass
	def encode(self, lock):
		pass
	def decode(self, key):
		pass