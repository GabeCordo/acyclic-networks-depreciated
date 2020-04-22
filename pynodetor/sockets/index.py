from datetime import date
import json, node

class Index(node.Node):
	
	def __init__(self, directoryIndex):
		'''(Index, string) -> None
			:constructor method for the Index Class
			
			@paramaters a valid pathway(directory) for all the user-id to ip-addr matches
			@exception the class constructor will throw an error if the pathway is NOT valid
		'''
		#check to see that the directory given for the JSON file is valid
		try:
			pathwayCheck = open(directoryLookup, 'r')
			#initialize the JSON file to a disctionary for quick-access called 'directory'
			self.directoryIndex = json.load(pathwayCheck)
			
			pathwayCheck = open(directoryLogs, 'r')
			#initialize the JSON file to a disctionary for quick-access called 'directory'
			self.directoryLogs = json.load(pathwayCheck)
		except:
			raise FileNotFoundError('Indexing Error: the JSON directory was INVALID')
		
		#initialize the JSON file to a disctionary for quick-access called 'directory'
		self.directoryIndex = json.load(pathwayCheck)
		#close the file reader for the JSON file
		pathwayCheck.close()
		
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
			return self.directoryLogs["ip-addresses"][ip]
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
		pass
	
	def specialFunctionality(self):
		'''(NodeExit) -> (boolean)
			:auto-handles the generic requests made to the indexing function
		'''
		return False
		