###############################
#		python imports
###############################
from time import sleep
from json import dump, load
from threading import Thread

###############################
#	   pynodetor imports
###############################
from pynodetor.utils import errors

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
		self.files = list(args)
		self.data  = []
		self.pull() #validate that the files provided to the class exist
			
	def push(self):
		'''
			(Handler) -> None
			:responsible for pushing the class dictionaries in data into
			 the JSON files linearly
				
			@exception throws a FileNotFound() error if one or more of the
					   files are not valid
		'''
		try:
			for i in range(0, len(self.files)):
				writeToJSON = open(self.files[i], 'w')
				dump(self.data[i], writeToJSON)
				writeToJSON.close()
		except:
			raise FileNotFoundError('linkerJSON Error: one or more of the provided files does not exist.')
	
	def pull(self):
		'''
			(Handler) -> None
			:responsible for pulling the data from the JSON files into the
			 class dictionaries linearly
				
			@exception throws a FileNotFound() error if one or more of the
					   files are not valid
		'''
		try:
			for i in range(0, len(self.files)):
				currentFile = open(self.files[i], 'r')
				self.data.append( load(currentFile) )
				currentFile.close()
		except:
			raise FileNotFoundError('linkerJSON Error: one or more of the provided files does not exist.')
	
	def additionalFunctionality(element):
		'''(Handler) -> None
			:
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
			time.sleep(timer)
			for fileJSON in range(0, len(self.files)):
				keys = self.data[fileJSON].keys()
				for key in range(0, keys):
					element = self.data[fileJSON][key]
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
		threadThree = Thread(target=self.cleaner(timer), args=())