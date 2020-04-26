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
			:the consturctor is the same as the node server, small maniplulation of the origional
			 node server to specifically redirect data to the final ip
		'''
		super().__init__(self, portIn, directoryKeyPrivate, directoryKeyPublic, indexIp)
	
	def stripBitsream(self, bitsream):
		'''(NodeExit, string) -> (string)
			:strip the advanced bitsream into a simpler form with less usless data for the user
			 and pass that to the specialFunctionality function
			
			@returns list with a simple bitsream 'mesage:message_origin' and the destination id
		'''
		modify = parser.Parser(bitsream)
		message = modify.get_message()
		origin = modify.get_origin_id() #we need the origin in case a message needs to be sent back
		destination = modify.get_target_id()
		return [ f'{message}:{origin}', destination ]
		
	def specialFunctionality(self, message, connectingAddress):
		'''(NodeExit, string, string) -> (boolean)
			:handles all messages sent to the final recipient of the message/request that
			 has transversed through the relay network
			
			@returns boolean False indicating that messages will NOT be enqueued to a queue
		'''
		data_exit = self.stripBitsream(message)
		destination_ip = self.checkDestination( data_exit[1] )
		#send to the target_id's ip on the index server on the default port for 8074
		self.send( destination_ip, 8074, data_exit[0] )
		#we shouldn't need any functionality other than sending data to a user's computer
		return False
	