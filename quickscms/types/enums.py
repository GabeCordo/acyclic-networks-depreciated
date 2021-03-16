##########################################
#			python imports
##########################################

from enum import Enum

##########################################
#			  Node Enums
##########################################

#The type of relay nodes present within the tor network
class Nodes(Enum):
	NODE = 0
	ENTRY = 1
	RELAY = 2
	EXIT = 3
	INDEX = 4
	BALANCER = 5

#Whether the node has end-to-end encryption enabled
class Encrypted(Enum):
	DISABLED = 0
	ENABLED = 1
	
#whether the node is set to listen for incoming traffic by default
class Listening(Enum):
	DISABLED = 0
	ENABLED = 1

#this is left for (future) cryptographic implementations
class Encryption(Enum):
	RSA = 0

#DEPRECIATED - this is used as a switch variable for the processing function
class DataTransfer(Enum):
	BASIC = 0
	ADVANCED = 1

#Return error constants
class ReturnCode(Enum):
	PRE_TRANSFER_FAILURE = 0
	SUCCESSFUL_TRANSFER = 1
	POST_TRANSFER_FAILURE = 2

#Default Server Request Codes
class RequestCode(Enum):
	PING_SERVER = 1
	
##########################################
#			 Routine Enums
##########################################

class Serialize(Enum):
	JSON = 0
	YAML = 1
	GORM = 2