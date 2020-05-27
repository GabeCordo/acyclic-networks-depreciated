###############################
#		python imports
###############################
import socket
from time import sleep, time
from sys import getsizeof
from threading import Thread

###############################
#	   pynodetor imports
###############################
from pynodetor.encryption import rsa
from pynodetor.utils import errors, enums

###############################
#		   main code
###############################

class Node:
	def __init__(self, ip='', port=8075, ip_index=None, ip_backup=None,
				 directory_key_private=None, directory_key_public=None,
				 supports_encryption=True, supports_listening=True,
				 supports_monitoring=True, supports_backup_ip=True):
		'''
			(Node, string, int, boolean, DataTransfer) -> None
			
			:the class constructor for the primitive node type. All children
			 class are specific variations of the node class for specific
			 socket input and output manipulation on the mock 'tor' network.
			
			ip : the protocol adress of the current server
			port : the socket for incoming connections to the server
			
			** defaulted to end-to-end encryption enabled **
		'''
		##Generic Variables##
		self.ip = ip
		self.port = port
		self.queue = [] #all unhandled requests will go here
		self.supports_monitoring = supports_monitoring
		
		##Initialize the recieving socket##
		self.supports_listening = supports_listening
		self.incoming = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		##Initialize the encryption handler##
		self.supports_encryption = supports_encryption
		self.handler_keys = rsa.Handler(directory_key_private, directory_key_public)
		
		##Settup connection to an indexing/logging server##
		self.ip_index = ip_index
		
		self.supports_backup_ip = supports_backup_ip
		self.ip_backup = ip_backup
		
		self.thread_one = Thread(target=self.listen, args=())
		self.thread_two = Thread(target=self.monitor, args=())
	
	def getIp(self):
		'''
			(Node) -> (string)
			:the getter function for the ip binded to the Node Class
			
			@returns the ip of the server the socket is binded to.
		'''
		return self.ip
	
	def isListening(self):
		'''
			(Node) -> (boolean)
			:the getter function for whether accepting incoming traffic is
			 toggled
			
			@returns whether the socket is currently listening.
		'''
		return self.supports_listening
		
	def isEncrypted(self):
		'''
			(Node) -> (boolean)
			:the getter function for whether encryption is toggled
			
			@returns whether the node allows for end-to-end encryption
		'''
		return self.supports_encryption
	
	def isMonitoring(self):
		'''
			(Node) -> (boolean)
			:the getter function for whether the queue monitor is damianzied
			
			@returns a boolean value representing whether the montior is toggled
		'''
		return self.supports_monitoring
	
	def specialFunctionality(self, message, address):
		'''
			(string, string) -> (boolean, string)
			:child classes can overide this function to offer special functionality
			 to the listening aspect of the server
			
			@returns a boolean value representing whether to enqueue message
		'''
		return (True, '0') #by default we wan't it to queue all the requests
	
	def listen(self):
		'''
			(Node, int) -> None
			:listens to all incoming traffic to the server node.
			
			@returns nothing.
			@exception will not queue any incoming messages that are over
					   1024 bites long to enforce maximum runtime of string
					   parsing.
					
			**despite not returning anything, all incoming messages
			 are checked and then enqued on the node to be processed.**
		'''
		self.incoming.bind((self.ip, self.port))
		self.incoming.listen(10)
		
		try:
			while True:
				c, addr = self.incoming.accept()
				
				print(f'Console: Received connection from {addr}') #console logging
				
				#send whether the node supports end-to-end encryption
				if (self.supports_encryption == True):
					pre_message = self.handler_keys.getPublicKey()
				else:
					pre_message = b'None'
				c.send(pre_message) #send the encryption key or None indiciating it's disabled
				
				time_first = time() #start timing the transfer time according to latency
				
				if (self.supports_encryption == True):
					#receive the connectors public RSA key
					publicRSA = c.recv(1024)
					
					print(f'Console: Recieved RSA: {publicRSA}') #console logging
					
				time_diff = time() - time_first #measure the latency time to compensate for when sending data 
				
				#receive the cypher text from the connector
				i = 0
				time_warning = time() #keep track of the start (we want to avoid going over ~10 seconds)
				cyphertexts = [ c.recv(1024) ]
				
				#start receiving data from the sending socket
				while (cyphertexts[i] != b'<<'): #loop until the terminating operator is reached
					sleep(time_diff)
					cyphertexts.append(c.recv(1024))
					#add the time needed to append the new message
					time_warning = time_warning + time()
					if (time_warning > 10.0):
						raise TimeoutError('Console: We have exceeded a 10 second data transfer')
					i+=1
				cyphertexts.pop() #remove the null terminating character
				
				print(f'Console: Received cyphertext') #console logging
				
				#we want to decrypt the message only if encryption is enabled otherwise it is
				#in plain-text and decrypting it will raise an error
				if (self.supports_encryption == True):
					#we need to individualy decrypt each message and then join it
					for i in range(0, len(cyphertexts)):
						cyphertexts[i] = self.handler_keys.decrypt(cyphertexts[i]) #decrypt the cypher text and place it into a temp holder
						print(f'Console: added {cyphertexts[i]}')
				else:
					#we need to individualy decode the utf-8 bitsream into plain text
					for i in range(0, len(cyphertexts)):
						cyphertexts[i] = cyphertexts[i].decode()
				
				message = ''.join(cyphertexts)
				
				print(f'Console: Received message: {message}') #console logging
				
				#allow child classes to manipulate the message
				data_processed = self.specialFunctionality(message, addr[0])

				#return the data to the user
				if (data_processed[1] != ''):
					if (self.supports_encryption == True):
						data_encoded = self.handler_keys.encrypt(data_processed[1], publicRSA)
					else:
						data_encoded = bytes(data_processed[1], 'utf-8')
					print(f'Node: sent response {data_encoded}') #console logging
					c.send(data_encoded)
				
				#append to the message queue if required for further functionality
				if (data_processed[0]):
					self.queue.append(message)
					
				#close the connection with the connector
				c.close()
		except Exception as e:
			print(f'Console: ERRORED OUT {e}')
	def close(self):
		'''
			(Node) -> None
			:close the socket listening for incoming connections.
		'''
		#make sure the listening port is open in the first place before closing
		#the socket otherwise it will throw an error.
		if (self.supports_listening == False):
			#ensure the socket is closed
			self.incoming.close()
	
	def send(self, ip_target, message='', port=''):
			'''
				(Node, int, message) -> (string)
				:sends a bitsream to another Node.
				
				ip_target : the ip-adress of the receving node
				message : the bitsream to send to the node
				
				@returns a response code in the form of a strins from the server.
				@exception returns an empty string if there was a failure.
			'''
			try:
				outgoing = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				
				#if we arn't send a port to send the message to, assume its the same as
				#the one given upon class declaration (option: send to a diff network)
				if (port == ''):
					port = self.port
				outgoing.connect((ip_target, port)) #all outgoing requests are sent on port 8075
				
				#if we leave the string empty we are asking for a simple ping of the listening
				#server so if we establish connection return '1' and end everything else
				if (message == ''):
					return '1'
				
				time_first = time() #start timing the transfer time according to latency 
				
				received_rsa_public = outgoing.recv(1024).decode()
				print(f'Console: Received public_rsa {received_rsa_public}') #console logging
				
				time_diff = time() - time_first #measure the latency time to compensate for when sending data 
				
				key_pub_ours = self.handler_keys.getPublicKey()
				if (received_rsa_public != 'None'):
					outgoing.send(key_pub_ours) #send public key for any responses
				
				
				message_lst = []
				permited_char_len = 100 #the max number of chars allowed per bitstream (RSA maximum)
				
				#prepare the message we are going to send to the 
				if(received_rsa_public != 'None'):
					#if encryption is enabled, cypher it with the recieved public rsa
					#we need to make sure the byte size of the string being encrypted does not grow > than 250
					remaining_chars = permited_char_len
					
					while ((len(message) - len(message_lst)*permited_char_len) > permited_char_len): #repeat untill the len is less than 150 chars
						#for visibility we will throw this into temp vars
						beggining = remaining_chars - permited_char_len
						end = remaining_chars
						
						#encrypt and append to the list of message segments to send that are encrypted
						temp = self.handler_keys.encrypt(message[beggining:end], received_rsa_public)
						message_lst.append(temp)
						
						#append the number of chars that remain within the message
						remaining_chars+=permited_char_len
					
					#append the final part of the message to the list
					beggining = remaining_chars - permited_char_len
					temp = self.handler_keys.encrypt(message[beggining:], received_rsa_public)
					message_lst.append(temp)
						
				else:
					message_lst.append(bytes(message, 'utf-8'))
				
				message_lst.append(b'<<') #add the message transfer terminator
				
				print(f'Console: Done preparing message {message_lst}') #console logging
				
				#send the encrypted message to the listening node, we don't encode this into utf-8 as the cyphered text will
				#already be in this form, and won't be able to be sent
				for message_segment in message_lst:
					sleep(time_diff)
					outgoing.send(message_segment)
					
				print('Console: Sent message') #console logging
				
				#we are going to receive a response code back from the user after this possibly indicating some status
				#code or will 'spit out' some sort of data associated with the request
				response_cyphered = outgoing.recv(1024)
				if(received_rsa_public != 'None' and response_cyphered != b''):
					print(f'Console: Recieved cypher: {response_cyphered}')
					response = self.handler_keys.decrypt(response_cyphered)
				else:
					response = response_cyphered.decode()
				
				print(f'Console: Received response: {response}') #console logging
				
				#if we receive a status code of '0' that means something went wrong
				if (response == '400'):
					#if there is default to returning an empty string
					outgoing.close()
					return 'Error 400: Bad Resquest'
				else:
					#the bitsream was successfuly sent, we received usfull information from
					#the server we may need to process (it might be a response)
					outgoing.close()
					return response
			except Exception as e:
				
				print(f'Console: Experienced Error {e}') #debugging
				
				#we need to check that the ip_target is not self.ip_backup to avoid going into a recursive infinite loop
				if (self.supports_backup_ip != None and ip_target != self.ip_backup):
					self.send(self.ip_backup, message)
				else:
					outgoing.close()
					return e
	
	def sizeOfQueue(self):
		'''
			(Node) -> (int)
			@returns the size of the queued messages
		'''
		return len(self.queue)
	
	def deQueue(self):
		'''
			(Node) -> (string)
			:retreives the enqueued messages that have been retreived by the
			 open port on the node.
			
			@returns a string of max bit-length 1024
			@exception returns an empty string if the queue is empty
		'''
		length_queue = len(self.queue)
		if ( length_queue > 0 ):
			#return the first element in the queue acording to the first-in-first-out
			#principle enforced by the queue algorithm
			return self.queue.pop(0)
		else:
			#the queue was empty, no bitsreams have been received or approved for enqueing
			return ''
	
	def monitor(self):
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
		while (self.supports_listening == True):
			sleep(60)
			#account for the fact that during runtime, this might be closed midway
			try:
				#check to see if the queue size has increased by 1000 in 60 seconds
				#it should process quickly, this means its laggining/being flooded
				length_queue = len(self.queue)
				if ((length_queue - length_queue_previous) > 1000):
					#reset the queue to 60s before the current check
					self.queue = self.queue[:length_queue_previous+1]
				else:
					#account for the new queue additions
					length_queue_previous = length_queue
			except:
				#stop monitoring the queue
				return
	
	def settup(self):
		'''
			(Node) -> None
			:creates two new threads for the socket node on the network
			
			1) Thread One : Receives and sorts all incoming bitsream traffic
			2) Thread Two : Monitors the enqueded bitsreams for overflow/flooding
			
			** settup end-to-end encryption keys for the socket node **
		'''
		if (self.supports_listening == True):
			##settup and start the incoming socket##
			self.thread_one.setDaemon(True) # Daemonize thread (run in background)
			self.thread_one.start()
		
		if (self.supports_monitoring == True):
			##settup and start the queue monitor##  
			self.thread_two.setDaemon(True) # Daemonize thread (run in background)
			self.thread_two.start()
		
		##settup the end-to-end encryption keys##
		#will generate a new key-set when the server is started
		self.handler_keys.generateKeySet()
		
	def isThreadOneRuning(self):
		'''
			(Node) -> (boolean)
		'''
		return self.thread_one.is_alive()
	
	def closeThreadOne(self):
		'''
			(Node) -> None
		'''
		self.thread_one._Thread_stop()
			
	def isThreadTwoRunning(self):
		'''
			(Node) -> (boolean)
		'''
		return self.thread_two.is_alive()
		
	def closeThreadTwo(self):
		'''
			(Node) -> None
		'''
		self.thread_two._Thread_stop()
		
	def __del__(self):
		self.close()
		print('Console: the node has been closed.')