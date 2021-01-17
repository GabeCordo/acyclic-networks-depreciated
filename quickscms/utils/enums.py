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
	
class Encryption(Enum):
	RSA = 0
	AES = 1
	
class DataTransfer(Enum):
	BASIC = 0
	ADVANCED = 1
	
##########################################
#			 Routine Enums
##########################################

class OfficialMarkups(Enum):
	JSON = 0
	YAML = 1
	GORM = 2