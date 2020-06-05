###############################
#		python imports
###############################

from time import sleep
from datetime import datetime
from threading import Thread

###############################
#	  pynodetor imports
###############################

from pynodetor.timing.timer import Timer
from pynodetor.timing.event import Event

###############################
#	   	  Alarm Class
###############################

class Alarm(Timer):
	
	def __init__(self, precision=3):
		'''
			(Alarm, int) -> None
			:constructor function for the StopWatch class, will initialize a
			 starting time upon the function call
			
			@paramaters the precission paramater must be given a integer
						argument, representing the number of decimals ea-
						ch float value will have that is logged, default 3
		'''
		super().__init__(precision)
		
	def alarms(self):
		'''
			(Alarm) -> (list of Events)
			:the getter function for the alarms that have been added to the
			 Alarm class to be executed upon the time
			
			@returns a list of Events that have been prepared to execute
		'''
		return self.log
		
	def add(self, event):
		'''
			(Alarm, event) -> None
			:an adder function which ensures that the object being pushed is
			 of type Event, to be executed when the time is ready
			
			@paramaters the argument must be of type Event
		'''
		if (type(event) != type(Event)):
			return False
			
		log.append(event) #the argument is of type Event, and should be added
	
	def _monitor(self):
		'''
			(Alarm) -> None
			:a monitor which keeps track of the log list, and executes functions
			 associated with Event wrappers at there designated times
			
			@paramaters CPU must support threading, or have threads available for
						the use of this funciton
		'''
		#we will repeat this until the alarm is de-constructed
		while True:
			
			sleep(60) #repeat every 60 seconds, to check if an event happens every minute
			
			time_current = datetime.now() #find the current date and time to see if it matches any of the alarms
			
			#iterate over every element within the alarm list
			for event in self.log:
				
				#if the event is suppose to happen at the current time or has been missed
				#in the case of by a second or minute (maximum, sleep is every 60s)
				if (event.starts <= time_current):
					thread_temp = Thread(event.execute, args=()) #execute the function associated with the event class
					thread_temp.daemon(True)
					thread_temp.start()
		
	def _settup(self):
		'''
			(Alarm) -> (boolean)
			:this function is incharge of establishing a new dameonized thread which
			 will start monitoring all the Events added to the log and execute them
			 when it is the apropriate time
		'''
		thread_monitoring = Thread(self._monitor, args=())
		thread_monitoring.daemon(True)
		thread_monitoring.start()
		
	def __del__(self):
		'''
			(Alarm) -> (list of Events)
			:the de-constructor function for the Alarm class which stops the execution of
			 any further alarms that are 'queued' by the programmer
			
			@returns a list of Events that have not been executed yet
		'''
		return self.log