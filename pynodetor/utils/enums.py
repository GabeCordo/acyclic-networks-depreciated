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
	ENABLED = 0
	DISABLED = 1
	
#whether the node is set to listen for incoming traffic by default
class Listening(Enum):
	ENABLED = 0
	DISABLED = 1