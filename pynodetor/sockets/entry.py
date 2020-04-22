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
		super().__init__(self, portIn, directoryKeyPrivate, directoryKeyPublic, indexIp, indexPort)
	
	def indexUserID(self, userid, connectingip):
		'''(NodeEntry, string, string) -> (boolean)
			:add a new userid and ip-address match on the indexing node for transmission
			
			@paramaters the userid must be unique and the ip must not have an id already indexed
			@returns a boolean true if the userid was added to the indexing node
			@exception returns boolean false if the userid or ip is already used
		'''
		idRequest = f'2:{userid}/{connectingip}'
		return self.send(self.indexIp, 8077, idRequest)

	def deindexUserID(self, userid, connectingip):
		'''(NodeEntry, string, string) -> (boolean)
			:remove a userid and ip-address match on the indexing node
			
			@paramaters the userid must be valid and the ip must be associated with the indexed id
			@returns a boolean true if the userid was removed from the indexing node
			@exception returns boolean false if the paramaters were invalid
		'''
		idRequest = f'3:{userid}/{connectingip}'
		return self.send(self.indexIp, 8077, idRequest)

	def mapAnonymousRoute(self):
		'''(NodeEntry) -> (list of strings)
			:map a route through all the tor relay nodes and choose a random exit node
			
			@returns a list of strings (relay_map, exit_node)
			@exceptions none should occur unless the indexing server is down
		'''
		idRequest = f'4:None'
		return self.send(self.indexIp, 8077, idRequest)
	
	def specialFunctionality(self, message, connectingAddress):
		'''(NodeEntry, string, string) -> (boolean)
			:handles all socket requests that pertain to the requests under 'entry node' in the docs
			
			@returns boolean False indicating that messages will NOT be enqueued to a queue
		'''
		character_seperator = message.index(':')
		request = message[:character_seperator]
		data = message[character_seperator+1:]
		
		if (request == '0'): #request to lookup index (most likely)    v
			self.checkDestination(data)
		elif (request == '7'): #request to send a message			   |
			character_seperator = message.index('/')
			userid_target = data[character_seperator+1:]
			text = data[:character_seperator]
			path = self.mapAnonymousRoute()
			template = f'<{text}<!{request}!?{path[0]}/{path[1]}?^{userid}/{userid_target}^' #add userid
			self.send(ip, 8076, template)
		elif (request == '5'): #request a Public RSA key			   |
			node_exit = self.mapAnonymousRoute()[1]
			template = f'<<!{request}!??^{userid}/{userid_target}^'
			self.send(node_exit, 8075, template)
		elif (request == '6'): #request to send a 'friend' request     |
			node_exit = self.mapAnonymousRoute()[1]
			template = f'<<!{request}!??^{userid}/{userid_target}^'
			self.send(node_exit, 8075, template)
		elif (request == '2'): #request to add index			       |
			character_seperator = message.index('/')
			userid = data[character_seperator+1:]
			userid_target = data[:character_seperator]
			self.indexUserID(userid, userid_target)
		elif (request == '3'): #request to delete index (least likely) |
			character_seperator = message.index('/')
			userid = data[character_seperator+1:]
			userid_target = data[:character_seperator]
			self.deindexUserID(userid, userid_target)
		else:
			#none of the requests matched the special functions		   ^
			return True
		#the message has been handled automaticly, there is no need to enqueue
		return False
	