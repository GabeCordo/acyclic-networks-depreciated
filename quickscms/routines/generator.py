###############################
#		python imports
###############################

from os import mkdir
from shutil import copyfile, copytree
from sys import path

###############################
#	   quickscms imports
###############################

from quickscms.linker import linkerYAML
from quickscms.utils import errors, enums

###############################
#		generator code
###############################

class Routine:
	
	def __init__(self, container_routine_author, container_routine_settings,
				 container_addresses, container_paths, container_customizations):
		'''
			(Routine, Addresses, Paths, Customizations) -> None
			:The constructor function for the Routine generator. Required to initialize
			 the various data-containers needed by the generator to create a proper r-
			 outline directory, furthermore creating holder-class variables for YAML and
			 directory handlers.
		'''
		self.container_routine_author = container_routine_author,
		self.container_routine_settings = container_routine_settings,
		self.container_addresses = container_addresses,
		self.container_paths = container_paths,
		self.container_customizations = container_customizations
		
		self.directory_root = None
		self.yaml_handler_config = None
		self.yaml_handler_author = None
	
	def _generate_template_routine(self, directory_root):
		'''
			(Routine, String) -> None
			:Copies the template for protocol routines found within the source code and
			 creates a deep-copy in the directory provided as an argument to the function
		'''
		self.directory_root = directory_root + './' + self.container_routine_author.name
		copytree(self.directory_root, directory_root)
	
	def _dictionary_create_author(self):
		'''
			(Routine) -> (boolean)
			:creates a YAML file for the author/routine information that does not effect the
			 functionality of the 
				
			@returns boolean True if the YAML file was successfully created with the data in the
					 containers passed as class arguments
			@paramaters the _generate_template_routine must have been called creating the blank
						directories and markup files
		'''
		if self.directory_root is not None:
			self.yaml_handler_author = linkerYAML.Handler(self.directory_root + 'author.yaml')
			self.yaml_handler_author.data[0] = {
				"data" : {
					"author" : {
						"name": self.container_routine_author.author_name,
						"email": self.container_routine_author.author_email,
						"site": self.container_routine_author.author_site,
						"date": self.container_routine_author.date
					},
					"routine" : {
						"name": self.container_routine_author.name,
						"version": self.container_routine_author.version,
						"description": self.container_routine_author.description,
						"licence": self.container_routine_author.licence,
						"keywords": self.container_routine_author.keywords,
						"classifiers": self.container_routine_author.classifiers,
						"documentation": self.container_routine_author.documentation
					}
				}
			} 
			self.yaml_handler_author.push()
			return True
			
		##If we return false that means that the routine class variable is still set to None,
		#meaning that we have not created a new routine with the generator
		return False
		
	def _dictionary_create_config(self):
		'''
			(Routine) -> (boolean)
			:creates a YAML file for the config information that effects the functionality of
			 the routine being implemented
				
			@returns boolean True if the YAML file was successfully created with the data in the
					 containers passed as class arguments
			@paramaters the _generate_template_routine must have been called creating the blank
						directories and markup files
		'''
		if self.directory_root is not None:
			self.yaml_handler_config = linkerYAML.Handler(self.directory_root + 'config.yaml')
			self.yaml_handler_config.data[0] = {
				"config" : {
					"settings" : {
						"port": self.container_addresses.port,
						"markup": self.container_routine_settings.markup,
						"return-codes": self.container_routine_settings.return_codes,
						"buffer-size": self.container_routine_settings.buffer_size,
						"latency-size": self.container_routine_settings.latency_size
					},
					"addresses" : {
						"ip": self.container_addresses.ip,
						"index": self.container_addresses.ip_index,
						"backup": self.container_addresses.ip_backup
					},
					"paths" : {
						"rsa": self.directory_root + '/paths/keys/',
						"logging": self.directory_root + './paths/logging/',
						"markup": self.directory_root + './paths/markup'
					},
					"customizations" : {
						"encryption": self.container_customizations.supports_encryption,
						"listening": self.container_customizations.supports_listening,
						"monitoring": self.container_customizations.supports_monitoring,
						"recovery": self.container_customizations.supports_recovery,
						"console": self.container_customizations.supports_console_cout,
						"data-capture": self.container_customizations.supports_data_capture,
						"dynamic-interaction": self.container_customizations.supports_dynamic_interaction,
						"scheduling-events": self.container_customizations.support_scheduling_events
					},
					"custom" : {
						"using-custom": False,
						"custom-settings": {},
						"custom-scripts": [],
						"markup-sheets": []
					}
				}
			}
			self.yaml_handler_config.push()
			return True
		
		##If we return false that means that the routine class variable is still set to None,
		#meaning that we have not created a new routine with the generator
		return False
	
	def _negate_custom_settings_bool(self):
		'''
			(Routine) -> (None)
			:due to the verbose syntax, this is a form of syntactical sugar
			 to make the manipulation of this deep-data in the dictionary
			 easily changeable
		'''
		self.yaml_handler_config['config']['custom']['using-custom'] = not self.yaml_handler_config['config']['custom']['using-custom']
		
	def _check_custom_settings(self):
		'''
			(Routine) -> (None)
			:if the use of custom settings are turned off, it will be turned
			 on to true
			
			!this function should be called at the call of any function adding
			 custom content to make sure it is up-to-date
		'''
		if self.yaml_handler_config['config']['custom']['using-custom'] is False:
			self._negate_custom_settings_bool()
		
	def add_custom_setting(self, identifier, Y):
		'''
			(String, Generic Y) -> (None)
			:add an key-data pair to the custom-settings dictionary to the config
			 file for storing information custom to the created routine
			
			@paramaters the generic must be a primitive type supported by the YAML
						markup language
		'''
		self._check_custom_settings()
		self.yaml_handler_config['config']['custom']['custom-settings'][identifier] = Y
	
	def add_script(self, script_name, directory_script):
		'''
			(Routine, String, String) -> (None)
			:add a custom python script to the folder in the routine, these are to be
			 called by the official python files
			
			!this custom directory will standardize the location for custom code that 
			 has been abstracted from the official scripts 
				L-> this directory will be imported by default in all official python 
					scripts
		'''
		self._check_custom_settings()
		self.yaml_handler_config['config']['custom']['custom-scripts'].append(script_name)
		copyfile(directory_script, self.directory_root + '/scripts/custom')
	
	def add_markup(self, markup_name, markup_enum, directory_markup):
		'''
			(Routine, String, RoutineSettings, String) -> (None)
			:add a custom markup file to the folder in the routine, this is for detailed
			 data-sheets that ARE NOT CONFIG SETTINGS
				L-> Config settings are added to the official config yaml markup
			
			!markups must be one of the officially supported languages, check supported
			 markups in the scms protocol documentation for more information
		'''
		self._check_custom_settings()
		self.yaml_handler_config['config']['custom']['markup-sheets'][markup_enum].append(markup_name)
		copyfile(directory_markup, self.directory_root + 'paths/logging/markup')
		
	def generate_new_routine(self, directory_root):
		'''
			(Routine, String) -> (None)
			:creates a bare-bone routine (based off of the template within the library) and
			 customizes the author and config sheets based on data passed to the class
			
			!scripts, markups and settings must be added individually
		'''
		try:
			self._generate_template_routine(directory_root)
			self._dictionary_create_author()
			self._dictionary_create_config()
		except:
			raise errors.CorruptedRoutine