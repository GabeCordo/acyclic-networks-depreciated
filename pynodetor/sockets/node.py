###############################
#		python imports
###############################
import socket, time
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
	def __init__(self, ip, directoryKeyPrivate=None, directoryKeyPublic=None, indexIp=None, encryption=True, listening=True, monitoring=True):
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
		self.queue = [] #all unhandled requests will go here
		self.monitoring = monitoring
		
		##Initialize the recieving socket##
		self.listening = listening
		self.incoming = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		
		##Initialize the encryption handler##
		self.encryption = encryption
		self.encryptionHandler = rsa.Handler(directoryKeyPrivate, directoryKeyPublic)
		
		##Settup connection to an indexing/logging server##
		self.indexIP = indexIP
	
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
		return self.listening
		
	def isEncrypted(self):
		'''
			(Node) -> (boolean)
			:the getter function for whether encryption is toggled
				
			@returns whether the node allows for end-to-end encryption
		'''
		return self.encryption
	
	def isMonitoring(self):
		'''
			(Node) -> (boolean)
			:the getter function for whether the queue monitor is damianzied
			
			@returns a boolean value representing whether the montior is toggled
		'''
		return self.monitoring
	
	def specialFunctionality(self):
		'''
			(string) -> (boolean)
			:child classes can overide this function to offer special functionality
			 to the listening aspect of the server
			
			@returns a boolean value representing whether to enqueue message
		'''
		return True #by default we wan't it to queue all the requests
	
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
		self.incoming.bind( (self.ip, 8074) )
		self.incoming.listen(10)
		while True:
			c, addr = self.incoming.accept()
			
			#send whether the node supports end-to-end encryption
			if (self.encryption == True):
				pre_message = self.encryptionHandler.getPublicKey()
			else:
				pre_message = 'None'
			c.send(bytes(pre_message, 'utf8'))
			
			if (self.encryption == True):
				#receive the connectors public RSA key
				publicRSA = c.recv(1024).decode()
			
			#receive the cypher text from the connector
			bitsream = c.recv(1024).decode()
			
			#ensure the bitsream isn't blank incase someone is trying to spam
			#the node program and overflow the queue 
			if (cyphertext != ''):
				if (self.encryption == True):
					message = self.encryptionHandler.decrypt(cyphertext) #decrypt the cypher text and place it into a temp holder
				else:
					message = bitsream
				#allow child classes to manipulate the message
				enqueue = self.specialFunctionality(message, addr)
				#append to the message queue if required for further functionality
				if (enqueue):
					self.queue.append( message )
				
			#close the connection with the connector
			c.close()

	def close(self):
		'''
			(Node) -> None
			:close the socket listening for incoming connections.
		'''
		#make sure the listening port is open in the first place before closing
		#the socket otherwise it will throw an error.
		if (self.listening == False):
			#ensure the socket is closed
			self.incoming.close()
	
	def send(self, ipOut, message):
			'''
				(Node, int, message) -> (string)
				:sends a bitsream to another Node.
				
				ipOut : the ip-adress of the receving node
				portOut : the listening port of the receving node
				message : the bitsream to send to the node
				
				@returns a response code in the form of a strins from the server.
				@exception returns an empty string if there was a failure.
			'''
			try:
				outgoing = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				outgoing.connect((ipOut, 8074)) #all outgoing requests are sent on port 8075
				
				publicRSA = outgoing.rec(1024).decode()
				if (publicRSA != 'None'):
					outgoing.send(bytes(self.encryptionHandler.getPublicKey(), 'utf8')) #send public key for any responses
				
				#ensure the node is not sending a message over a certain byte length
				#to avoid strenious or inefficient processing on the devs end
				if (len(message.encode('utf-8')) <= 1024):
					if(self.encryption == True):
						message_ready = self.encryptionHandler(message, publicRSA) #if encryption is enabled, cypher it with the recieved public rsa
					else:
						message_ready = message
					outgoing.send(bytes(message_ready, 'utf-8'))
				else:
					#if there is default to returning an empty string
					return ''
				
				if (self.encryption == True):
					received = outgoing.recv(1024).decode()
					#if we receive a status code of '0' that means something went wrong
					if (received == '0'):
						#if there is default to returning an empty string
						return ''
					else:
						#the bitsream was successfuly sent, we received usfull information from
						#the server we may need to process (it might be a response)
						return received
				else:
					return '1'
				
				outgoing.close()
			except:
				return '2'
	
	def sizeOfQueue(self):
		'''
			(Node) -> (int)
			@returns the size of the queued messages
		'''
		return len( self.queue )
	
	def deQueue(self):
		'''
			(Node) -> (string)
			:retreives the enqueued messages that have been retreived by the
			 open port on the node.
			
			@returns a string of max bit-length 1024
			@exception returns an empty string if the queue is empty
		'''
		length = len( self.queue )
		if ( length > 0 ):
			#return the first element in the queue acording to the first-in-first-out
			#principle enforced by the queue algorithm
			return self.queue[ 0 ]
			#reshape the queue to no-longer include the first element
			self.queue = self.queue[1:]
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
		sizeQueuePrevious = 0
		#runs throughout the lifetime of the incoming socket
		while ( self.listening == True ):
			time.sleep(60)
			#account for the fact that during runtime, this might be closed midway
			try:
				#check to see if the queue size has increased by 1000 in 60 seconds
				#it should process quickly, this means its laggining/being flooded
				sizeQueueCurrent = len( self.queue )
				if ( (sizeQueueCurrent - sizeQueuePrevious) > 1000 ):
					#reset the queue to 60s before the current check
					self.queue = self.queue[:sizeQueuePrevious+1]
				else:
					#account for the new queue additions
					sizeQueuePrevious = sizeQueueCurrent
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
		if (self.listening == True):
			##settup and start the incoming socket##
			threadOne = threading.Thread(target=self.listen, args=())
			threadOne.daemon = True # Daemonize thread (run in background)
			threadOne.start()  
		
		if (self.monitoring == True):
			##settup and start the queue monitor##  
			threadTwo = threading.Thread(target=self.monitor, args=())
			threadTwo.daemon = True # Daemonize thread (run in background)
			threadTwo.start()
		
		##settup the end-to-end encryption keys##
		#will generate a new key-set when the server is started
		encryptionHandler.generateKeySet()