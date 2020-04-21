##Child Class of the Node##
#Responisble for sending the message request to the final destination in the userid
class NodeEntry(Node):
	def __init__(self, portIn, directoryKeyPrivate, directoryKeyPublic, networkMap):
		super().__init__(self, portIn, directoryKeyPrivate, directoryKeyPublic)
		self.network = network
	def modifyPath(self):
		pass
	def deliverPacket(self):
		pass
	