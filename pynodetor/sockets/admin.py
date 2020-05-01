import node
from pynodetor.utils import linkerJSON
from pynodetor.utils.authenticator import generate

class Admin(node.Node, linkerJSON.Handler):
	
	def __init__(self, authcode):
		self.authcode = authcode
			
	def refreshAuth(self):
		pass
	
	def verifyNetwork(self):
		pass
	
	def specialFunctionality(self, message, connectingAddress):
		return True