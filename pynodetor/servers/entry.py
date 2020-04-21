##Child Class of the Node##
#Responisble for handling incoming connections that are to be fed through the tor network
class NodeEntry(Node):
	def __init__(self, portIn, directoryKeyPrivate, directoryKeyPublic, networkMap):
		super().__init__(self, portIn, directoryKeyPrivate, directoryKeyPublic)
		self.network = network
	def mapPathway(self):
		pass
	def checkDestination(self):
		pass
	