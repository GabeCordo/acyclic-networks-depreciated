###############################
#		python imports
###############################
import random, os
from datetime import date
from threading import Thread

###############################
#	   pynodetor imports
###############################
import node
from pynodetor.encryption import rsa
from pynodetor.bitstream import basic
from pynodetor.utils import linkerJSON, errors, enums

###############################
#		   main code
###############################
#This node is responisble for storing all SENSITIVE information, hence it is important
#that this node remain HIGHLY ANONYMOUS and can only recieve connections from the entry
#node in such a way that it acts as a proxy to conceal the address or data of this node

class Index(node.Node):
	def __init__(self, ip, directoryKeyPrivate, directoryKeyPublic, directoryIndex, directoryLog, directoryKeys):
		'''
			(Index, string, string, string, string, string) -> None
			:constructor method for the Index Class
			
			@paramaters a valid pathway(directory) for all the user-id 
						to ip-addr matches
			@exception the class constructor will throw an error if the
					   pathway is NOT valid
		'''
		super().__init__(self, ip, directoryKeyPrivate, directoryKeyPublic, True, True, False) #ecryption, listening, monitoring
		
		self.directoryIndex = directoryIndex
		self.directoryLog = directoryLog
		self.directoryKeys = directoryKeys
		
		self.l = linkerJSON(directoryLookup, directoryLog)
		self.index = self.l.data[0]
		self.log = self.l.data[1]
		
		self.startCleaner()
		
	def lookupIndex(self, userid):
		'''
			(Index, string) -> (string)
			:lookup an ip address associated with a certain id
			
			@paramaters a valid userid on the index node is provided
			@returns the ip-address of a user-id in the index JSON file
			@exception if there is an error (id doesnt exist) an empty 
					   string is returned
		'''
		try:
			return self.index[userid]['ip']
		except:
			return ''
	
	def lookupIP(self, ip):
		'''
			(Index, string) -> (string)
			:lookup the timestamp associtate with the initialization of
			 an ip with userid
			
			@paramaters a valid ip-address on the index node is provided
			@returns the userid of a ip-address in the logger JSON file
			@exception if there is an error (ip doesnt exist) an empty 
					   string is returned
		'''
		try:
			return self.log[ip]
		except:
			return ''
	
	def addRSA(self, userid, publicRSA):
		'''
			(Index, string) -> (boolean)
			:this is a private function responsible for adding a new public
			 encryption key file to the directory for all userid-keys
			
			@returns boolean true if the file was created sucessfully
			@exception returns boolean false if the file could not be made
			
				** files created with the formated (userid).pem **
		'''
		try:
			f = open(self.index[userid]['rsa'], 'wb')
			f.write(publicRSA)
			f.close()
		except:
			return False
		
		return True
	
	def lookupRSA(self, userid=None, ip=None):
		'''
			(Index, string) -> (string)
			:lookup the public RSA key associated with the provided user-id
			 from the directory of public RSA keys specified through the c-
			 lasses initializer
			
			@paramaters a valid userid on the index node is provided
			@returns the public RSA key string in the index JSON file
			@exception if there is an error (id doesnt exist) an empty string
					   is returned
		'''
		try:
			if (userid == None or ip != None):
				userid = self.lookupIP(ip)
				
			if (userid != None):
				self.lookupIndex(userid)
			
			f = open(self.index[userid]['rsa'], 'rb')
			key = f.read()
			f.close()
			
			return key
		except:
			return ''
			
	def deleteRSA(self, userid):
		'''
			(Index, string) -> (boolean)
			:deletes the public RSA key file associated with the provided
			 userid
			
			@returns boolean true if the file was removed sucessfully
			@exception returns boolean false if the file doesn't exist
			
					** looks for a file named (userid.pem) **
		'''
		try:
			check = self.lookupRSA(userid=userid)
			if (check == ''):
				return False
			
			os.remove(self.index[userid]['rsa'])
		except:
			return False
		
		return True
	
	def addIndex(self, userid, ip, publicRSA):
		'''
			(Index, string) -> (boolean)
			:insert a new user-id / ip link within the index JSON file and 
			 timestamp it in the JSON log file
			
			@paramaters a valid ip-address on the index node is provided
			@returns boolean true if the userid and ip were sucessfuly added
					 to the index and log JSON files
			@exception returns boolean false; it is likely that the userid or
					   ip has not been used before
		'''
		#check to see if the userid already exists
		if (self.lookupIndex(userid) != ''):
			return False
		#check to see if the ipaddress already has an id assigned
		if (self.lookupIP(ip) != ''):
			return False
		
		self.index[userid] = {
			'ip': ip,
			'rsa': self.directoryKeys + f'/{userid}.pem'
		}
		self.log[ip] =  userid
		self.addRSA(userid, publicRSA)
	
	def deleteIndex(self, userid, connectingIp):
		'''
			(Index, string) -> (boolean)
			:delete the userid and ip found within the index and log JSON files
			
			@paramaters the userid exists within the index JSON file and the 
						connecting ip is associated with the account
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
		
		self.deleteRSA(userid)
		self.index.pop(userid)
		self.log.pop(connectingIp)
	
	def validateRelay(self, ip):
		'''
			(Index, string) -> (boolean)
			:pings the ip-address that needs to be validated and if a ping
			 attempt fails (node closed), de-index the ip-id match
			
			@paramaters the connectingIP address given is in the JSON log
						file
			@returns boolean true if the loged relay could be reached and
					 was not de-indexed
			@exception returns boolean false if the logged relay could not
					   be reached and was de-indexed
					
			** this is to fix issues when people hard-close their client
			   nodes instead of running a proper de-indexing quit proce. **
		'''
		#check to see if the id exists already (we don't want to add an ip unknowiningly
		#and not have it link up with the index JSON file
		if ( self.lookupIP(ip) == ''):
			return False
		
		try:
			self.send(ip, '') #all empty strings are discarted (treated as a ping)
		except:
			self.deleteIndex(self.log[ip], ip)
			
		return True
			
	def encryptPathwayAndExit(self):
		'''
			(Index) -> (string)
			:creates a randomized path through the server relay nodes
			
			@returns a path of 4 node relays
		'''
		h = rsa.Handler()
		activeRelays = self.log.keys()
		
		ip_previous = ''
		for i in range(0, 4):
			random_index = random.randrange(0, len(activeRelays) )
			
			if i > 0:
				relay_ip = activeRelays.pop(random_index)
				relay_encrypted = h.encrypt(relay_ip, self.lookupRSA(ip = ip_previous))
			else:
				relay_encrypted = activeRelays.pop(random_index)
			
			pathway = pathway + ":" + relay_encrypted
			ip_previous = relay_ip
			
			if i == 3:
				activeExits = len( self.index['exit'] )
				exitNode = random.randrange(0, activeExits)
				
				exit = self.index['exit'][exitNode]['ip']
		
		return f'^{pathway}^@{exit}@'
		
	def encryptData(self, usrid, message):
		'''
			(Index) -> (string)
		'''
		h = rsa.Handler()
		encrypted_message = h.encrypt(message, self.lookupRSA(userid = usrid))
		return f'#{encrypted_message}#'
	
	def formatMessage(self, targetid, message, originid):
		'''
			(Index) -> (string)
		'''
		message = self.encryptData(message)
		route = self.encryptPathwayAndExit()
		return data + route + f'<{originid}<>{targetid}>'
				
	def specialFunctionality(self, message, connectingAddress):
		'''
			(Node, string, string) -> (boolean)
			:auto-handles the generic requests made to the indexing function
			
			@returns boolean False indicating that messages will NOT be enqueued
					 to a queue
		'''
		#parse the simple bitsream requests
		try:
			p = basic.Parser(message)
			
			request = p.getRequest()
			data_first = p.getPrimaryData()
			data_last = p.getSecondaryData()
		except:
			return False
		
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
			message = self.formatMessage(data_firt, data_last, p.getOtherData()[0])
			self.send(connectingAddress, message)
		
		#the message has been handled by the generic implemented index requests
		return False
		