#####################################
#		   Python Imports
#####################################

import cmd, os, sys

#####################################
#		 pynodetor Imports
#####################################

from pynodetor.utils import terminal
from pynodetor.server import console

#####################################
#		 Terminal Interface
#####################################

class interface(cmd.Cmd):
	
	def __init__(self):
		cmd.Cmd.__init__(self)
		self.prompt = '> '
	
	def do_quit(self, args):
		'''Remove your user-id on the tor indexing server, delete the cache, and close the terminal. 
		'''
		self.do_remove_id(args)
		sys.exit(1)
	def def_quit(self):
		print("syntax: quit [userid]")
	
	
#####################################
#		 	  Main Code
#####################################

if __name__ == '__main__':
	prompt = interface()
	prompt.cmdloop(intro=terminal.watermark())
	client.settup()