#####################################
#		Client-Side Requests
#####################################
from quickscmp.utils import caching

##		Whitelist Functions		##

def pullWhitelist(directory):
	'''
		(string) -> (list of strings)
		
		@returns a list of strings where each index represents a user-id
				 that have been approved to send messages to the clientx
		@exceptions returns an empty list if the directory is invalid
	'''
	__caching = caching.fileHandler(directory)
	return __caching.lookupCachedFile('whitelist')
def addWhitelist(directory, id_user):
	'''
		(string, string) -> (boolean)
		
		@returns boolean true if the element was successfully added
		@exception returns boolean false if the element was not added
	'''
	__caching = caching.fileHandler(directory)
	return __caching.appendCachedFile('whitelist', id_user)
def removeWhitelist(directory, id_user):
	'''
		(string, string) -> (boolean)
		
		@returns boolean true if the element was successfully removed
		@exception returns boolean false if the element was not removed
	'''
	__caching = caching.fileHandler(directory)
	return __caching.deleteCachedElement('whitelist', id_user)

##		Blacklist Functions		##

def pullBlacklist(directory):
	'''
		(string) -> (list of strings)
		
		@returns a list of strings where each index represents a user-id
				 that have been blocked from sending messages to the client
		@exceptions returns an empty list if the directory is invalid
	'''
	__caching = caching.fileHandler(directory)
	return __caching.lookupCachedFile('blacklist')
def addBlacklist(directory, id_user):
	'''
		(string, string) -> (boolean)
		
		@returns boolean true if the element was successfully added
		@exception returns boolean false if the element was not added
	'''
	__caching = caching.fileHandler(directory)
	return __caching.appendCachedFile('blacklist', id_user)
def removeBlacklist(directory, id_user):
	'''
		(string, string) -> (boolean)
		
		@returns boolean true if the element was successfully removed
		@exception returns boolean false if the element was not removed
	'''
	__caching = caching.fileHandler(directory)
	return __caching.deleteCachedElement('blacklist', id_user)

##		Pending-File Functions		##

def pullPending(directory):
	'''
		(string) -> (boolean)
		
		@returns a list of strings where each index represents a user-id
				 that is waiting to be added to the whitelist or blacklist
		@exceptions returns an empty list if the directory is invalid
	'''
	__caching = caching.fileHandler(directory)
	return __caching.lookupCachedFile('pending')
def addPending(directory, id_user):
	'''
		(string, string) -> (boolean)
		
		@returns boolean true if the element was successfully added
		@exception returns boolean false if the element was not added
	'''
	__caching = caching.fileHandler(directory)
	return __caching.appendCachedFile('pending', id_user)
def removePending(directory, id_user):
	'''
		(string, string) -> (boolean)
		
		@returns boolean true if the element was successfully removed
		@exception returns boolean false if the element was not removed
	'''
	__caching = caching.fileHandler(directory)
	return __caching.deleteCachedElement('pending', id_user)

##		Chat History Functions		##

def pullChatHistory(directory, id_user):
	'''
		(string, string) -> (boolean)
		
		@returns a list of strings where each index represents a message
				 received from the specified user-id that has been cached
		@exceptions returns an empty list if the directory is invalid
	'''
	__caching = caching.fileHandler(directory)
	return __caching.lookupCachedFile(id_user)
def addChatHistory(directory, id_user, message):
	'''
		(string, string) -> (boolean)
		
		@returns boolean true if the element was successfully added
		@exception returns boolean false if the element was not added
	'''
	__caching = caching.fileHandler(directory)
	return __caching.appendCachedFile(id_user, message)
def deleteChatHistory(directory, id_user):
	'''
		(string, string) -> (boolean)
		
		@returns boolean true if the element was successfully removed
		@exception returns boolean false if the element was not removed
	'''
	__caching = caching.fileHandler(directory)
	return __caching.deleteCachedFiled(id_user)
	
def transferPending(directory, id_user, location):
	'''
	'''
	pass
	
def splitter(request):
	'''
		(string) -> (list of strings)
	'''
	return request.split(' ')