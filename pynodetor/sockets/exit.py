#import the parent class and pathway library
import node, sys

#import the bitstream parser
sys.path.append('../bitstream/')
import parser

###########################
##Child Class of the Node##
###########################
#Responisble for sending the message request to the final destination in the userid
class NodeExit(node.Node):
	
	def __init__(self, portIn, directoryKeyPrivate, directoryKeyPublic, indexIp):
		'''(NodeExit, string, string, string, string) -> None
		'''
		super().__init__(self, portIn, directoryKeyPrivate, directoryKeyPublic, indexIp, indexPort)
	
	def stripBitsream(self, bitsream):
		''' (NodeExit, string) -> (string)
		'''
		pass
		
	def specialFunctionality(self, message, connectingAddress):
		'''(NodeExit, string, string) -> (boolean)
			:handles all messages sent to the final recipient of the message/request that
			 has transversed through the relay network
			
			@returns boolean False indicating that messages will NOT be enqueued to a queue
		'''
		return False
	