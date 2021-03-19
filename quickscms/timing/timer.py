###############################
#		python imports
###############################

from time import time

###############################
#		 Timing Class
###############################

class Timer:

	def __init__(self, precision=3):
		'''
			(Timing, int) -> (None)
			:constructor function for the Timing class, will initialize a
			 starting time upon the function call
			
			@paramaters the precission paramater must be given a integer
						argument, representing the number of decimals ea-
						ch float value will have that is logged, default 3
		'''
		self.precision = precision
		self.start = round(time(), self.precision) #start time of the class
		
		self.log = []
	
	def getLog(self):
		'''
			(Timing) -> (list of floats)
			:the getter function for the last recorded time difference
		'''
		return self.log
	
	def getStart(self):
		'''
			(Timing) -> (float)
			:the getter function for the classes start time
			
			@returns the time recorded when the class was initialized
		'''
		return self.start
	
	def pop(self, index):
		'''
			(Timing) -> (float)
			:remove a stored lap based on it's index
				
			@returns a float representing the popped value
			@exception returns 0.0 if a valid index was given
		'''
		log_length = len(self.log)
			
		if (index > log_length or (index < 0 and index < -log_length)):
			return 0.0
			
		return self.log.pop(index)
	
	def reset(self):
		'''
			(Timing) -> (None)
			:remove the currently stored laps on the Timmer
		'''
		self.log = []
	
	def timeAlive(self):
		'''
			(Timer) -> (float)
			:a function returning the time the Timer class has been
			 running since being initialize, following the rounding
				
			@returns a float representing time since placed on the heap
		'''
		temp = round(time(), self.precision) - self.start
		return temp
		
	def __eq__(self, other):
		'''
			(Timer, object) -> (boolean)
		'''
		#check if the types are the same
		if (type(other) != type(self)):
			return False
			
		#check to see if the logs of both of the timers are the same
		if (self.log != other.log):
			return False
		
		return True
		
	def __repr__(self):
		'''
			(Timing) -> (list of floats)
			:the Timing class can be represented by the the list of
			 logs they hold from the lap function being called
				
			@returns a list of floats representing all the laps
			@exception if no laps have been called an empty list of 
					   floats is returned
		'''
		return self.log
		
	def __str__(self):
		'''
			(Timing) -> (string)
			:the string representation function for the Timer class
			
			@returns a client-friendly string representing the class
		'''
		return f'Timer(start={self.start}, {self.precision})'
			
	def __del__(self):
		'''
			(Timing) -> (float)
			:the destructor object for the Timing class, released from
			 memory and returns the total runtime of the counter
		'''
		temp = round(time(), self.precision) - self.start
		return temp