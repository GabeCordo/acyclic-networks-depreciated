#import the parent class and pathway library
import node, sys

#import the bitstream parser
sys.path.append('../bitstream/')
import parser

###########################
##Child Class of the Node##
###########################
#Responisble for routing the packet to the next relay or exit node
class NodeRelay(node.Node):
	
	def __init__(self, portIn, directoryKeyPrivate, directoryKeyPublic, indexIp):
		'''(NodeRelay, string, string, string, string) -> None
			:constructor for the NodeRelay class, sets up the relay node server
		'''
		super().__init__(self, portIn, directoryKeyPrivate, directoryKeyPublic, indexIp, indexPort)
	
	def discoverNextNode(self, bitsream):
		'''(NodeRelay, string) -> (list of strings)
			:discover the next relay node for communication and modify the path
			
			@paramaters a valid bitsream syntax is provided
			@returns a list of strings [the next node id, the modified pathway]
			@exception returns an empty list if the paramaters are not followed
		'''
		modify = parser.Parser(bitsream)
		#retrieve the path ids and the ip-address of the exit node
		relayPath = modify.get_relay_path()
		exitNode = modify.get_exit_node()
		#see whether to modify the relay path or exit node path
		if (relayPath == ''):
			return [ exitNode, '' ]
		else:
			numberOfRelays = len(relayPath)
			return [ relayPath[numberOfRelays], relayPath[:numberOfRelays] ]
		
	
	def specialFunctionality(self, message, connectingAddress):
		'''(NodeRelay, string, string) -> (boolean)
			:handles all relay requests made to the server
			
			@returns boolean False indicating that messages will NOT be enqueued to a queue
		'''
		return False