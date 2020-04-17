#import pythons socket connection features
import socket

## Parent Class for Entry, Relay and Exit Nodes ##
# The Node class contains functionality shared by all entry, relay or exit nodes
# that will be needed on the mock-tor network for socket communication
class Node:
	
	def __init__(self, ip, portIn, _endToEnd=True):
		'''(Node, string, int) -> None
			:the class constructor for the primitive node type. All children class
			 are specific variations of the node class for specific socket input and
			 output manipulation on the mock 'tor' network.
			
			ip : the protocol adress of the current server
			port : the socket for incoming connections to the server
			endToEnd : defaulted to end-to-end encryption enabled
		'''
		##Generic Variables##
		self.ip = ip
		self.queue = []
		self._endToEnd = _endToEnd
		#initialize the incoming traffic socket when the class is created
		self.portIn = portIn
		self.listening = True
		self.incoming = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		self.listen()
	
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
		
	def isEncrypted(self):
		'''(Node) -> (boolean)
			@returns whether the socket supports end-to-end encryption.
		'''
		return self._endToEnd
	
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
			'''
			outgoing = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			outgoing.connect((ipOut, portOut))
		
			outgoing.send(bytes(message, 'utf-8'))

			received = outgoing.recv(1024).decode()
			if (received == '0'):
				return ''
				#Failed to send message to target
			else:
				return received
				#Message successfully sent

			outgoing.close()