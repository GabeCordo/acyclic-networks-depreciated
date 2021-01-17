#####################################
#		   Python Imports
#####################################

from clint.textui import colored
from datetime import datetime
from pyfiglet import Figlet
from random import randint

#####################################
#		   ASCII GRAPHICS
#####################################

def watermark():
	'''
		None -> (string)
		
		@returns the programmer and repository details
	'''
	title = 'PYNODETOR Server Console'
	text = '\n[' + colored.yellow('+') + '] github.com/GabeCordo/manakin-messenger\n'
	return (title + text)
	
#####################################
#		   Data Graphics
#####################################

def file(header, data):
	'''
		(string, list of strings) -> (string)
		
		@returns a pretty version of the file text
	'''
	header = colored.green(header)
	header = f'\n[ {header} ]\n'
	
	line = ''
	for i in range(0, len(data)):
		line = '\t' + line + f'{i+1}. {data[i]}\n'
	
	footer = colored.green('end of text')
	footer = f'[ {footer} ]\n'
	
	print(header + line + footer)
	
def message(id_user, message):
	'''
		(string, string) -> (string)
		
		@returns a pretty version of the received message
	'''
	header = colored.cyan(id_user)
	header = f'[ {header} ] '
	
	print(header + message) 
	
def alert(header, message):
	'''
		(string, string) -> (string)
		
		@returns an alert titled with the header with the
				 description of the alert being the message
	'''
	header = colored.red(header)
	header = f'[ {header} ] '
	
	print(header + message)
	
#####################################
#		   		EOF
#####################################
	