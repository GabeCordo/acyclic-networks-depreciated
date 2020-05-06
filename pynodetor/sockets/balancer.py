###############################
#	   pynodetor imports
###############################
from pynodetor.bitstream import basic
from pynodetor.sockets.node import Node
from pynodetor.utils import linkerJSON, errors, enums

###############################
#		   main code
###############################
class NodeBalancer(Node, linkerJSON.Handler):
	def __init__(self, ip, port, directory_key_private, directory_key_public, directory_entry_nodes):
		'''(Balancer, list of strings) -> None
			:constuctor for the Balancer class takes a list of ip-addresses
			 representing the available entry Nodes.
		'''
		Node.__init__(self, ip, port, None, '', directory_key_private,
					  directory_key_public, True, True, False, False) #ecryption, listening, monitoring
		
		linkerJSON.Handler.__init__(self, directory_entry_nodes)
		
		self.nodes_entry = self.data[0]
		self.trackers = [0] * len(self.nodes_entry)
	
	def track(self, ip):
		'''(Balancer, string) -> (int)
			:find the number of times traffic has been re-directed to a specific
			 ip
			
			@returns an integer representing the number of re-directs
		'''
		index = self.nodes_entry.index(ip)
		return self.trackers[index]
		
	def redirect(self):
		'''(Balancer) -> (string)
			:find the entry node with the least re-directs and return it
			
			@returns a string of the ip-address with the least re-directs
		'''
		index = self.trackers.index(min( self.trackers ))
		self.trackers[index] = self.trackers[index] + 1
		return self.nodes_entry[index]
		
	def synatxValidator(self, message):
		'''(Balancer, string) -> None
			:validates whether the basic markup request is valid
			
			@returns nothing indicating it is valid
			@exception raises MismatchedSyntax() error if it is invalid
		'''
		check = basic.Parser(message)
	
	def specialFunctionality(self, message, connectingAddress):
		'''(Balancer, string, string) -> (boolean)
			:
		'''
		try:
			self.synatxValidator(message) #will throw an error if invalid (hence, using try/catch)
			entry = self.redirect()
			#if the syntax is valid and we have a new entry node, send the message into the network
			message_modified = message + f'/{connectingAddress}'
			self.send(entry, message_modified)
		except:
			print(f'Console: Received bad reciept from {connectingAddress}')
		
		#we always want this to return False, there is NO need to have any other functionality
		return False