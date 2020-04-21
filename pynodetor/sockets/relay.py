##Child Class of the Node##
#Responisble for routing the packet to the next relay or exit node
class NodeRelay(Node):
	def __init__(self, portIn, directoryKeyPrivate, directoryKeyPublic, networkMap):
		'''
		'''
		super().__init__(self, portIn, directoryKeyPrivate, directoryKeyPublic)
		self.network = network
	def discoverNextNode(self):
		'''
		'''
		pass
	def modifyPathStatus(self):
		'''
		'''
		pass
	def specialFunctionality(self):
		'''
		'''
		return False