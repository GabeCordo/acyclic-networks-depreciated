import node

##Child Class of the Node##
#Responisble for sending the message request to the final destination in the userid
class NodeExit(node.Node):
	def __init__(self, portIn, directoryKeyPrivate, directoryKeyPublic, networkMap):
		''' (NodeExit, string, string, string, list) -> None
		'''
		super().__init__(self, portIn, directoryKeyPrivate, directoryKeyPublic)
		self.network = network
	def stripBitsream(self):
		''' (NodeExit, string) -> (string)
		'''
		pass
	def specialFunctionality(self):
		''' (NodeExit) -> (boolean)
		'''
		return False
	