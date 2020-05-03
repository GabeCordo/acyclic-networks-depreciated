###############################
#	   pynodetor imports
###############################
import node
from pynodetor.bitstream import basic
from pynodetor.utils import errors, enums

###############################
#		   main code
###############################
#Responisble for handling incoming connections that are to be fed through the tor network
# [we will want to keep the template (even if it can increase runtime by 0.01s, we NEED to
# [ensure a failproof transfer of data to more sensitive areas of the network

class NodeEntry(node.Node):
	def __init__(self, ip, directoryKeyPrivate, directoryKeyPublic, indexIp):
		'''
			(NodeEntry, string, string, string, string) -> None
			
			:constructor for the node entry class; provides all the connective
			 functionality to begin routing messages or act as a middle-man for
			 indexing/removing/lookingup userids on the index node
		'''
		super().__init__(self, ip, directoryKeyPrivate, directoryKeyPublic, indexIp, True, True, False) #ecryption, listening, monitoring
		
	def checkDestination(self, userid):
		'''
			(Node) -> (string)
			:retrieves the ip-address of the userid inputed from the index server
			
			@returns the string representation of the ip-address associated with
					 the userid
			@exception if the connection is lost or the userid is invalid, returns
					 an empty string
		'''
		idRequest = f'0:{userid}'
		return self.send(self.indexIp, idRequest) #settup ip and port of indexing server
	
	def indexUserID(self, userid, connectingip):
		'''
			(NodeEntry, string, string) -> (boolean)
			:add a new userid and ip-address match on the indexing node for
			 transmission
			
			@paramaters the userid must be unique and the ip must not have an id
						already indexed
			@returns a boolean true if the userid was added to the indexing node
			@exception returns boolean false if the userid or ip is already used
		'''
		idRequest = f'2:{userid}/{connectingip}'
		return self.send(self.indexIp, idRequest)

	def deindexUserID(self, userid, connectingip):
		'''
			(NodeEntry, string, string) -> (boolean)
			:remove a userid and ip-address match on the indexing node
			
			@paramaters the userid must be valid and the ip must be associated
						with the indexed id
			@returns a boolean true if the userid was removed from the indexing
					 node
			@exception returns boolean false if the paramaters were invalid
		'''
		idRequest = f'3:{userid}/{connectingip}'
		return self.send(self.indexIp, idRequest)
		
	def useridOfAddress(self, ip):
		'''
			(NodeEntry, string) -> (string)
			:finds the associated id with the connecting ip address
			
			** this is a private function, it is important only the
			   entry node has this functionality					 **
		'''
		return self.send(self.indexIP, f'1:{ip}')
		
	def formatMessage(self, targetid, message, userid):
		'''
			(NodeEntry) -> None
			:formats the data into an advanced parsable bitsream request for
			 transmitting messages
		'''
		return self.send(self.indexIP, f'4:{targetid}/{message}')
	
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
			return
		
		#request to lookup index (most likely)
		if (request == '0'):
			self.checkDestination(data)
		#request to send a message
		elif (request == '4'):
			self.formatMessage(connectingAddress, data_first, data_last, b.getOtherData()[0])
		#request to add index
		elif (request == '2'):
			self.indexUserID(data_fist, data_last) #data_first: userid | data_last: userip
		#request to delete index (least likely)
		elif (request == '3'):
			self.deindexUserID(data_first, data_last) #data_first: userid | data_last: userip
		
		#the message has been handled automaticly, there is no need to enqueue
		return False
	