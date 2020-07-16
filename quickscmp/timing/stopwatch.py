###############################
#		python imports
###############################

from time import time

###############################
#	  quickscmp imports
###############################

from quickscmp.timing.timer import Timer

###############################
#	    Stop Watch Class
###############################

class StopWatch(Timer):
	
	def __init__(self, precision=3):
		'''
			(StopWatch, int) -> None
			:constructor function for the StopWatch class, will initialize a
			 starting time upon the function call
			
			@paramaters the precission paramater must be given a integer
						argument, representing the number of decimals ea-
						ch float value will have that is logged, default 3
		'''
		super().__init__(precision)
		
	def getLaps(self):
		'''
			(Timing) -> (list of floats)
			:the getter funciton for the last recorded time difference
		'''
		return self.log
		
	def getShortestLap(self):
		'''	
			(Timing) -> (float)
			:the getter function fro the shortest recorded time
			
			@returns the smallest float in the list of logs
		'''
		return self._findValue()
		
	def getLongestLap(self):
		'''
			(Timing) -> (float)
			:the getter function for the longest recorded time
			
			@returns the largest float in the list of logs
		'''
		return self._findValue(find_min = False)
	
	def lap(self):
		'''
			(Timing) -> (float)
			:append a new time to the list of laps
		'''
		temp = round(time(), self.precision)
		log_len = len(self.log)
		
		#check to see if we have a log already or not
		if (log_len > 0): #we are more likely to already have a log, therefore, we put it first
			temp -= (sum(self.log) + self.start)
		elif (log_len == 0):
			temp -= self.start #if not, sub from the start time
		
		#we don't want to accept any values of 0
		if (temp > 0):
			self.log.append(temp) #append the time in-between to the class variable log[]
			return temp
	
	def _findValue(self, find_min=True):
		'''
			(Timing, boolean) -> (float)
			:either looks for the maximum or minimum value with-
			 in the list of floats, by default finds the minimum
			
			@returns the minimum or maximum value in the log
			@exception returns 0.0 if a non-boolean was provided
		'''
		if (type(find_min) != bool):
			return 0.0
		
		if (len(self.log) == 1):
			return self.log[0]

		value = self.log[0]
		for lap in self.log:
			if (find_min == True and lap < value):
				value = lap
			elif (find_min == False and lap > value):
				value = lap
				
		return value