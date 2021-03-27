###############################
#	  	python imports
###############################

from yaml import load, dump

###############################
#	   quickscms imports
###############################

from quickscms.linker import linkerTemplate

###############################
#	  YAML LINKER Wrapper
###############################

class Handler(linkerTemplate.Handler):
	
	def __init__(self, *args):
		'''
			(List of Strings) -> None
			:Constructor function for the YAML handler. This function allows any number of JSON files to be entered under args*.  
		'''
		super().__init__(args)
		self.pull() #test whether the provided files exist
	
	def push(self):
		'''
			:pushes to the changes in the class
			 dictionary to all the YAML files
		'''
		self.template_push(dump)
		
	def pull(self):
		'''
			:pulls all the data within the YAML
			 files that have been pushed as class
			 parameters
		'''
		self.template_pull(dump)
		
###############################
#	 		 EOF
###############################