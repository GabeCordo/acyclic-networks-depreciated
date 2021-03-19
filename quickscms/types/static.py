## --------------------------------------------------------------------------------

from quickscms.types.enums import Options

class Option():
	def __init__(self, option: Options, description: str):
		'''
		'''
		self.option = option
		self.description = description
	def is_valid(self):
		'''
		'''
		return not(self.option == None)
	def __eq__(self, other: Options) -> bool:
		'''
		'''
		if (other == None):
			return False
		if (type(other) != type(Options)):
			return False
		if (self.option != Options):
			return False
		return True
	def __repr__(self) -> str:
		'''
		'''
		return f'Option({self.option})'
	def __str__(self) -> str:
		'''
		'''
		return f'{self.option}: {self.description}'

## --------------------------------------------------------------------------------

from quickscms.types.enums import RequestCode

class Request():
	def __init__(self, ip: str, cipher: str, rsa_pub: str, plaintext: str,
				 authentication: str, nonce: str, request: RequestCode
		):
		'''
		'''
		self.ip = ip
		self.request = request
		self.rsa_pub = rsa_pub
		self.cipher = cipher
		self.plaintext = plaintext
		self.authentication = authentication
		self.nonce = nonce
	
	def serialize(self) -> dict:
		'''
		'''
		return {
			'ip': self.ip,
			'req': self.request,
			'metdata': {
				'rsa': self.rsa_pub,
				'auth': self.authentication,
				'nonce': self.nonce
			},
			'data': {
				'cipher': self.cipher,
				'plain': self.plaintext
			}
		}

	def unserialize(self, json_dic) -> None:
		'''
		'''
		self.ip = json_dic['ip']
		self.request = json_dic['req']
		self.rsa_pub = json_dic['metdata']['rsa']
		self.cipher = json_dic['data']['cipher']
		self.plaintext = json_dic['data']['plain']
		self.authentication = json_dic['metdata']['auth']
		self.nonce = json_dic['metdata']['nonce']

	def __eq__(self, other):
		'''
		'''
		if (other == None): return False
		if (type(other) != type(Request)):  return False
		if (self.nonce == other.nonce):
			return True
		return False

	def __str__(self):
		'''
		'''
		return (f'ip:{self.ip}\nrequest:{self.request}\nauth:{self.authentication}\n'
			 + f'nonce:{self.nonce}\n{self.rsa_pub}\n{self.cipher}\n{self.plaintext}'
		)

	def __repr__(self):
		'''
		'''
		return f'Request({self.ip}, {self.request}, {self.nonce})'

## --------------------------------------------------------------------------------

from time import ctime, strftime

class Log():
	def __init__(self, message: str, description: str, 
				 request: Request, latency: int 
		):
		'''
		'''
		self.message = message
		self.description = description
		self.request = request
		self.time = ctime()
		self.latency = latency
	
	def serialize(self) -> dict:
		'''
		'''
		return {
			'msg': self.message,
			'des': self.decription,
			'data': {
				'req': self.request,
				'time': self.time,
				'lat': self.latency
			}
		}

	def unserialize(self, json_dic) -> None:
		'''
		'''
		self.message = json_dic['msg']
		self.description = json_dic['des']
		self.request = json_dic['data']['req']
		self.time = json_dic['data']['time']
		self.latency = json_dic['data']['lat']
	
	def __eq__(self, other) -> bool:
		'''
		'''
		if (other == None): return False
		if (type(other) != type(Log)):  return False
		if (self.request == other.request):
			return True
		return False

	def __str__(self) -> str:
		'''
		'''
		return f'({self.time}:{self.request}) {self.message}\n{self.description}\n{str(self.request)}'

	def __repr__(self) -> str:
		'''
		'''
		return f'Log({self.time}, {self.request})'


## --------------------------------------------------------------------------------

class Event():
	def __init__(self, generic, title, description, starts, ends, function=None, repeat=False):
		'''
			(Event, Generic, string, datetime, datetime, object, boolean) -> None
			:the constructor class for events that are scheduled on callenders
			 or on alarms using the quickscms system
			
			@paramaters the types must be respected indicated above
		'''
		self.generic = generic
		self.title = title
		self.description = description
		self.starts = starts
		self.ends = ends
		self.function = function
		self.repeat = repeat
	
	def linkFunction(self, new_function_p) -> bool:
		'''
			(None) -> (Boolean)
			:links an external function to the event by passing it as a first class var

			@returns true if the function was successfully linked
			@exception will return false if there is a failure or it is previously defined
		'''
		if (self.function == None):
			return False
		self.function = new_function_p
		return True

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
		
	def serialize(self) -> dict:
		return {
			'metadata': {
				'generic': str(self.generic),
				'title': self.title,
				'description': self.description
			},
			'starts': str(self.starts),
			'ends': str(self.ends),
			'func': str(self.function),
			'repeat': self.reapeat
		}

	def unserialize(self, json_dic) -> None:
		self.generic = json_dic['metadata']['generic']
		self.title = json_dic['metadata']['title']
		self.description = json_dic['metadata']['description']
		self.starts = json_dic['starts']
		self.ends = json_dic['ends']
		self.function = None
		self.repeat = int(json_dic['repeat'])
		

## --------------------------------------------------------------------------------

from quickscms.crypto import rsa
from quickscms.types import enums, errors

class Keys:
	def __init__(self, type_encryption: enums.EncryptionScheme, directory_key_private: str, directory_key_public: str):
		'''
			(Keys, Encryption, string, string) -> None
			:constructor function of the RSA Key Pair Class
			
			@paramaters directories must point to a valid path
		'''
		##class variables##
		self.type_encryption = type_encryption
		self.directory_key_private = directory_key_private
		self.directory_key_public = directory_key_public
		
		##check keys##
		self._publicKey = ''
		self._privateKey = ''
		self.verifyPath() #verify the are not corrupted
	
	def verifyPath(self):
		'''
			(Keys) -> None
			:checks whether the pathways provided are a valid key pair
			
			@returns nothing reveals the key pairs are not corrupted
			@exception throws MismatchedKeys() error
		'''
		try:
			if (self.type_encryption == enums.EncryptionScheme.RSA):
				
				#use the directory of the public key to encrypt a test message
				h = rsa.Handler(self.directory_key_private, self.directory_key_public)
				message = 'test keys'
				encrypted = h.encrypt(message, h.getPublicKey())
				
				#check if the original message and the decryption match
				if (message == h.decrypt(encrypted)):
					#if so, we can push them to the class variables and stop the funciton
					self._publicKey = h.getPublicKey()
					self._privateKey = h.getPrivateKey()
		except:
			raise errors.MismatchedKeys()
			
	def getPublicKey(self):
		'''
			(Keys) -> (string)
			:the getter function for the public encryption key
			
			@returns the public encryption key
		'''
		return self._publicKey
		
	def getPrivateKey(self):
		'''
			(Keys) -> (string)
			:the getter function for the private encryption key
			
			@returns the private encryption key
		'''
		return self._privateKey

	def serialize(self) -> dict:
		return {
			'encryption-type': str(self.type_encryption),
			'private-key': self.directory_key_private,
			'public-key': self.directory_key_public
		}

	def unserialize(self, json_dic) -> None:
		if (json_dic['encryption-type'] == 'EncryptionScheme.RSA'):
			self.type_encryption = enums.EncryptionScheme.RSA
		self.directory_key_private = json_dic['private-key']
		self.directory_key_public = json_dic['public-key']

## --------------------------------------------------------------------------------

class AVLTreeNode():
	
	def __init__(self, key, val=None, balance_factor=0):
		self.key = key
		self.val = val
		self.left = None
		self.right = None
		self.parent = None
		self.balance_factor = balance_factor
		self.height = 1
		

## --------------------------------------------------------------------------------