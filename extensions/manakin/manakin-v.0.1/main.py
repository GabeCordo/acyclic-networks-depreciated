#####################################
#		   Python Imports
#####################################

import cmd, os, sys

#####################################
#		  Manakin Imports
#####################################

import generator
import config

from sockets import incoming, outgoing
from requests import local, server
from pynodetor.sockets import node
from graphics import terminal

#####################################
#		Default Paramaters
#####################################

config = config.Config('json/config.json')

client = node.Node(
	ip = '',
	ip_backup = '',
	port = config.getPort(),
	directory_key_private = config.getDirectoryPrivateKey(), 
	directory_key_public = config.getDirectoryPublicKey()
)

OPEN_NODE = config.getEntryServer()

INDEXING = config.isIndexed()
CACHING = config.isCaching()

#####################################
#		 Terminal Interface
#####################################

class interface(cmd.Cmd):
	
	def __init__(self):
		cmd.Cmd.__init__(self)
		self.prompt = '> '
	
	##		Visual Settings		##
	
	def do_banner(self, args):
		'''Refresh the manakin client terminal with a new banner.
		'''
		os.system('clear') #clear the temrinal to have a fresh start
		prompt.cmdloop(intro=graphics.banner())
	def def_banner(self, args):
		print("syntax: banner")
	
	##		UserID Indexing		##
	
	def do_setup_id(self, args):
		'''Setup a new tor user-id on the indexing server.
		'''
		message = server.addIndex(args, client.handler_keys.getPublicKey().decode()) #format the message using the request modules
		print(message)
		result = client.send(OPEN_NODE, message)
		terminal.alert('UserID', f'Indexed on the server to {args}. ({result})')
	def def_setup_id(self):
		print("syntax: setup_id [user-id]")
	
	def do_lookup_id(self, args):
		'''Validate whether your user-id is on the tor indexing server.
		'''
		message = server.lookupIndex(args)
		result = client.send(OPEN_NODE, message)
		terminal.alert('UserID', f'Indexed on the server: {args}. ({result})')
	def def_lookup_id(self):
		print("syntax: lookup_id [user-id]")
	
	def do_remove_id(self, args):
		'''Remove your user-id from the tor indexing server.
		'''
		message = server.deleteIndex(args)
		result = client.send(OPEN_NODE, message)
		terminal.alert('UserID', f'De-indexed on the server: {args}. ({result})')
	def def_remove_id(self):
		print("syntax: remove_id [user-id]")
	
	##		Logs		##
	
	def do_log(self, args):
		'''
		'''
		text = local.pullChatHistory(config.directoryCaching(), args)
		terminal.file(id_user, text)
	def def_log(self):
		print("syntax: log [user-id]")
	
	##		Pending		##
	
	def do_pending(self, args):
		'''
		'''
		text = local.pullPending(config.directoryCaching())
		terminal.file('pending', text)
	def def_pending(self, args):
		print("syntax: pending")
		
	def do_pending_transfer(self, args):
		'''
		'''
		data = local.splitter(args)
		if (data[1] != 'whitelist' and data[1] != 'blacklist'):
			pass
		requests.transferPending(config.directoryCaching(), data[0], data[1])
	def def_pending_transfer(self):
		print("syntax: pending_transfer [user-id] [whitelist/blacklist]")
	
	##		Whitelist		##
	
	def do_whitelist(self, args):
		'''
		'''
		text = local.pullWhitelist(config.directoryCaching())
		terminal.file('whitelist', text)
	def def_whitelist(self):
		print("syntax: whitelist")
	
	def do_whitelist_add(self, args):
		'''Whitelist a foreign user-id to send you messages across the tor network.
		'''
		result = local.addWhitelist(config.directoryCaching(), args)
		terminal.alert('Whitelist', f'Added {args} to the file. ({result})')
	def def_whitelist_add(self):
		print("syntax: whitelist_add [userid]")
		
	def do_whitelist_remove(self, args):
		'''
		'''
		local.removeWhitelist(config.directoryCaching(), args)
		terminal.alert('Whitelist', f'Removed {args} from the file.')
	def def_whitelist_remove(self):
		print("syntax: whitelist_remove [user-id]")
	
	##		Blacklist		##
	
	def do_blacklist(self, args):
		'''
		'''
		text = local.pullBlacklist(config.directoryCaching())
		terminal.file('blacklist', text)
	def def_blacklist(self):
		print("syntax: blacklist")
	
	def do_blacklist_add(self, args):
		'''Blacklist a foreign a user-id to stop the transfer of messages.
		'''
		result = local.addBlacklist(config.directoryCaching(), args)
		terminal.alert('Blacklist', f'Added {args} to the file. ({result})')
	def def_blacklist_add(self):
		print("syntax: blacklist_add [user-id]")
		
	def do_blacklist_remove(self, args):
		'''
		'''
		result = local.removeBlacklist(config.directoryCaching(), args)
		terminal.alert('Blacklist', f'Removed {args} to the file. ({result})')
	def def_blacklist_remove(self):
		print("syntax: blacklist_remove [user-id]")
	
	##		Toggling Settings		##
	
	def do_toggle_caching(self, args):
		'''Toggle the caching of messages received on your client whitelist.
		'''
		if (config.isCaching() == True):
			value = False
		else:
			value = True
		config.setCaching(value)
	def def_toggle_caching(self):
		print("syntax: toggle_caching")
	
	def do_toggle_incoming(self):
		'''Toggle whether you wish to accept incoming user-id whitelist requsts.
		'''
		if (config.isIncoming() == True):
			value = False
		else:
			value = True
		config.setIncoming(value)
	def def_toggle_incoming(self):
		print("syntax: toggle_incoming")
	
	##		Messeging		##
	
	def do_send_message(self, args):
		'''Send a message to a target-id across the tor-network on your friend list.
		'''
		data = local.splitter(args)
		message = server.sendMessage(data[0], data[1])
		result = client.send(OPEN_NODE, message)
		terminal.alert('Ping', f'Message sent to {data[0]} over the network. ({result})')
	def def_send_message(self):
		print("syntax: send_message [user-id] [messsage]")

	##		Other Settings		##
	
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
	prompt.cmdloop(intro=terminal.banner())
	client.settup()