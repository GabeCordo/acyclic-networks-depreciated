#####################################
#		   Python Imports
#####################################

from quickscms.bitstream import basic
from sys import path

#####################################
#		   Manakin Imports
#####################################

path.append('../')
from chaching import fileHandler

#####################################
#		 Node Queue Handler
#####################################

def handler(client):
	'''
		(NodeRelay) -> None
		This file will be incharge of distributing incoming messages to the proper
		whitelist, blacklist or pending text-files for the client
	'''
	
	fileHandler(directory)
	
	while True:
		
		if (client.sizeOfQueue() > 0):
			
			bitsream_received = client.deQueue()
			parser = basic.Parser(message_received)
			
			request = parser.getRequest()
			message_received = parser.getPrimaryData()
			message_sender = parser.getSecondaryData()
			
			if (request == '4'):
				pass
				#check if the sender is on the blacklist
				#we will discard the message if they are on it
		