import node, random
from datetime import date
from threading import Thread
from pynodetor.bitstream import basic
from pynodetor.utils import linkerJSON


###########################
## Indexing DATA Node    ##
###########################
#This node is responisble for storing all SENSITIVE information, hence it is important
#that this node remain HIGHLY ANONYMOUS and can only recieve connections from the entry
#node in such a way that it acts as a proxy to conceal the address or data of this node
class Index(node.Node):
	def __init__(self, ip, directoryKeyPrivate, directoryKeyPublic, directoryLookup, directoryLog):
		'''(Index, string, string, string, string, string) -> None
			:constructor method for the Index Class
			
			@paramaters a valid pathway(directory) for all the user-id to ip-addr matches
			@exception the class constructor will throw an error if the pathway is NOT valid
		'''
		super().__init__(self, ip, directoryKeyPrivate, directoryKeyPublic)
		self.directoryLookup = directoryLookup
		self.directoryLog = directoryLog
		self.l = linkerJSON(directoryLookup, directoryLog)
		self.directoryLogs = self.l.data[0]
		self.directoryIndex = self.l.data[1]
		
	def lookupIndex(self, userid):
		'''(Index, string) -> (string)
			:lookup an ip address associated with a certain id
			
			@paramaters a valid userid on the index node is provided
			@returns the ip-address of a user-id in the index JSON file
			@exception if there is an error (id doesnt exist) an empty string is returned
		'''
		try:
			return self.directoryIndex["index"][userid]
		except:
			return ''
	
	def lookupIP(self, ip):
		'''(Index, string) -> (string)
			:lookup the timestamp associtate with the initialization of an ip with userid
			
			@paramaters a valid ip-address on the index node is provided
			@returns the timestamp of a ip-address in the logger JSON file
			@exception if there is an error (ip doesnt exist) an empty string is returned
		'''
		try:
			return self.directoryLogs["ip-addresses"].append(ip)
		except:
			return ''
	
	def addIndex(self, userid, ip):
		'''(Index, string) -> (boolean)
			:insert a new user-id / ip link within the index JSON file and timestamp it in the JSON log file
			
			@paramaters a valid ip-address on the index node is provided
			@returns boolean true if the userid and ip were sucessfuly added to the index and log JSON files
			@exception returns boolean false; it is likely that the userid or ip has not been used before
		'''
		#check to see if the userid already exists
		if (self.lookupIndex(userid) != ''):
			return False
		#check to see if the ipaddress already has an id assigned
		if (self.lookupIP(ip) != ''):
			return False
		self.directoryIndex["index"][userid] = ip
		self.directoryLogs["ip-addresses"][ip] = str( date.today() ) #convert from date to string type
	
	def deleteIndex(self, userid, connectingIp):
		'''(Index, string) -> (boolean)
			:delete the userid and ip found within the index and log JSON files
			
			@paramaters the userid exists within the index JSON file and the connecting
						ip is associated with the account
			@returns boolean true if the userid was sucessfuly deleted
			@exception returns boolean false if any of the paramaters are not met
		'''
		loggedIP = self.lookupIndex(userid)
		#check to see that if the userid exists (the ip will exist if the userid does)
		if (loggedIP == ''):
			return False
		#check to see that the ip-address matches the logged user-id
		if (loggedIP != connectingIp):
			return False
		self.directoryIndex["index"].pop(userid)
		self.directoryLogs.pop(connectingIp)
	
	def resetLoggedDate(self, connectingIp):
		'''(Index, string) -> (boolean)
			:reset the time-stamp on the JSON log file to ensure that the cleaner does not delete all data
			
			@paramaters the connectingIP address given is in the JSON log file
			@returns boolean true if the time-stamp was changed to the current day
			@exception returns boolean false if your ip has not been logged before
		'''
		#check to see if the id exists already (we don't want to add an ip unknowiningly
		#and not have it link up with the index JSON file
		if ( self.lookupIP(connectingIp) == ''):
			return False
		self.directoryLogs[connectingIp] = str( date.today() ) #convert from date to string type
	
	def cleaner(self):
		'''(Index) -> None
			:responsible for removing ip-addresses that go unused for over two days
			** this is to make sure that ip's are not stored forever (NO LOGS ALLOWED) **
		'''
		while True:
			#run this script every 10 minutes to updates the tor index
			time.sleep(600)
			ipAddresses = getList(self.directoryLogs)
			#iterate over every logged ip address and associated with it  
			for i in range(0, len(ipAddresses)):
				currentUserIP = ipAddresses[i]
				currentUserID = self.directoryLogs["ip-addresses"][i]
				#ping the address (an empty string will not be queued and dropped)
				connectionResponse = self.send(currentUserIP, portOut, '')
				if (connectionResponse == '2'):
					self.deleteIndex(currentUserID, currentUserIP)
			#write the current JSON dictionaries to the JSON files in-case the server unexpectedly stops
			#to avoid the loss of data stored on the heap
			pathwayCheck = open(self.directoryLookup, 'w')
			json.dump(self.directoryIndex, pathwayCheck)
			pathwayCheck = open(self.directoryLog, 'w')
			json.dump(self.directoryLogs, pathwayCheck)
			pathwayCheck.close()
	
	def mapPathway(self):
		'''(Index) -> (string)
			:creates a randomized path through the server relay nodes
			
			@returns a path of 4 node relays
		'''
		activeRelays = self.directoryLogs.keys()
		for i in range(0, 4):
			relayNode = random.randrange(0, activeRelays)
			pathway = activeRelays[relayNode] + ':'
		return pathway[:len(pathway)]
			
	def mapExit(self):
		'''(Index) -> (string)
			:chooses one random exit node to leave (reduce the chance of someone sitting on the end
			 of the socket and listening to the unencrypted traffic)
			
			@returns the ip of one exit node of n many within the index JSON file
		'''
		activeExits = len( self.directoryIndex['index']['entry'] )
		exitNode = random.randrange(0, activeExits)
		return self.directoryIndex['index']['entry'][exitNode]['ip-address']
	
	def specialFunctionality(self, message, connectingAddress):
		'''(NodeExit, string, string) -> (boolean)
			:auto-handles the generic requests made to the indexing function
			
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
			
		if (request == '0'):
			address = self.lookupIndex(data_first) #the first data is the userid
			self.send(connectingAddress, address)
		elif (request == '1'):
			userid = self.lookupIP(data_first) #the first data is the ip
			self.send(connectingAddress, userid)
		elif (request == '2'):
			check = self.addIndex(data_first, data_last) #the first data is the userid, last is userip
			self.send(connectingAddress, check)
		elif (request == '3'): 
			check = self.deleteIndex(data_first, data_last) #the first data is the userid, last is userip
		elif (request == '4'):
			path = self.mapPathway() #the relays pathway
			exit = self.mapExit() #the exit node ip
			self.send(connectingAddress, f'{path}/{exit}') #concat the two together and release
		else:
			#the message is not specific to the generic indexing requests
			return True
		
		#the message has been handled by the generic implemented index requests
		return False
		