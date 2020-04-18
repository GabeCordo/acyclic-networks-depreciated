#import pythons socket connection features
from threading import Thread
import socket, time

## Parent Class for Entry, Relay and Exit Nodes ##
# The Node class contains functionality shared by all entry, relay or exit nodes
# that will be needed on the mock-tor network for socket communication
class Node:
	
	def __init__(self, ip, portIn):
		'''(Node, string, int) -> None
			:the class constructor for the primitive node type. All children class
			 are specific variations of the node class for specific socket input and
			 output manipulation on the mock 'tor' network.
			
			ip : the protocol adress of the current server
			port : the socket for incoming connections to the server
			
			** defaulted to end-to-end encryption enabled **
		'''
		##Generic Variables##
		self.ip = ip
		self.portIn = portIn
		##List to store all received bitsreams for processing##
		self.queue = []
		##Initialize the recieving socket##
		self.listening = True
		self.incoming = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	
	def getIp(self):
		'''(Node) -> (string)
			@returns the ip of the server the socket is binded to.
		'''
		return self.ip
	
	def getPort(self):
		'''(Node) -> (string)
			@returns the port binded to watch all incoming traffic.
		'''
		return self.portIn
	
	def isListening(self):
		'''(Node) -> (boolean)
			@returns whether the socket is currently listening.
		'''
		return self.listening
	
	def listen(self):
		'''(Node, int) -> None
			:listens to all incoming traffic to the server node.
			
			[despite not returning anything, all incoming messages
			 are checked and then enqued on the node to be processed.]
			
			@returns nothing.
			@exception will not queue any incoming messages that are over
					   1024 bites long to enforce maximum runtime of string
					   parsing.
		'''
		self.incoming.bind( (self.ip, self.portIn) )
		self.incoming.listen(10)
		while True:
			c, addr = self.incoming.accept()
			message = c.recv(1024)
			#ensure the bitsream isn't blank incase someone is trying to spam
			#the node program and overflow the queue 
			if (message != ''):
				self.queue.append( message )
			c.close()

	def close(self):
		'''(Node) -> None
			close the socket listening for incoming connections.
		'''
		#make sure the listening port is open in the first place before closing
		#the socket otherwise it will throw an error.
		if (self.listening):
			#ensure the socket is closed
			self.incoming.close()
	
	def send(self, ipOut, portOut, message):
			'''(Node, int, message) -> (string)
				:sends a bitsream to another Node.
				
				ipOut : the ip-adress of the receving node
				portOut : the listening port of the receving node
				message : the bitsream to send to the node
				
				@returns a response code in the form of a string
						 from the server.
				@exception returns an empty string if there was a failure.
			'''
			outgoing = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			outgoing.connect((ipOut, portOut))
			
			#ensure the node is not sending a message over a certain byte length
			#to avoid strenious or inefficient processing on the devs end
			if (len(message.encode('utf-8')) <= 1024):
				outgoing.send(bytes(message, 'utf-8'))
			else:
				#if there is default to returning an empty string
				return ''
				
			received = outgoing.recv(1024).decode()
			#if we receive a status code of '0' that means something went wrong
			if (received == '0'):
				#if there is default to returning an empty string
				return ''
			else:
				#the bitsream was successfuly sent, we received usfull information from
				#the server we may need to process (it might be a response)
				return received
			
			outgoing.close()
	
	def sizeOfQueue(self):
		'''(Node) -> (int)
			@returns the size of the queued messages
		'''
		return len( self.queue )
	
	def deQueue(self):
		'''(Node) -> (string)
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
		'''(Node) -> None
			:the monitor function is an active listener on the enqueued messages
			 looking for potential spamming or overflows
			1) Check for garbage messages near the end of the queue
			
			**Queues only near the end of the queue will be effect to ensure it does
			  not interfere with the any systems working to manipulate/handle elements
			  at the front of the queue during runtime AVOIDING MEMORY RACES **
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
		'''(Node) -> None
			:creates two new threads for the socket node on the network
			1) Thread One : Receives and sorts all incoming bitsream traffic
			2) Thread Two : Monitors the enqueded bitsreams for overflow/flooding
		'''
		#settup and start the incoming socket
		threadOne = threading.Thread(target=self.listen)
		threadOne.daemon = True # Daemonize thread (run in background)
		threadOne.start()  
		#settup and start the queue monitor  
		threadTwo = threading.Thread(target=self.monitor)
		threadTwo.daemon = True # Daemonize thread (run in background)
		threadTwo.start()