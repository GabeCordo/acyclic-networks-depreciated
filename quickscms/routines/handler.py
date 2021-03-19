###############################
#		python imports
###############################

from sys import path

###############################
#	   quickscms imports
###############################

from quickscms.linker import linkerYAML, linkerJSON
from quickscms.types import containers, errors

###############################
#	   external imports
###############################

path.append('..')

###############################
#		 routine code
###############################

class Handler(linkerYAML.Handler):
	
	def __init__(self, directory_to_routine):
		'''
			(String) -> None
			:the constructor class for the routine handler function responsible
			 for initializing
		'''
		super().__init__(directory_to_routine + 'author.yaml', directory_to_routine + 'config.yaml')
		
		self.sheet_author = self.data[0]
		self.sheet_config = self.data[1]
		
		self.directory_to_routine = directory_to_routine
		
		self.loadConfigurations() #check all the configurations in the file
		
		self.list_of_scripts = self._load_scripts()
		self.list_of_markdowns = self._load_markdowns()

		self.func_switch = None
	
	def routine_info(self) -> tuple(str, str):
		'''
			(Handler) -> (name, version, description)
			:returns a tuple of information pertaining to the routine
		'''
		return (self.sheet_author['data']['routine']['name'],
				self.sheet_author['data']['routine']['version'],
				self.sheet_author['data']['routine']['description']
		)

	def author_info(self) -> tuple(str, str, str):
		'''
			(Handler) -> (name, email, site)
			:returns a tuple of information pertaining to the author
		'''
		return (self.sheet_author['data']['routine']['name'],
				self.sheet_author['data']['routine']['email'],
				self.sheet_author['data']['routine']['site']
		)
	
	def change_port(self, port: int):
		'''
			(int) -> None
			:changes the ip-address that is located on the config sheet, this may be required
			 if the port-forwarded ip address has changed for some reason or the script has
			 been moved to a new machine

			@condition the port must be outside of the 0-1024 range
		'''
		if (port < 1024 or port > 65535):
			raise errors.IllegalPortRange
		
		self.sheet_config['config']['settings']['port'] = port
		self.push() #dump the changes of the YAML configuration file to the stored location
	
	def uses_custom_settings(self):
		'''
			(None) -> (boolean)
			:returns whether the routine implements custom scripts, markup-sheets or settings
			 for the protocol listed under a specific section of the configuration sheet
		'''
		return self.sheet_config['config']['custom']['using-custom']
	
	def _load_configurations(self):
		'''
			(None) -> (boolean)
			:create a reference to the location of the custom-config's dictionary
			 starting key to avoid redundant and convoluted dictionary syntax
		'''
		if self.usesCustomSettings():
			self.sheet_custom = self.sheet_config['config']['custom']
			return True
		
		#the custom-setting flag is set to false on the config sheet, so we will not
		#initialize any data that may, or may not exist past this point
		return False
		
	def _load_markdowns(self) -> list[str]:
		'''
			(None) -> (list of markdown scripts)
		'''
		##there are 3 officials supported markups: JSON, YAML, GORM. All are stored in
		#arrays within the custom-markup key and can access each file by indexing
		self.list_of_markdowns.append(linkerJSON.Handler(self.sheet_config['config']['custom']['custom-markup'][0]))
		self.list_of_markdowns.append(linkerYAML.Handler(self.sheet_config['config']['custom']['custom-markup'][1]))
		
		#TODO: there has yet to be a linker written for GORM, as GORM is under development
		
		#we need to return a list of custom markups for console output
		return self.sheet_config['config']['custom']['markup-sheets']
	
	def _load_scripts(self) -> list[str]:
		'''
			(None) -> (list of functions)
		'''
		path.append(self.directory_to_routine + '/scripts/official/')
		import dtpf, icf, qmf, rcf

		self.func_switch = {
			'dtpf': dtpf.main,
			'icf': icf.main,
			'qmf': qmf.main,
			'rcf': rcf.main 
		}

		#we need to return a list of custom functions for console output
		return self.sheet_config['config']['custom']['scripts']

	def cast_to_container_addresses(self) -> containers.Addresses:
		'''
		'''
		return containers.Addresses(
			ip = self.sheet_config['config']['addresses']['ip'],
			port = self.sheet_config['config']['settings']['port'],
			ip_index = self.sheet_config['config']['addresses']['index'],
			ip_backup = self.sheet_config['config']['addresses']['backup']
		)

	def cast_to_container_paths(self) -> containers.Paths:
		'''
		'''
		return containers.Paths(
			directory_key_public = self.sheet_config['config']['paths']['rsa'] + 'public.pem',
			directory_key_private = self.sheet_config['config']['paths']['rsa'] + 'private.pem',
			directory_file_logging = self.sheet_config['config']['paths']['logging']
		)

	def cast_to_container_customizations(self) -> containers.Customizations:
		'''
		'''
		return containers.Customizations(
			supports_encryption = self.sheet_config['config']['customizations']['encryption'],
			supports_listening = self.sheet_config['config']['customizations']['listening'],
			supports_monitoring = self.sheet_config['config']['customizations']['monitoring'],
			supports_recovery = self.sheet_config['config']['customizations']['recovery'],
			supports_console_cout = self.sheet_config['config']['customizations']['console'],
			supports_data_capture = self.sheet_config['config']['customizations']['data-capture'],
			supports_dynamic_interaction = self.sheet_config['config']['customizations']['dynamic-interaction'],
			supports_dynamic_keyset = self.sheet_config['config']['customizations']['dynamic-keys'],
			supports_scheduling_events = self.sheet_config['config']['customizations']['scheduling-events']
		)
		