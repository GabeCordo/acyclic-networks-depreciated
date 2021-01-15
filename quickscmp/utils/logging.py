#####################################
#		   Python Imports
#####################################

from pyfiglet import Figlet
from clint.textui import colored
from datetime import datetime

#####################################
#		  quickscmp Imports
#####################################

from quickscmp.linker import linkerJSON

#####################################
#			  Constants
#####################################

TITLE = '[' + colored.red('Console') + '] '

BRACKET_START = '---------------------------' + colored.red('>')
BRACKET_END = colored.red('<') + '---------------------------'

#####################################
#		 Condosole Graphics
#####################################

class Logger(linkerJSON.Handler):
	
	def __init__(self, file_logging_path, flag_graphics):
		'''
			(String, boolean) -> None
			:the constructor class for the logging class which
			 initializes the logging json file and the boolean
			 flag which determines whether logging text will be
			 outputed to the console.
		'''
		super().__init__(file_logging_path)
		self.flag_graphics = flag_graphics
		
		self.log = self.data[0] #pull the first data(JSON) sheet from the linkerJSON class
		self.identifier = 'NONE'
		self.num_of_commits = 0 #the number of data pieces we collect per log
	
	def terminal_start_logging(identifier):
		'''
			(String) -> None
			:Will start a new logg for a connection to the server
			 or client node
		'''
		if (self.flag_graphics):
			print(BRACKET_START)
		
		self.identifier = identifier
		self.num_of_logs = 0
		
		self.log[identifier] = {
			"connected": str(datetime.now()),
			"commits": []
		}
	
	def notification(text):
		'''
			(String) -> None
			:loggs a new entry to the JSON File specified within the class
			 constructor 
		'''
		temp_time = datetime.now().time()
		
		if (self.flag_graphics):
			print(TITLE + f'({temp_time}) {text}')

		self.num_of_commits += 1
		seld.log[self.identifier]['commits'][self.num_of_commits] = {
			"time": temp_time,
			"text": text
		}
	
	def terminal_stop_logging():
		'''
			:Will stop a logg for a connection to the server or
			 client node
		'''
		if (self.flag_graphics):
			print(BRACKET_END)
			
		self.push() #this will commit all the logging changes to the JSON file

#####################################
#		   		EOF
#####################################