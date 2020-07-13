
class Event:
	
	def __init__(self, generic, title, description, starts, ends, function, repeat=False):
		'''
			(Event, Generic, string, datetime, datetime, object, boolean) -> None
			:the constructor class for events that are scheduled on callenders
			 or on alarms using the pynodetor system
			
			@paramaters the types must be respected indicated above
		'''
		self.generic = generic
		self.title = title
		self.description = description
		self.starts = starts
		self.ends = ends
		self.function = function
		self.repeat = repeat
	
	def execute(self):
		'''
			(Event) -> Generic
			:executes the function passed to the Event wrapper upon its initialization
			
			@returns a generic type that is the return type of the function
			@exception if there is no return type on the function, None
		'''
		return self.function
		
	def __eq__(self, other):
		'''
			(Event, object) -> (boolean)
			:the comparator operator overide for the Event class, compares two
			 objects based on whether there start and end dates are the same
			
			@returns boolean True if there is a conflict in the timing
			@exception returns boolean False if there are no conflicts in timing
		'''
		if (type(other) != type(self)):
			return False
			
		#check to see if the times overlap, using the built-in comparators of the
		#datetime python function
		if (self.starts < other.ends and other.starts < self.ends):
			return False
		
		return True #the two events do not overlap
		
	def __str__(self):
		'''
			(Event) -> (string)
			:returns a friendly looking string for the title and description of
			 the specific event
			
			@returns a client-friendly string to the calling thread
		'''
		return (self.title + ':' + self.description)
		
	def __repr__(self):
		'''
			(Event) -> (tuple)
			:returns a tuple of all the critical-information held within the Event
			 class that could be required for specific processing
			
			@returns a tuple representing the title, start-time, end-time, and
					 whether the event is meant to repeat
		'''
		return (self.title, self.starts, self.ends, self.repeat)
		