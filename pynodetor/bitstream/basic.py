'''
	  INTERFACE FOR PARSING RAW BASIC SERVER BITSREAMS
		-          DO NOT MODIFY THIS FILE          -
		
	*** used for bitstream transfers with minimal (one-
		two elements of data on-top of the standard
		request, can be used by any node class: O(n) ***
'''

###############################
#	   pynodetor imports
###############################
from pynodetor.utils.errors import *

###############################
#		   main code
###############################
class Parser():
	
	def __init__(self, message=''):
		'''
			(Parser, string) -> None
			@description the constructor class for the simple parser
			
			@syntax (request):(primary_data)/(secondary_data)
						^			^				^
						0			1				2
				
			0: the action the server needs to preform on the data
			1: the most significant piece of data
			2: assisting data to the primary data
			
			@exception throws MismatchedSyntax() Error if given an
					   invalid message
		'''
		self.message = message
		
		self.request = ''
		self.data_primary = ''
		self.data_secondary = ''
		
		self.parse()
	
	def parse(self):
		'''
			(Parser) -> None
			:using indexing, parses the pieces of data into the class
			 variables
			
			@returns nothing to the main program but initializes the
					 class variables
			@exception if an incorrect syntax is provided, throws
					   MismatchedSyntax() Error
		'''
		try:
			request_seperator = self.message.index(':')
			data_seperator = self.message.index('/')
			#the request is from index 0 to the request seperator
			self.request = self.message[:request_seperator]
			#the first data is from the index after the index seperator to the data seperator
			self.data_primary = self.message[request_seperator+1:data_seperator]
			#the second data is from the index after the data seperator to the end of the bitsream
			self.data_secondary = self.message[data_seperator+1:]
		except:
			raise MismatchedSyntax()
		
	def getRequest(self):
		'''
			(Parser) -> (string)
			:the getter function for the messages request field
			
			@returns the request parsed from the message during initialization
			@exception returns an empty string if invalid syntax was provided
		'''
		return self.request
		
	def getPrimaryData(self):
		'''
			(Parser) -> (string)
			:the getter function for the messages primary data field
			
			@returns the primary data parsed from the message during initialization
			@exception returns an empty string if invalid syntax was provided
		'''
		return self.data_primary
		
	def getSecondaryData(self):
		'''
			(Parser) -> (string)
			:the getter function for the messages secondary data field
			
			@returns the secondary data parsed from the message during initialization
			@exception returns an empty string if invalid syntax was provided
		'''
		return self.data_secondary
		
	def __str__(self):
		'''
			(Parser) -> (string)
			@returns a string representation of the class variables in the proper
					 simple bitstream syntax
		'''
		return f'{self.request}:{self.data_primary}/{self.data_secondary}'
		
	def __repr__(self):
		'''
			(Parser) -> (string)
			@returns a string representation of the class type
		'''
		return f'Parser({message})'