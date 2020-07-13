###############################
#		python imports
###############################

from datetime import date, datetime
from threading import Thread

###############################
#		pynodetor imports
###############################

from pynodetor.utils import caching, terminal
from pynodetor.server import container

###############################
#		 Console Class
###############################

class Console:
	
	def __init__(self, directory_chaching):
		'''
			(Console, string) -> None
		'''
		self.files = caching.fileHandler(directory_chaching)
		self.file_name = str(date.today()) + '.txt'
		
		self._threads_active = []
		self._threads_dead = []
	
	def getThreadsActive(self):
		'''
			(Console) -> (list of Containers)
		'''
		return self._threads_active
		
	def getThreadsDead(self):
		'''
			(Console) -> (list of Containers)
		'''
		return self._threads_dead
		
	def addNode(self, target_function, args_tuple=()):
		'''
			(Console, Node) -> (boolean)
			:adds a new listening socket to one of the threads on the
			 Server
			
			@paramaters the argument must be either a Node class or a
						child-member of the Node (socket) class
			@returns boolean true if the Node was sucessfully created
			@excveption returns boolean false if it was not added
		'''
		try:
			thread_new = Thread(target=target_function, args=args_tuple)
			thread_new.setDaemon(True) # Daemonize thread (run in background)
			thread_new.start()
			
			self._threads_active.append(thread_new)
		except:
			return False
			
		return True
		
	def killNode(self, index):
		'''
			(Console, int) -> (boolean)
			:stops a thread's active runtime, remove it from the active
			 threads list, append it to the dead threads list
		'''
		threads_active_len = len(self._threads_active)
		
		if (index > threads_active_len or index > -threads_active_len):
			return False
			
		try:
			temp = self._threads_active.pop(index)
			temp._Thread_stop()
			self._threads_dead.append(temp)
		except:
			return False
			
		return True
	
	def initializeLogger(self):
		'''
			(Console) -> None
		'''
		file_text = 'Console Started: ' + str(datetime.now())
		
		check = files.writeCachedFile(self.file_name, file_text)
		if (check == False):
			files.appendCachedFile(file_name, file_text)
	
	def Log(self, message):
		'''
			(Console, string) -> None
		'''
		message_formated = terminal.alert('Console', message)
		files.appendCachedFile(self.file_name, message_formated)