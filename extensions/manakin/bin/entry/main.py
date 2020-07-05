#####################################
#		   Python Imports
#####################################

import cmd, os, sys
from clint.textui import colored

#####################################
#		  Manakin Imports
#####################################

from pynodetor.sockets import entry

#####################################
#		Default Paramaters
#####################################

entry = entry.NodeEntry(
	ip = '',
	port = 8075,
	ip_index = '178.128.234.252',
	ip_backup = '',
	directory_key_private = 'keys/private.pem',
	directory_key_public = 'keys/public.pem'
)

banner = ( colored.cyan('Manakin Server')
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
		check = entry.isThreadOneRuning()
		print(check)
	def def_listening(self):
		print('syntax: listening')
		
	def do_monitoring(self, args):
		check = entry.isThreadTwoRunning()
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
	entry.settup()
	prompt = interface()
	prompt.cmdloop(intro=banner)