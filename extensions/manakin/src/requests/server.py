#####################################
#		   Manakin Imports
#####################################

from chaching import fileHandler

#####################################
#		Server-Side Requests
#####################################

def lookupIndex(id_user):
	'''
		(string) -> (string)
		:format the data into a request accepted by the indexing server
		
		@returns a string in the format '0:(id)'
										 ^
								 request identifier
	'''
	return f'0:{id_user}'
def addIndex(id_user, key_public):
	'''
		(string, string) -> (string)
		:format the data into a request accepted by the indexing server
		
		@returns a string in the format '2:(id)/(rsa)'
										 ^
								 request identifier
	'''
	return f'2:{id_user}~{key_public}'
def deleteIndex(id_user):
	'''
		(string) -> (string)
		:format the data into a request accepted by the indexing server
		
		@returns a string in the format '3:(id)'
										 ^
								 request identifier
	'''
	return f'3:{id_user}'

def sendMessage(id_target, message):
	'''
		(string, string) -> (string)
		:format the data into a request accepted by the indexing server
		
		@returns a string in the format '4:(id)/(message)'
										 ^
								 request identifier
	'''
	return f'4:{id_target}~{message}'