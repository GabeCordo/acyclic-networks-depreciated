#####################################
#		   Python Imports
#####################################

from os import remove

#####################################
#	   fileHandler for Caching
#####################################

class fileHandler:
	
	def __init__(self, directory):
		self.directory = directory
	
	def generatePath(self, id_user):
		'''
			(fileHandler, string) -> (string)
			
			@paramaters a non-empty string is provided
			@returns a modified pathway where the user-id message data
					 should have been cached if created properly
			@exception if an empty-string is provided, the pathway will
					   not be created an an empty string will be returned
		'''
		#a valid user-id cannot be an empty-string
		if (id_user == ''):
			return id_user
		
		path = (self.directory
				+ id_user
				+ '.txt')

		return path

	def writeCachedFile(self, id_user, message=''):
		'''
			(fileHandler, string, string) -> (boolean)
			
			@paramaters provided a non-empty string as a user-id
			@returns boolean true if a new cached-file is created
			@exception returns boolean false if the file-exists or the
					   pathway is corrupt or invalid
		'''
		path = self.generatePath(id_user)
		
		try:
			file_manage = open(path, "w+")
			file_manage.write(message)
			file_manage.close()
		except Exception as e:
			print(f'Console: caching experienced {e}')
			return False
		
		#no exceptions were encountered, run sucessful
		return True
		
	def lookupCachedFile(self, id_user):
		'''
			(fileHandler, string) -> (list of strings)
		
			@paramaters a user-id that is chached is provided
			@returns a list of strings, each index representing a new line
			@exception returns an empty list if the file doesn't exist
		'''
		path = self.generatePath(id_user)
		data = []
		
		try:
			file_manage = open(path, "r")
			data = file_manage.read().splitlines() #splits each line based on the '\n' opp.
			file_manage.close()
		except:
			return data #will return an empty list
			
		return data
		
	def lookupCachedFileString(self, id_user):
		'''
			(fileHandler, string) -> (string)
			
			@paramaters a user-id that is chached is provided
			@returns the cached file as a string
			@exception returns an empty string if the file doesn't exist
		'''
		return '\n'.join(self.lookupCachedFile(id_user))
	
	def lookupChachedFileElement(self, id_user):
		'''
			(fileHandler, string) -> (boolean)
			
			@paramaters none.
			@returns boolean true if the id_user is in the file
			@exception returns boolean false if it is not in the file
		'''
		try:
			temp_list = self.lookupCachedFile(id_user)
			temp_list.pop(id_user) #will error if it does not exist
		except:
			return False
		
		#if it did not error, the user-id must exist
		return True
			
	def appendCachedFile(self, id_user, message):
		'''
			(fileHandler, string, string) -> (boolean)
			
			@paramaters a valid user-id was provided
			@returns boolean true if the message paramater was
					 appended to the cache file
			@exceotion returns boolean false if the data was not
					   written
		'''
		path = self.generatePath(id_user)
		
		try:
			file_manage = open(path, "a")
			file_manage.write(message + '\n')
			file_manage.close()
		except Exception as e:
			print(f'Console: caching experienced {e}')
			return False
		
		#no exceptions were encountered, run sucessful
		return True
	
	def deleteCachedFiled(self, id_user):
		'''
			(fileHandler) -> (boolean)
			
			@return boolean true if the cache file was deleted
			@exception returns boolean false if the file was not
					   deleted from the cache folder
		'''
		path = self.generatePath(id_user)
		
		try:
			remove(path) #linked to os.remove
		except:
			return False
			
		#no exceptions were encountered, run sucessful
		return True
	
	def deleteCachedElement(self, id_user, element):
		'''
			(fileHandler) -> (boolean)
			
			@paramaters a valid user-id is provided
			@returns boolean true if the data embeded within the
					 cache file that matched the 'element' param
					 was exclusivly removed from the file
			@exception returns boolean false if the paramaters
					   were not met
					
			** if the element d.n.e will return true still **
		'''
		#grab the data currently stored within the cache file
		data = self.lookupCachedFile(id_user)
		i = data.index(element) #index the element we want to remove
		print(i)
		data.pop(i)
		
		path = self.generatePath(id_user)
		
		try:
			file_manage = open(path, 'w')
			for line in range(0, len(data)):
				file_manage.write(data[line]) #write the data back into the file
			file_manage.close()
		except:
			return False
		
		#no exceptions were encountered, run sucessful
		return True
	
	def __del__(self):
		'''
			(fileHandler) -> None
		'''
		pass