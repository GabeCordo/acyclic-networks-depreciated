###############################
#		python imports
###############################
import random
from os import remove
from datetime import date
from threading import Thread

###############################
#	   quickscmp imports
###############################
from quickscms.encryption import rsa
from quickscms.bitstream import basic
from quickscms.sockets.node import Node
from quickscms.linker import linkerJSON
from quickscms.utils import errors, enums, containers

###############################
#		   main code
###############################
#This node is responisble for storing all SENSITIVE information, hence it is important
#that this node remain HIGHLY ANONYMOUS and can only recieve connections from the entry
#node in such a way that it acts as a proxy to conceal the address or data of this node

class Index(Node, linkerJSON.Handler):
	def __init__(self, container_addresses, container_paths, 
				 directory_index, directory_log, directory_collected_keys, 
				 simplified_network = False):
		'''
			(Index, string, string, string, string, string, boolean) -> None
			:constructor method for the Index Class
			
			@paramaters a valid pathway(directory) for all the user-id 
						to ip-addr matches
			@exception the class constructor will throw an error if the
					   pathway is NOT valid
		'''
		Node.__init__(self, container_addresses, container_paths, containers.PRESET_SETTINGS_INDEX)
		linkerJSON.Handler.__init__(self, directory_index, directory_log)
		
		##Setting up indexing, logging JSON files AND the RSA keys directory for storage
		self.directory_index = directory_index
		self.directory_log = directory_log
		self.directory_collected_keys = directory_collected_keys
		
		##Settup the indexing node to either run on simplified network mode or full mode
		self.simplified_network = simplified_network
		
		##Pull the extracted JSON sheets from the linkerJSON class variable 'self.data'
		self.index = self.data[0]
		self.log = self.data[1]
		
	def lookupIndex(self, id_origin):
		'''
			(Index, string) -> (string)
			:lookup an ip address associated with a certain id
			
			@paramaters a valid userid on the index node is provided
			@returns the ip-address of a user-id in the index JSON file
			@exception if there is an error (id doesnt exist) an empty 
					   string is returned
		'''
		try:
			return self.index[id_origin]['ip']
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
	
	def addRSA(self, id_origin, rsa_public):
		'''
			(Index, string) -> (boolean)
			:this is a private function responsible for adding a new public
			 encryption key file to the directory for all userid-keys
			
			@returns boolean true if the file was created sucessfully
			@exception returns boolean false if the file could not be made
			
				** files created with the formated (userid).pem **
		'''
		try:
			f = open(self.index[id_origin]['rsa'], 'w')
			f.write(rsa_public)
			f.close()
		except:
			return False
		
		return True
	
	def lookupRSA(self, id_origin=None, ip=None):
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
			if (id_origin == None or ip != None):
				id_origin = self.lookupIP(ip)
				
			if (id_origin != None):
				self.lookupIndex(id_origin)
			
			test = self.index[id_origin]['rsa']
			f = open(self.index[id_origin]['rsa'], 'rb')
			key = f.read()
			f.close()
			
			return key
		except:
			return ''
			
	def deleteRSA(self, id_origin):
		'''
			(Index, string) -> (boolean)
			:deletes the public RSA key file associated with the provided
			 userid
			
			@returns boolean true if the file was removed sucessfully
			@exception returns boolean false if the file doesn't exist
			
					** looks for a file named (userid.pem) **
		'''
		try:
			check = self.lookupRSA(id_origin=id_origin)
			if (check == ''):
				return False
			
			remove(self.index[id_origin]['rsa'])
		except:
			return False
		
		return True
	
	def addIndex(self, id_origin, publicRSA, ip_connecting):
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
		if (self.lookupIndex(id_origin) != ''):
			return 'Already Indexed'
		#check to see if the ipaddress already has an id assigned
		if (self.lookupIP(ip_connecting) != ''):
			return 'Already Has IP'
		
		self.index[id_origin] = {
			'ip': ip_connecting,
			'rsa': self.directory_collected_keys + f'{id_origin}.pem'
		}
		self.log[ip_connecting] =  id_origin
		self.addRSA(id_origin, publicRSA)
		
		return 'Succesfully Added'
	
	def deleteIndex(self, id_origin, ip_connecting):
		'''
			(Index, string) -> (boolean)
			:delete the userid and ip found within the index and log JSON files
			
			@paramaters the userid exists within the index JSON file and the 
						connecting ip is associated with the account
			@returns boolean true if the userid was sucessfuly deleted
			@exception returns boolean false if any of the paramaters are not met
		'''
		ip_is_logged = self.lookupIndex(id_origin)
		
		#check to see that if the userid exists (the ip will exist if the userid does)
		if (ip_is_logged == ''):
			return '0'
		#check to see that the ip-address matches the logged user-id
		if (ip_is_logged != ip_connecting):
			return '0'
		
		self.deleteRSA(id_origin)
		self.index.pop(id_origin)
		self.log.pop(ip_connecting)
		
		return 'Succesfully Deleted'
	
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
			(Index) -> (string, string)
			:creates a randomized path through the server relay nodes
			
			@returns the first relay ip and a path of 4 node relays encrypted
		'''
		h = rsa.Handler()
		activeRelays = self.log.keys()
		
		ip_first = ''
		ip_previous = ''
		for i in range(0, 4):
			random_index = random.randrange(0, len(activeRelays))
			
			if i > 0:
				relay_ip = activeRelays.pop(random_index)
				relay_encrypted = h.encrypt(relay_ip, self.lookupRSA(ip = ip_previous))
			else:
				ip_first = activeRelays.pop(random_index)
				continue #skip to the begining of the loop
			
			pathway = pathway + ":" + relay_encrypted
			ip_previous = relay_ip
			
			if i == 3:
				activeExits = len(self.index['exit'])
				exitNode = random.randrange(0, activeExits)
				
				exit = self.index['exit'][exitNode]['ip']
		
		return (ip_first, f'^{pathway}^@{exit}@')
		
	def encryptData(self, id_origin, message):
		'''
			(Index, string, string) -> (string)
		'''
		rsa_temp = self.lookupRSA(id_origin)
		print(message)
		encrypted_message = self.handler_keys.encrypt(message, rsa_temp)
		#send the encrypted data with the RSA of the reciever
		return encrypted_message
	
	def formatMessage(self, id_target, message, id_origin):
		'''
			(Index, string, string, string) -> (string)
		'''
		message = self.encryptData(message)
		route = self.encryptPathwayAndExit()
		#send the next_ip and the bitstream readable only to the network
		return (route[0], f'#{message}#{route}<{id_origin}<>{id_target}>')
		
	def formatMessageShort(self, id_target, message, id_origin):
		'''
			(Index, string, string, string) -> (string)
		'''
		ip_target = self.lookupIndex(id_target)
		message = self.encryptData(id_origin, message)
		#send the next_ip (target-ip since it is simplified network msg)
		#and the message readable by the target
		return (ip_target, f'4:{message}~{id_origin}')
				
	def specialFunctionality(self, message, connectingAddress):
		'''
			(Node, string, string) -> (boolean, string)
			:auto-handles the generic requests made to the indexing function
			
			@returns boolean False indicating that messages will NOT be enqueued
					 to a queue
		'''
		#parse the simple bitsream requests
		try:
			p = basic.Parser(message)
			
			request = p.getRequest()
			data_first = p.getPrimaryData()
			data_second = p.getSecondaryData()
		except:
			return (False, '400') #error code 400: invalid request type
		
		print(self.index)
		
		#check all the standard network requests
		if (request == '0'):
			address = self.lookupIndex(data_first) #the first data is the userid
			return (False, address)
		elif (request == '1'):
			userid = self.lookupIP(data_first) #the first data is the ip
			return (False, userid)
		elif (request == '2'):
			data_third = p.getOtherData()[0]
			check = self.addIndex(data_first, data_second, data_third) #the first data is the userid, second is publicRSA, last is userip
			print(f'CHECK: {check}')
			return (False, check)
		elif (request == '3'):
			check = self.deleteIndex(data_first, data_second) #the first data is the userid, last is userip
			return (False, check)
		elif (request == '4'):
			data_third = p.getOtherData()[0]
			if (self.simplified_network):
				message = self.formatMessageShort(data_first, data_second, data_third) #for simplified networks
			else:
				message = self.formatMessage(data_firt, data_second, data_third) #for complex networks
			return (False, f'{message[0]}%{message[1]}')
		
		#the message has been handled by the generic implemented index requests
		return (False, '400') #error code 400: invalid request type
		