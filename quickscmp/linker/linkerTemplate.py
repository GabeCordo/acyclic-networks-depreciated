###############################
#		python imports
###############################
from time import sleep
from threading import Thread

###############################
#	   quickscmp imports
###############################
from quickscmp.utils import errors

###############################
#		   main code
###############################
class Handler:
	def __init__(self, *args):
		'''
			(Handler, n strings) -> None
			:the constructor function of the linkerJSON handler class
			 takes in as many files as are required by the Node or element
			
			@exception throws a FileNotFound() error if one or more of
					   the files are not valid
		'''
		self.files = args
		self.data  = []
		self.pull() #validate that the files provided to the class exist
			
	def template_push(self, dump_function):
		'''
			(Handler, Markup Dump Function) -> None
			:responsible for pushing the class dictionaries in data into
			 the JSON files linearly
				
			@exception throws a FileNotFound() error if one or more of the
					   files are not valid
		'''
		try:
			for i in range(0, len(self.files)):
				write_to_markup = open(self.files[i], 'w')
				dump_function(self.data[i], write_to_json)
				write_to_markup.close()
		except:
			raise FileNotFoundError('linkerJSON Error: one or more of the provided files does not exist.')
	
	def template_pull(self, load_function):
		'''
			(Handler, Markup Loader Function) -> None
			:responsible for pulling the data from the JSON files into the
			 class dictionaries linearly
				
			@exception throws a FileNotFound() error if one or more of the
					   files are not valid
		'''
		try:
			for i in range(0, len(self.files)):
				file_current = open(self.files[i], 'r')
				self.data.append(load_function(file_current))
				file_current.close()
		except:
			raise FileNotFoundError(f'linkerJSON Error: one or more of the provided files does not exist.')
	
	def cleanerFunctionality(self, element):
		'''(Handler) -> None
			:adds special functionality to the JSON updater file
		'''
		pass
	
	def cleaner(self, timer):
		'''
			(Handler, int) -> None
			:responsible for manipulating and pushing the dictionary data
			 to the JSON files every 'timer' seconds
		'''
		while True:
			#complete this loop every 'timer' seconds
			sleep(timer)
			for file_json in range(0, len(self.files)):
				keys = self.data[file_json].keys()
				for key in range(0, keys):
					element = self.data[file_json][key]
					#pass the element into the additionalFunctionality function to manipulate the local data
					self.additionalFunctionality(element)
			#push all local changes to the JSON files
			self.push()
			
	def startCleaner(self, timer):
		'''
			(Handler) -> None
			:Starts the cleaner, we want to avoid using it (wastes cpu thread)
			 if we don't need it
		'''
		#thread one and two are occupied by listening port and queue monitor respecitvley
		thread_three = Thread(target=self.cleaner(timer), args=())
		thread_three.daemon = True
		thread_three.start()