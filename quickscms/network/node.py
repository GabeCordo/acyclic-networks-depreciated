###############################
#		python imports
###############################

import socket
from sys import path
from time import sleep, time
from threading import Thread

###############################
#	   quickscms imports
###############################

from quickscms.crypto import rsa
from quickscms.timing.stopwatch import StopWatch
from quickscms.timing.timer import Timer
from quickscms.types import alias, static, dynamic, errors, enums, containers
from quickscms.utils import logging

###############################
#		   constants
###############################

PARAM_EMPTY_PORT = ''
PARAM_PERMITTED_CHAR_LEN = 100 #the max number of chars allowed per bitstream (RSA maximum)

REQUEST_BYTE_SIZE = 1024
REQUEST_TIMEOUT = 5.0

QUEUE_MONITOR_SCANNER_DELAY = 60
QUEUE_MONITOR_MAX_GROWTH = 1000

SCHEDULER_PRECISION = 3

QUEUE_DEFAULT_ITEM = ''
QUEUE_EMPTY = 0

###############################
#		   main code
###############################

class Node:
	def __init__(self, routine=None, container_addresses=None, container_paths=None, container_customizations=None):
		'''
			(Node, Addresses, Paths, Customizations) -> None
			
			:the class constructor for the primitive node type. All children
			 class are specific variations of the node class for specific
			 socket input and output manipulation on the mock 'tor' network.
			
			!the node class uses containers to store huge amounts of variables
			 for better customization, reusability, and to make code cleaner
			
				L-> all wrapper classes found under utils/containers
			
			** defaulted to end-to-end encryption enabled **
		'''
		self.routine = routine
		## we can either have a routine or manually defined containers, NOT both)
		containers_defined = ((container_addresses != None) and (container_paths != None) and (container_customizations != None))
		routine_defined = (routine != None)
		if (not (routine_defined or containers_defined) and ((not routine_defined) or (not containers_defined)) ):
			raise errors.ContainersLinkageFailed

		##Imported Containers##
		if (not routine):
			## import the container wrappers manually ##
			self.container_addresses = container_addresses
			self.container_paths = container_paths
			self.container_customizations = container_customizations
		else:
			## use the predefined config.yaml file linked to the config.py ##
			self.container_addresses = routine.cast_to_container_addresses()
			self.container_paths = routine.cast_to_container_paths()
			self.container_customizations = routine.cast_to_container_customizations()
		
		##Generic Variables##
		self.queue = [] #all unhandled requests will go here
		
		##Initialize the receiving socket##
		self.incoming = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		##Initialize the encryption handler##
		self.handler_keys = rsa.Handler(container_paths.directory_key_private, container_paths.directory_key_public)
		
		##Settup logging file for connection speed data
		logging.Logger(container_paths.directory_file_logging, container_customizations.supports_console_cout)
		
		##Define a placeholder for a timer##
		self.event_scheduler = None

		#these threads will need to be visible to a grouping of functions in the
		#class so we are throwing it in the constructor
		self.thread_one = Thread(target=self.listen, args=())
		self.thread_three = Thread(target=self.scheduler, args=())
		
		#a routine will need to override the default functions#
		self.thread_two = None
		if (routine == None):
			self.thread_two = Thread(target=self.monitor, args=())
		else:
			self.thread_two = Thread(target=routine.func_switch['qmf'](), args=())
	
	def getIp(self):
		'''
			(Node) -> (string)
			:the getter function for the ip binded to the Node Class
			
			@returns the ip of the server the socket is binded to.
		'''
		return self.container_addresses.ip
	
	def isListening(self):
		'''
			(Node) -> (boolean)
			:the getter function for whether accepting incoming traffic is
			 toggled
			
			@returns whether the socket is currently listening.
		'''
		return self.container_customizations.supports_listening
		
	def isEncrypted(self):
		'''
			(Node) -> (boolean)

			:the getter function for whether encryption is toggled
			
			@returns whether the node allows for end-to-end encryption
		'''
		return self.container_customizations.supports_encryption
	
	def isMonitoring(self):
		'''
			(Node) -> (boolean)
			:the getter function for whether the queue monitor is daemonize
			
			@returns a boolean value representing whether the monitor is toggled
		'''
		return self.container_customizations.supports_monitoring
	
	def specialFunctionality(self, message: str, address: str) -> list[bool, str]:
		'''
			(string, string) -> (boolean, string)
			:child classes can overide this function to offer special functionality
			 to the listening aspect of the server
			
			@returns a boolean value representing whether to enqueue message
		'''
		return (True, '0') #by default we want it to queue all the requests
	
	def specialFunctionalityError(self, status: str) -> enums.ReturnCode:
		'''
			(string, string) -> (string)
			:child classes can overide this function to offer special functionality
			 to processing and re-writting the errors processed by the node
			
			@returns a string representing a processed error code
		'''
		return (status)
	
	def listen(self) -> None:
		'''
			(Node, int) -> None
			:listens to all incoming traffic to the server node.
			
			@returns nothing.
			@exception will not queue any incoming messages that are over
					   1024 bites long to enforce maximum runtime of string
					   parsing.
					
			**despite not returning anything, all incoming messages
			 are checked and then enqueued on the node to be processed.**
		'''
		self.incoming.bind((self.container_addresses.ip, self.container_addresses.port))
		self.incoming.listen(10)
		
		while True:
			
			c, addr = self.incoming.accept()
			print(f'Console: Received connection from {addr}') #console logging
			
			optimizer = StopWatch(4) #we will use this to capture time between data captures to offer the best latency
			print("Set Optimizer" + str(optimizer))
			
			try:
				
				#send whether the node supports end-to-end encryption
				if (self.container_customizations.supports_encryption == True):
					pre_message = self.handler_keys.getPublicKey()
				else:
					pre_message = b'None'
				optimizer.lap()
				c.send(pre_message) ##send the encryption key or None indiciating it's disabled
				optimizer.lap()
				
				if (self.container_customizations.supports_encryption == True):
					#receive the connectors public RSA key
					publicRSA = c.recv(REQUEST_BYTE_SIZE)
				
				print(f'Console: Received publicRSA') #console logging
				print(publicRSA) #debuging
				
				#receive the cypher text from the connector
				time_warning = time() #keep track of the start (we want to avoid going over ~10 seconds)
				
				optimizer.lap() #start timing the transfer time according to latency
				cyphertexts = [c.recv(REQUEST_BYTE_SIZE)]
				optimizer.lap() #measure the latency time to compensate for when sending data
				print(f'Console: Time difference - {optimizer.getLog()}')
				i = 0
				
				delay = optimizer.getShortestLap()
				#start receiving data from the sending socket
				while (cyphertexts[i] != b'<<'): #loop until the terminating operator is reached
				
					sleep(delay)
					cyphertexts.append(c.recv(REQUEST_BYTE_SIZE))
					
					#ensure data collection has not exceeded 5 seconds
					if ((time() - time_warning) > REQUEST_TIMEOUT):
						raise TimeoutError('Data Transfer Exceeded 5 seconds')
					i+=1
				
				cyphertexts.pop() #remove the null terminating character
				
				print(f'Console: Received cyphertext') #console logging
				
				#we want to decrypt the message only if encryption is enabled otherwise it is
				#in plain-text and decrypting it will raise an error
				if (self.container_customizations.supports_encryption == True):
					#we need to individually decrypt each message and then join it
					for i in range(0, len(cyphertexts)):
						cyphertexts[i] = self.handler_keys.decrypt(cyphertexts[i]) #decrypt the cypher text and place it into a temp holder
				else:
					#we need to individually decode the utf-8 bitsream into plain text
					for i in range(0, len(cyphertexts)):
						cyphertexts[i] = cyphertexts[i].decode()
					
				message = ''.join(cyphertexts)
				
				#allow child classes to manipulate the message
				data_processed = None
				if (not self.routine):
					data_processed = self.specialFunctionality(message, addr[0])
				else:
					data_processed = self.routine.func_switch['rtpf']()
				
				print(f'Console: proccessed data') #console logging
				print(data_processed) #debuging
				
				#send the response code that will alert the sender whether to listen for future
				#response data associated with the request sent to the "server"
				c.send(data_processed[1].encode())
				
				#return the data to the user
				if (data_processed[1] == '1'):
					
					data_processed_lst = []
					permitted_char_len = 100 #the max number of chars allowed per bitstream (RSA maximum)
					
					#prepare the message we are going to send to the 
					if(self.supports_encryption == True):
						
						#if encryption is enabled, cypher it with the received public rsa
						#we need to make sure the byte size of the string being encrypted does not grow > than 250
						remaining_chars = permitted_char_len
						
						while ((len(data_processed[1]) - len(data_processed_lst)*permitted_char_len) > permitted_char_len): #repeat until the len is less than 150 chars
							#for visibility we will throw this into temp vars
							beggining = remaining_chars - permitted_char_len
							end = remaining_chars
							
							#encrypt and append to the list of message segments to send that are encrypted
							temp = self.handler_keys.encrypt(data_processed[1][beggining:end], publicRSA)
							data_processed_lst.append(temp)
							
							#append the number of chars that remain within the message
							remaining_chars+=permitted_char_len
						
						#append the final part of the message to the list
						beggining = remaining_chars - permitted_char_len
						temp = self.handler_keys.encrypt(data_processed[1][beggining:], publicRSA)
						data_processed_lst.append(temp)
							
					else:
						
						data_processed_lst.append(bytes(data_processed[1], 'utf-8'))
					
					data_processed_lst.append(b'<<') #add the message transfer terminator
					
					print(f'Console: finished preparing response') #console logging
					print(data_processed_lst) #debugging
					
					delay = optimizer.getLongestLap()
					#send the encrypted message to the listening node, we don't encode this into utf-8 as the cyphered text will
					#already be in this form, and won't be able to be sent
					for data_segment in data_processed_lst:
						sleep(delay)
						c.send(data_segment)
						
					print(f'Console: sent response') #console logging
					
				#append to the message queue if required for further functionality
				if (data_processed[0]):
					self.queue.append(message)
				
			except Exception as e:
				proccessed_error = self.specialFunctionalityError(e)
				print(f'Console: There was a problem during execution ({proccessed_error})')
			
			#close the connection with the connector
			c.close()

	def close(self) -> None:
		'''
			(Node) -> None
			:close the socket listening for incoming connections.
		'''
		#make sure the listening port is open in the first place before closing
		#the socket otherwise it will throw an error.
		if (self.container_customizations.supports_listening == False):
			#ensure the socket is closed
			self.incoming.close()
	
	def send(self, ip_target: int, message: enums.RequestCode, port: str) -> enums.ReturnCode:
			'''
				(Node, int, message) -> (string)
				:sends a bitsream to another Node.
				
				ip_target : the ip-address of the receiving node
				message : the bitsream to send to the node
				
				@returns a response code in the form of a strins from the server.
				@exception returns an empty string if there was a failure.
			'''
			try:
				outgoing = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				
				#if we aren't send a port to send the message to, assume its the same as
				#the one given upon class declaration (option: send to a diff network)
				if (port == PARAM_EMPTY_PORT):
					port = self.port
				
				optimizer = StopWatch(6) #we will use this to capture time between data captures to offer the best latency
				outgoing.connect((ip_target, port)) #all outgoing requests are sent on port 8075
				
				#if we leave the string empty we are asking for a simple ping of the listening
				#server so if we establish connection return '1' and end everything else
				if (message == enums.ReturnCode.PING_SERVER):
					return enums.ReturnCode.PING_SERVER
				
				optimizer.lap()
				received_rsa_public = outgoing.recv(REQUEST_BYTE_SIZE).decode()
				optimizer.lap()
				
				key_pub_ours = self.handler_keys.getPublicKey()
				if (received_rsa_public != 'None'):
					outgoing.send(key_pub_ours) #send public key for any responses
				
				message_lst = []
				print(f'Console: Time difference - {optimizer.getLog()}')
				
				#prepare the message we are going to send to the
				if(received_rsa_public != 'None'):
					#if encryption is enabled, cypher it with the received public rsa
					#we need to make sure the byte size of the string being encrypted does not grow > than 250
					remaining_chars = PARAM_PERMITTED_CHAR_LEN
					
					while ((len(message) - len(message_lst)*PARAM_PERMITTED_CHAR_LEN) > PARAM_PERMITTED_CHAR_LEN): #repeat untill the len is less than 150 chars
						#for visibility we will throw this into temp vars
						beggining = remaining_chars - PARAM_PERMITTED_CHAR_LEN
						end = remaining_chars
						
						#encrypt and append to the list of message segments to send that are encrypted
						temp = self.handler_keys.encrypt(message[beggining:end], received_rsa_public)
						message_lst.append(temp)
						
						#append the number of chars that remain within the message
						remaining_chars+=PARAM_PERMITTED_CHAR_LEN
					
					#append the final part of the message to the list
					beggining = remaining_chars - PARAM_PERMITTED_CHAR_LEN
					temp = self.handler_keys.encrypt(message[beggining:], received_rsa_public)
					message_lst.append(temp)
						
				else:
					message_lst.append(bytes(message, 'utf-8'))
				
				message_lst.append(b'<<') #add the message transfer terminator
				
				print(f'Console: prepared message') #console logging
				
				delay = optimizer.getLongestLap()
				#send the encrypted message to the listening node, we don't encode this into utf-8 as the cyphered text will
				#already be in this form, and won't be able to be sent
				for message_segment in message_lst:
					sleep(delay)
					outgoing.send(message_segment)
					
				print(f'Console: Sent message') #console logging
				
				#we are going to receive a response code back from the user after this possibly indicating some status
				#code or will 'spit out' some sort of data associated with the request
				
				response_code = outgoing.recv(REQUEST_BYTE_SIZE)
				
				if (response_code == b'1'):
				
					#receive the cypher text from the connector
					time_warning = time() #keep track of the start (we want to avoid going over ~10 seconds)
					
					cyphertexts = [outgoing.recv(REQUEST_BYTE_SIZE)]
					i = 0

					delay = optimizer.getShortestLap()
					#start receiving data from the sending socket
					while (cyphertexts[i] != b'<<'): #loop until the terminating operator is reached
					
						sleep(delay)
						cyphertexts.append(outgoing.recv(REQUEST_BYTE_SIZE))
						
						#ensure data collection has not exceeded 5 seconds
						if ((time() - time_warning) > REQUEST_TIMEOUT):
							raise TimeoutError('Data Transfer Exceeded 5 seconds')
						
						i+=1
						
					cyphertexts.pop() #remove the null terminating character
					
					print(f'Console: Received Cyphertext') #console logging
					
					#we want to decrypt the message only if encryption is enabled otherwise it is
					#in plain-text and decrypting it will raise an error
					if (received_rsa_public != 'None'):
						#we need to individually decrypt each message and then join it
						for i in range(0, len(cyphertexts)):
							cyphertexts[i] = self.handler_keys.decrypt(cyphertexts[i]) #decrypt the cypher text and place it into a temp holder
					else:
						#we need to individually decode the utf-8 bitsream into plain text
						for i in range(0, len(cyphertexts)):
							cyphertexts[i] = cyphertexts[i].decode()
						
					response = ''.join(cyphertexts) #join the decoded cyphertexts
					
					print(f'Console: Formated cypher to plain text') #console logging
					
					#if we receive a status code of '0' that means something went wrong
					if (response == '400' or response == None):
						#if there is default to returning an empty string
						outgoing.close()
						return 'Error 400: Bad Resquest'
					else:
						#the bitsream was successfully sent, we received usefully information from
						#the server we may need to process (it might be a response)
						outgoing.close()
						return response
			
				else:
					
					if (response_code == b'0'):
						print(f'Console: (Code 0) General Failure')
					elif (response_code == b'2'):
						print(f'Console: (Code 2) Transfer Failure')
						
				outgoing.close()
				return None
			
			except Exception as e:
				
				print(f'Console: Experienced Error {e}') #debugging
				
				#we need to check that the ip_target is not self.ip_backup to avoid going into a recursive infinite loop
				if (self.container_customizations.supports_backup_ip != False and ip_target != self.container_addresses.ip_backup):
					self.send(self.container_addresses.ip_backup, message)
				else:
					outgoing.close()
					return e
	
	def sizeOfQueue(self) -> (int):
		'''
			(Node) -> (int)
			@returns the size of the queued messages
		'''
		if (self.queue != None):
			return len(self.queue)
		return QUEUE_EMPTY
	
	def deQueue(self) -> (str):
		'''
			(Node) -> (string)
			:retrieves the enqueued messages that have been retrieved by the
			 open port on the node.
			
			@returns a string of max bit-length 1024
			@exception returns an empty string if the queue is empty
		'''
		length_queue = len(self.queue)
		if (length_queue > 0):
			#return the first element in the queue according to the first-in-first-out
			#principle enforced by the queue algorithm
			return self.queue.pop(0)
		else:
			#the queue was empty, no bitsreams have been received or approved for enqueuing
			return QUEUE_DEFAULT_ITEM
	
	def monitor(self) -> None:
		'''
			(Node) -> None
			
			:the monitor function is an active listener on the enqueued messages
			 looking for potential spamming or overflows
			
			1) Check for garbage messages near the end of the queue
			
			**Queues only near the end of the queue will be effect to ensure it
			  does not interfere with the any systems working to manipulate/handle
			  elements at the front of the queue during runtime AVOIDING MEMORY RACES **
		'''
		length_queue_previous = 0
		#runs throughout the lifetime of the incoming socket
		while (self.container_customizations.supports_listening == True):
			sleep(QUEUE_MONITOR_SCANNER_DELAY)
			#account for the fact that during runtime, this might be closed midway
			try:
				#check to see if the queue size has increased by N in N(s) seconds
				#it should process quickly, this means its laggining/being flooded
				length_queue = len(self.queue)
				if ((length_queue - length_queue_previous) > QUEUE_MONITOR_MAX_GROWTH):
					#reset the queue to 60s before the current check
					self.queue = self.queue[:length_queue_previous+1]
				else:
					#account for the new queue additions
					length_queue_previous = length_queue
			except Exception:
				#stop monitoring the queue
				return
	
	def scheduler(self) -> None:
		'''
			(Node) -> None
			:if a event scheduler has not already been created, we need to
			 define one on the self.event_scheduler placeholder
		'''
		#check to see that a scheduler has not already been created.
		if (not self.event_scheduler):
			self.event_scheduler = Timer(SCHEDULER_PRECISION)

	def settup(self):
		'''
			(Node) -> None
			:creates two new threads for the socket node on the network
			
			1) Thread One : Receives and sorts all incoming bitsream traffic
			2) Thread Two : Monitors the enqueued bitsreams for overflow/flooding
			3) Thread Three : Monitors events that we may want to perform on a Node
			
			** settup end-to-end encryption keys for the socket node **
		'''
		if (self.container_customizations.supports_listening == True):
			##settup and start the incoming socket##
			if (self.thread_one != None):
				self.thread_one.setDaemon(True) # Daemonize thread (run in background)
				self.thread_one.start()
			elif (self.container_customizations.supports_console_cout):
				print("Warning: Thread one failed to daemonize and run.")
			
		
		if (self.container_customizations.supports_monitoring == True):
			##settup and start the queue monitor##  
			if (self.thread_two != None):
				self.thread_two.setDaemon(True) # Daemonize thread (run in background)
				self.thread_two.start()
			elif (self.container_customizations.supports_console_cout):
				print("Warning: Thread two failed to daemonize and run.")

		if (self.container_customizations.supports_scheduling_events == True):
			##settup and start scheduled events##
			if (self.thread_three != None):
				self.thread_three.setDaemon(True)
				self.thread_three.start()
			elif (self.container_customizations.supports_console_cout):
				print("Warning: Thread three failed to daemonize and run.")

		##settup the end-to-end encryption keys##
		#will generate a new key-set when the server is started
		self.handler_keys.generateKeySet()			
		
	def isThreadOneRuning(self) -> bool:
		'''
			(Node) -> (boolean)
		'''
		if (self.thread_one != None):
			return self.thread_one.is_alive()
	
	def closeThreadOne(self) -> None:
		'''
			(Node) -> None
		'''
		if (self.thread_one != None):
			self.thread_one._Thread_stop()
			
	def isThreadTwoRunning(self) -> bool:
		'''
			(Node) -> (boolean)
		'''
		if (self.thread_two != None):
			return self.thread_two.is_alive()
		
	def closeThreadTwo(self) -> None:
		'''
			(Node) -> None
		'''
		if (self.thread_two != None):
			self.thread_two._Thread_stop()
	
	def isThreadThreeRunning(self) -> bool:
		'''
			(Node) -> (boolean)
		'''
		if (self.thread_three != None):
			return self.thread_three.is_alive()
		
	def closeThreadThree(self) -> None:
		'''
			(Node) -> None
		'''
		if (self.thread_three != None):
			self.thread_three._Thread_stop()

	def __repr__(self) -> str:
		'''
		'''
		return f'Node(ip:{self.container_addresses.ip}, port:{self.container_addresses.port}, queue-len:{len(self.queue)})'

	def __eq__(self, other) -> bool:
		'''
		'''
		if (other == None):
			return False
		if (type(other) != type(Node)):
			return False
		return self.container_customizations == other.container_customizations

	def __del__(self) -> None:
		'''
		'''
		self.close()
		if (self.container_customizations.supports_console_cout):
			print('Console: the node has been closed.')