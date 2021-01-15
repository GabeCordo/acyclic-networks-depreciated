###############################
#	  	python imports
###############################

from yaml import load, dump

###############################
#	   quickscmp imports
###############################

from quickscmp.linker import linkerTemplate

###############################
#	  YAML LINKER Wrapper
###############################

class Handler(linkerTemplate.Handler):
	
	def __init__(self, *args):
		'''
			(String...) -> None
		'''
		super().__init__(args)
	
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