###############################
#	   pynodetor imports
###############################
from pynodetor.bitstream import basic
from pynodetor.sockets.node import Node
from pynodetor.utils import errors, enums

###############################
#		   main code
###############################
#Responisble for handling incoming connections that are to be fed through the tor network
# [we will want to keep the template (even if it can increase runtime by 0.01s, we NEED to
# [ensure a failproof transfer of data to more sensitive areas of the network

class NodeEntry(Node):
	def __init__(self, ip, port, ip_index, ip_backup, directory_key_private, directory_key_public):
		'''
			(NodeEntry, string, string, string, string, boolean) -> None
			
			:constructor for the node entry class; provides all the connective
			 functionality to begin routing messages or act as a middle-man for
			 indexing/removing/lookingup userids on the index node
		'''
		super().__init__(ip, port, ip_index, ip_backup, directory_key_private,
						 directory_key_public, True, True, False, True) #ecryption, listening, monitoring
		
		#determines whether the message should be sent strait to the target-ip after
		#being encrypted by the indexing node
		self.simplified_network = False
		
	def checkDestination(self, id_origin):
		'''
			(Node) -> (string)
			:retrieves the ip-address of the userid inputed from the index server
			
			@returns the string representation of the ip-address associated with
					 the userid
			@exception if the connection is lost or the userid is invalid, returns
					 an empty string
		'''
		request = f'0:{id_origin}'
		return self.send(self.ip_index, request) #settup ip and port of indexing server
	
	def indexUserID(self, id_origin, ip_connecting):
		'''
			(NodeEntry, string, string) -> (boolean)
			:add a new userid and ip-address match on the indexing node for
			 transmission
			
			@paramaters the userid must be unique and the ip must not have an id
						already indexed
			@returns a boolean true if the userid was added to the indexing node
			@exception returns boolean false if the userid or ip is already used
		'''
		request = f'2:{id_origin}~{ip_connecting}'
		return self.send(self.ip_index, request)

	def deindexUserID(self, id_origin, ip_connecting):
		'''
			(NodeEntry, string, string) -> (boolean)
			:remove a userid and ip-address match on the indexing node
			
			@paramaters the userid must be valid and the ip must be associated
						with the indexed id
			@returns a boolean true if the userid was removed from the indexing
					 node
			@exception returns boolean false if the paramaters were invalid
		'''
		request = f'3:{id_origin}~{ip_connecting}'
		return self.send(self.ip_index, request)
		
	def useridOfAddress(self, ip):
		'''
			(NodeEntry, string) -> (string)
			:finds the associated id with the connecting ip address
			
			** this is a private function, it is important only the
			   entry node has this functionality					 **
		'''
		return self.send(self.ip_index, f'1:{ip}')
		
	def formatMessage(self, id_target, message, id_origin):
		'''
			(NodeEntry) -> None
			:formats the data into an advanced parsable bitsream request for
			 transmitting messages
		'''
		#process the relay-web ready string
		message = self.send(self.ip_index, f'4:{id_target}~{message}')
		data = message.split('%')
		#send the message to the target or into the network and get a status code
		check = self.send(data[0], data[1])
		return check
	
	def specialFunctionality(self, message, connectingAddress):
		'''
			(Node, string, string) -> (boolean)
			:handles all socket requests that pertain to the requests under
			 'entry node' in the docs
			
			@returns boolean False indicating that messages will NOT be
					 enqueued to a queue
		'''
		#validate syntax in-case the message hasn't been run through a balancer which verifies syntax
		try:
			b = basic.Parser(message)
			request = b.getRequest()
			data_first = b.getPrimaryData()
			data_last = b.getSecondaryData()
		except:
			return (False, '')
		
		#request to lookup index (most likely)
		if (request == '0'):
			check = self.checkDestination(data)
			return (False, check)
		#request to send a message
		elif (request == '4'):
			message = self.formatMessage(connectingAddress, data_first, data_last, b.getOtherData()[0])
			return (False, check)
		#request to add index
		elif (request == '2'):
			check = self.indexUserID(data_fist, data_last) #data_first: userid | data_last: userip
			return (False, check)
		#request to delete index (least likely)
		elif (request == '3'):
			check = self.deindexUserID(data_first, data_last) #data_first: userid | data_last: userip
			return (False, check)
		
		#the message has been handled automaticly, there is no need to enqueue
		return (False, '')
	