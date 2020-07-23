###############################
#	IP Address Indexing
###############################

class Addresses:
	def __init__(self, ip, port, ip_index=None, ip_backup=None):
		'''
			(String, int, String, String) -> None
			:a container class for ip-addresses and standard indexes for the
			 Node socket parent-class
		'''
		self.ip = ip
		self.port = port
		self.ip_index = ip_index
		self.ip_backup = ip_backup


###############################
#	JSON/RSA Paths Container
###############################

class Paths:
	def __init__(self, directory_key_public, directory_key_private, directory_file_logging):
		'''
			(String, String, String) -> None
			:a container class for JSON and public key direcetories required for encrypting
			 packet traffic and logging latency data for tracking (respectivly)
		'''
		self.directory_key_public = directory_key_public
		self.directory_key_private = directory_key_private
		self.directory_file_logging = directory_file_logging

###############################
#	Customization Container
###############################

class Customizations:
	def __init__(self, supports_encryption=True, supports_listening=True,
				 supports_monitoring=True, supports_recovery=True, 
				 supports_console_cout=False, supports_data_capture=False):
		'''
			(bool, bool, bool, bool, bool, bool)
			:a container class for all the various customization options for the Node class
			 so that it can be used across multiple Node without redundant hardcoding
		'''
		self.supports_encryption = supports_encryption
		self.supports_listening = supports_listening
		self.supports_monitoring = supports_monitoring
		self.supports_recovery = supports_recovery
		self.supports_console_cout = supports_console_cout
		self.supports_data_capture = supports_data_capture
		
## PRE-SET CUSTOMIZATIONS FOR ROUTING NODES

PRESET_SETTINGS_ENTRY = Customizations(
		supports_encryption = True,
		supports_listening = True,
		supports_monitoring = False,
		supports_recovery = True,
		supports_console_cout = False
	)

PRESET_SETTINGS_BALANCER = Customizations(
		supports_encryption = True,
		supports_listening = True,
		supports_monitoring = False,
		supports_recovery = False,
		supports_console_cout = False
	)

PRESET_SETTINGS_INDEX = PRESET_SETTINGS_BALANCER

PRESET_SETTINGS_RELAY = Customizations(
		supports_encryption = False,
		supports_listening = True,
		supports_monitoring = True,
		supports_recovery = True,
		supports_console_cout = False
	)

PRESET_SETTINGS_EXIT = Customizations(
		supports_encryption = False,
		supports_listening = True,
		supports_monitoring = True,
		supports_recovery = False,
		supports_console_cout = False
	)

###############################
#		   	  EOF
###############################