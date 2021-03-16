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
				 supports_monitoring=True, supports_dynamic_interaction=True,
				 supports_recovery=True, supports_console_cout=False, 
				 supports_data_capture=False, supports_dynamic_keyset=True):
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
		self.supports_dynamic_interaction = supports_dynamic_interaction
		self.supports_dynamic_keyset = supports_dynamic_keyset
		
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
#	 Routine Configuration
###############################

class RoutineAuthor:
	def __init__(self, author_name='', author_email='', author_site='',
				 date='', name='Unnamed Routine', version=1.0, description='', 
				 licence=None, keywords=None, classifiers=None, documentation=None):
		'''
			(String, String, String, String, String, Int, String, String, List, List, String) -> None
			:a container class for the contents of the author file. This is to catagorize
			 developer and routine details that contribute to the documentation of a routine
			 rather than the functionality of the package.
		'''
		self.author_name = author_name
		self.author_email = author_email
		self.author_site = author_site
		self.date = date
		self.name = name
		self.version = version
		self.description = description
		self.licence = licence
		self.keywords = keywords
		self.classifiers = classifiers
		self.documentation = documentation

class RoutineSettings:
	def __init__(self, port=5078, markup='Basic', return_codes=[0,1,2],
				 buffer_size=1024, latency_size=4):
		'''
			(Int, String, List of Ints, Int, Int) -> None
			:a container class for the settings of the routines config file. These are
			 generic paramaters that control the barebone functionality of the sockets.
		'''
		self.port = port
		self.markup = markup
		self.return_codes = return_codes
		self.buffer_size = buffer_size
		self.latency_size = latency_size

###############################
#		   	  EOF
###############################