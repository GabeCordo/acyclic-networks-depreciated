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
	
	def __init__(self, portIn, directoryKeyPrivate, directoryKeyPublic, indexIP):
		'''(NodeRelay, string, string, string, string) -> None
			:constructor for the NodeRelay class, sets up the relay node server
		'''
		super().__init__(self, portIn, directoryKeyPrivate, directoryKeyPublic, indexIP)
	
	def discoverNextNode(self, bitsream):
		'''(NodeRelay, string) -> (list of strings)
			:discover the next relay node for communication and modify the path
			
			@paramaters a valid bitsream syntax is provided
			@returns a list of strings [the next relay node id, the modified pathway, exitpath]
			@exception returns an empty list if the paramaters are not followed
		'''
		modify = parser.Parser(bitsream)
		#retrieve the path ids and the ip-address of the exit node
		pathway = modify.get_relay_path()
		exitNode = modify.get_exit_node()
		#see whether to modify the relay path or exit node path
		activeRelays = pathway.split(':')
		nextRelay = activeRelays.pop()
		#[ only the last node, every relay but the last node, exitNode IP ]
		return [ nextRelay, ':'.join(activeRelays), exitNode ]
		
	
	def specialFunctionality(self, message, connectingAddress):
		'''(NodeRelay, string, string) -> (boolean)
			:handles all relay requests made to the server
			
			@returns boolean False indicating that messages will NOT be enqueued to a queue
		'''
		#extract the bitsream mapped route from the former entry or relay node
		resend_data = self.discoverNextNode(message)
		
		#if the next relay node is blank, this means that it needs to be sent to the exit node
		#as it is done meshing/anonymising through the network
		if (resend_data[0] == ''):
			self.send(ipOut, message)
		#the bitsream still needs to be send through the network
		else:
			message_modified = modify.replace_paths(resend_data[1], resend_data[2])
			self.send(next_relay_ip, message_modified)
		
		#the relay node should only redirect data, it should never do anything else
		#(we want to avoid users capturing any traffic on the network)
		return False