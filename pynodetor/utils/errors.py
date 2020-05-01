##########################################
#			  Fatal Errors
##########################################

class NetworkNotConfigured(Exception):
	def __init__(self):
		Exception.__init__(self, f'Fatal Error: There was attempt to use a tor-network that is improperly configured.')

class UnauthorizedNetwork(Exception):
	def __init__(self):
		Exception.__init__(self, f'Fatal Error: There was attempt to attach a node that is not authorized to be apart of a network.')

##########################################
#		Generic Network Errors
##########################################

class IllegalRequest(Exception):
	def __init__(self, request):
		Exception.__init__(self, f'Generic Network Error: Illigal Request was provided to the node.')
		self.request = request
		
class CorruptedMessage(Exception):
	def __init__(self, message):
		Exception.__init__(self, f'Generic Network Error: The message can not be decoded by the userids public RSA.')
		self.message = message

##########################################
#		Security Network Errors
##########################################

class MissingRSAKey(Exception):
	def __init__(self):
		Exception.__init__(self, f'Security Network Error: There was an attempt to send a message to a target-id but the public RSA was missing and cannot be encoded.')
		
class UnkownFriendWarning(Exception):
	def __init__(self, userid):
		Exception.__init__(self, f'Security Network Error: There was an attempt to send a message to a target-id that has not been friended.')
		
class UnusualTraffic(Exception):
	def __init__(self, userid):
		Exception.__init__(self, f'Security Network Error: The local relay node received unusual traffic and was automaticly shut-down.')
		
class AuthenticationFailure(Exception):
	def __init__(self):
		Exception.__init__(self, f'Security Network Error: There was a mis-match in authenticator codes, access denied.')

##########################################
#		Connection Network Errors
##########################################

class TransferFailure(Exception):
	def __init__(self, ip):
		Exception.__init__(self, f'Connection Network Error: There was an attempt to send a bitsream to a non-responsive node.')
		self.transfer = ip
		
class NodeIncomingWarning(Exception):
	def __init__(self, transfer):
		Exception.__init__(self, f'Connection Network Warning: Incoming transfer(friend)-requests is toggled off.')
		self.transfer = transfer
		
class EndToEndOffWarning(Exception):
	def __init__(self):
		Exception.__init__(self, f'Connection Network Warning: End-toEnd encryption on this node is toggled off.')
		
##########################################
#		  Indexing Node Errors
##########################################

class CleanupFailure(Exception):
	def __init__(self, time):
		Exception.__init__(self, f'Indexing Node Error: There was an attempt to load the local index to the JSON file but an error occured.')
		self.time = time
		
class MissingIndex(Exception):
	def __init__(self, request):
		Exception.__init__(self, f'Indexing Node Error: There was an attempt to pull from JSON but the indexing file was missing.')
		self.request = request
		
##########################################
#		  Balancer Node Errors
##########################################

class TrafficOverloadError(Exception):
	def __init__(self):
		Exception.__init__(self, f'Balancer Node Error: As a result of an unusual amount of requests the Node has closed.')
		
##########################################
#	 	  Parsing/Markup Errors
##########################################

class MismatchedSyntax(Exception):
	def __init__(self):
		Exception.__init__(self, f'Parsing Error: There was an attempt to pass incorrect syntax to the parser.')