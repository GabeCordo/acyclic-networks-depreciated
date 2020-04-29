#import the parent class and pathway library
import node, sys

#import the bitstream parser
sys.path.append('../bitstream/')
import parser

###########################
##Child Class of the Node##
###########################
#Responisble for handling incoming connections that are to be fed through the tor network

###########################
# we will want to keep the template (even if it can increase runtime by 0.01s, we NEED to
# ensure a failproof transfer of data to more sensitive areas of the network
###########################
class NodeEntry(node.Node):
	
	def __init__(self, portIn, directoryKeyPrivate, directoryKeyPublic, indexIp):
		'''(NodeEntry, string, string, string, string) -> None
			:constructor for the node entry class; provides all the connective functionality to begin routing
			 messages or act as a middle-man for indexing/removing/lookingup userids on the index node
		'''
		super().__init__(self, portIn, directoryKeyPrivate, directoryKeyPublic, indexIp)
	
	def checkDestination(self, userid):
		'''(Node) -> (string)
			:retrieves the ip-address of the userid inputed from the index server
			
			@returns the string representation of the ip-address associated with the userid
			@exception if the connection is lost or the userid is invalid, returns an empty string
		'''
		idRequest = f'0:{userid}'
		return self.send(self.indexIp, idRequest) #settup ip and port of indexing server
	
	def indexUserID(self, userid, connectingip):
		'''(NodeEntry, string, string) -> (boolean)
			:add a new userid and ip-address match on the indexing node for transmission
			
			@paramaters the userid must be unique and the ip must not have an id already indexed
			@returns a boolean true if the userid was added to the indexing node
			@exception returns boolean false if the userid or ip is already used
		'''
		idRequest = f'2:{userid}/{connectingip}'
		return self.send(self.indexIp, idRequest)

	def deindexUserID(self, userid, connectingip):
		'''(NodeEntry, string, string) -> (boolean)
			:remove a userid and ip-address match on the indexing node
			
			@paramaters the userid must be valid and the ip must be associated with the indexed id
			@returns a boolean true if the userid was removed from the indexing node
			@exception returns boolean false if the paramaters were invalid
		'''
		idRequest = f'3:{userid}/{connectingip}'
		return self.send(self.indexIp, idRequest)

	def mapAnonymousRoute(self):
		'''(NodeEntry) -> (list of strings)
			:map a route through all the tor relay nodes and choose a random exit node
			
			@returns a list of strings (relay_map, exit_node)
			@exceptions none should occur unless the indexing server is down
		'''
		idRequest = f'4:none/none'
		return self.send(self.indexIp, idRequest)
		
	def useridOfAddress(self, ip):
		'''(NodeEntry, string) -> (string)
			:finds the associated id with the connecting ip address
			**this is a private function, it is important only the entry node has this functionality**
		'''
		return self.send(self.indexIP, f'1:{ip}')
	
	def specialFunctionality(self, message, connectingAddress):
		'''(NodeEntry, string, string) -> (boolean)
			:handles all socket requests that pertain to the requests under 'entry node' in the docs
			
			@returns boolean False indicating that messages will NOT be enqueued to a queue
		'''
		
		#parse the simple bitsream requests
		try:
			request_seperator = origin_and_target_ids.index(':')
			data_seperator = origin_and_target_ids.index('/')
			#the request is from index 0 to the request seperator
			request = message[:request_seperator]
			#the first data is from the index after the index seperator to the data seperator
			data_first = message[request_seperator+1:data_seperator]
			#the second data is from the index after the data seperator to the end of the bitsream
			data_last = message[data_seperator+1:]
		except:
			#the message is not specific to the generic indexing requests
			return True
		
		#request to lookup index (most likely)
		if (request == '0'):
			self.checkDestination(data)
		#request to send a message
		elif (request == '7'):
			path = self.mapAnonymousRoute()
			#find what the id is of the individual who sent the request
			userid = self.useridOfAddress(connectingAddress)
			template = f'#{data_first}#?7?^{path[0]}^@{path[1]}@<{userid}<>{data_last}>' #add userid
			self.send(ip, template)
		#request a Public RSA key
		elif (request == '5'):
			path = self.mapAnonymousRoute()
			#find what the id is of the individual who sent the request
			userid = self.useridOfAddress(connectingAddress)
			template = f'?5?<{userid}<>{data_first}>'
			self.send(path[1], template)
		#request to send a 'friend' request
		elif (request == '6'):
			path = self.mapAnonymousRoute()
			#find what the id is of the individual who sent the request
			userid = self.useridOfAddress(connectingAddress)
			template = f'?6?<{userid}<>{data_first}>'
			self.send(path[1], template)
		#request to add index
		elif (request == '2'):
			#data_first is userid, data_lat is userip
			self.indexUserID(data_fist, data_last)
		#request to delete index (least likely)
		elif (request == '3'):
			#data_first is userid, data_lat is userip
			self.deindexUserID(data_first, data_last)
		else:
			#none of the requests matched the special functions		   ^
			return True
		
		#the message has been handled automaticly, there is no need to enqueue
		return False
	