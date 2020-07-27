###############################
#	  	python imports
###############################

from json import dump, load

###############################
#	   quickscmp imports
###############################

from quickscmp.linker import linkerTemplate

###############################
#	  JSON LINKER Wrapper
###############################

class Handler(linkerTemplate.Handler):
	
	def __init__(self, *args):
		'''
			(Strings) -> None
			:
		'''
		super().__init__(args)
		
	def push():
		'''
			:pushes to the changes in the class
			 dictionary to all the JSON files
		'''
		self.template_push(dump)
			
	def pull():
		'''
			:pulls all the data within the JSON
			 files that have been pushed as class
			 parameters
		'''
		self.template_pull(load)
		
###############################
#	 		 EOF
###############################