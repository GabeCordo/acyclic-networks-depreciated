###############################
#	   quickscmp imports
###############################
from quickscmp.sockets.node import Node
from quickscmp.bitstream import advanced
from quickscmp.utils import errors, enums, containers

###############################
#		   main code
###############################
#Responisble for sending the message request to the final destination in the userid

class NodeExit(Node):
	def __init__(self, container_addresses, container_paths):
		'''(NodeExit, string, string, string, string) -> None
			:the consturctor is the same as the node server, small maniplulation
			 of the origional node server to specifically redirect data to the
			 final ip
		'''
		super().__init__(container_addresses, container_paths, containers.PRESET_SETTINGS_EXIT)
	
	def checkDestination(self, id_origin):
		'''(Node) -> (string)
			:retrieves the ip-address of the userid inputed from the index server
				
			@returns the string representation of the ip-address associated with
					 the userid
			@exception if the connection is lost or the userid is invalid, returns
					   an empty string
		'''
		request = f'0:{id_origin}'
		return self.send(self.container_addresses.ip_index, request) #settup ip and port of indexing server
	
	def formatMessage(self, message, origin):
		'''(NodeExit, string) -> (string)
			:strip the advanced bitsream into a simpler form with less usless data
			 for the user and pass that to the specialFunctionality function
			
			@returns list with a simple bitsream 'request:message/origin_id' and
					 the destination id
		'''
		return f'4:{message}~{origin}'
	
	def specialFunctionality(self, message, connectingAddress):
		'''(Node, string, string) -> (boolean)
			:handles all messages sent to the final recipient of the message/
			 request that has transversed through the relay network
			
			@returns boolean False indicating that messages will NOT be enqueued
					 to a queue
		'''
		modify = advanced.Parser(bitsream)
		
		request = modify.get_request_type()
		#we need the origin in case a message needs to be sent back
		origin = modify.get_origin_id()
		destination = self.checkDestination(modify.get_target_id())
		
		#if we are sending a standard message
		if (request == '4'):
			message_formated = self.formatMessage(message, origin)
			#send to the target_id's ip on the index server on the default port for 8074
			self.send(destination, message_formated)
			
		#we shouldn't need any functionality other than sending data to a user's computer
		return (False, 'Successfuly Handled')
	