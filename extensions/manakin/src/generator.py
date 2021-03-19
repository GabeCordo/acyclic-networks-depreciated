'''
	USERID GENERATOR FOR IP MATCHING ON THE INDEX NODE
	-     Accompany the alphanumerical name 		 -
	-   	with a randomized 6-bit digit  	         -
	
	Default input/output class initializations:
		
	#import generator
	#userid = generate(custom_alpha)
'''

from random import randint

def userid(custom_alpha):
	'''(string) -> (string)
		:concatenates a 6-digit random id to ensure that the userid
		 is not re-used amongst various users
		
		@paramaters a string with only alphanumerical characters
		@returns a userid for the messenger
		@exception returns an empty string if the params are not met
	'''
	#check to see if the provided id contains only alphanumerical characters
	if ( custom_alpha.isalpha() == False ):
		return ''
	#create a random 6-bit digit
	new_digit = randint(100000,1000000)
	#return the generated user-id
	return custom_alpha + ":" + str(new_digit)
	