#####################################
#		   Python Imports
#####################################

import cmd, os, sys
from clint.textui import colored

#####################################
#		  Manakin Imports
#####################################

from pynodetor.sockets import index

#####################################
#		Default Paramaters
#####################################

index = index.Index(
	ip = '',
	port = 8075,
	directory_key_private = 'keys_private/private.pem',
	directory_key_public = 'keys_private/public.pem',
	directory_index = 'json/index.json',
	directory_log = 'json/log.json',
	directory_collected_keys = 'keys_stored/',
	simplified_network = True
)

banner = ( colored.cyan('Manakin Control Pannel')
		   +'\n['
		   + colored.cyan('+')
		   + '] github.com/GabeCordo/manakin-messenger\n' )

#####################################
#		 Terminal Interface
#####################################

class interface(cmd.Cmd):
	
	def __init__(self):
		cmd.Cmd.__init__(self)
		self.prompt = '> '
		self.useLogo = True

	def do_listening(self, args):
		check = index.isThreadOneRuning()
		print(check)
	def def_listening(self):
		print('syntax: listening')
		
	def do_monitoring(self, args):
		check = index.isThreadTwoRunning()
		print(check)
	def def_monitoring(self):
		print('syntax: monitoring')
		
	def do_quit(self, args):
		sys.exit(1)
	def def_quit(self):
		print("syntax: quit")

#####################################
#		 	  Main Code
#####################################

if __name__ == '__main__':
	index.settup()
	prompt = interface()
	prompt.cmdloop(intro=banner)