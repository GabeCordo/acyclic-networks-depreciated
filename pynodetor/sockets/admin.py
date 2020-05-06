###############################
#	   pynodetor imports
###############################
from pynodetor.sockets.node import Node
from pynodetor.utils.authenticator import generate
from pynodetor.utils import linkerJSON, errors, enums

###############################
#		   main code
###############################
class Admin(Node, linkerJSON.Handler):
	
	def __init__(self, authcode):
		self.authcode = authcode
			
	def refreshAuth(self):
		pass
	
	def verifyNetwork(self):
		pass
	
	def specialFunctionality(self, message, connectingAddress):
		return True