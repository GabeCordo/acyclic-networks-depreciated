import json

def settup(directoryJSON):
	'''(string) -> (boolean)
		:imports the JSON data required for the controlled tor network
		
		@returns boolean true if the JSON data was extracted correctly
		@exception returns boolean false if the directory was broken
	'''
	try:
		dataFile = open(directoryJSON, 'r')
		#initialize the JSON data into a multi-dimentional list under the name 'network'
		#all data can be extracted from this given the settup function is called
		network = json.load(dataFile)
	except:
		#there was most likley something wrong with the directory if this fails or JSON Syntax
		return False
	#JSON was successfuly extracted into the multidimentional list
	return True
	