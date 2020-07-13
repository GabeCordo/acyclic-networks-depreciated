###############################
#		python imports
###############################
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from base64 import b64encode, b64decode

###############################
#		   main code
###############################
#an out-of the box and easy to use object-oriented RSA encryption handler for developers
#to implement end-to-end encryption within socket communication
class Handler:
	def __init__(self, directory_key_private=None, directory_key_public=None):
		'''
			(Handler, string, string) -> None
			:constructor function of the end-to-end encryption handler
			
			@paramaters directories must point to a valid path
		'''
		##class variables##
		self.directory_key_private = directory_key_private
		self.directory_key_public = directory_key_public
		
		#check to see that the directories given for the encryption keys are valid
		try:
			if (directory_key_private != None):
				#check the private key pathway
				check_pathway = open(directory_key_private, 'r')
				check_pathway.close()
			if (directory_key_public != None):
				#check the public key pathway
				check_pathway = open(directory_key_public, 'r')
				check_pathway.close()
		except:
			raise FileNotFoundError('RSA Key Error: one or more key paths are invalid')
			
		##instance variables
		self._privateKey = ''
		self._publicKey = ''
		
		self.restoreKeySet()
	
	def getPublicKey(self):
		'''
			(Handler) -> (string)
			:getter function for the classes public encryption key
			
			@paramaters a public key must exist
			@returns the public key found within the placehodler variable
			@exception returns an empty string if no key was generated or
					   restored
		'''
		return self._publicKey
	
	def getPrivateKey(self):
		'''
			(Handler) -> (string)
			:getter function for the classes private encryption key
			
			@paramaters a private key must exist
			@returns the private key found within the placehodler variable
			@exception returns an empty string if no key was generated or
					   restored
		'''
		return self._privateKey
	
	def restoreKeySet(self):
		'''
			(Handler) -> (boolean)
			:loads all public and private keys from text-files to class variables
			
			@paramaters keys must be pre-initialized within the file directories,
						password must be valid
			@returns boolean true if the keys were transfered from file to instance
					 var
			@exception returns boolean false if there was an issue (password likeley
					   INVALID)
		'''
		if (self.directory_key_private != None):
			#Open the file containing the private key and store in the class instance variable
			try:
				key_private = open(self.directory_key_private, 'rb')
				self._privateKey = key_private.read()
			except:
				raise Exception(f'There was a problem restoring the private key: check if the directoryKeyPrivate path is valid or that the file is not empty')
		if (self.directory_key_public != None):
			#Open the file containing the public key and store in the class instance variable
			try:
				key_public = open(self.directory_key_public, 'rb')
				self._publicKey = key_public.read()
			except:
				raise Exception(f'There was a problem restoring the public key: check if the directoryKeyPublic path is valid or that the file is not empty')
	
	def generateKeySet(self):
		'''
			(Handler) -> (list of strings)
			:creates a random private key deleting the old private key
			
			@paramaters none
			@returns a list of keys: public at index [0], private at index [1]
		'''
		key = RSA.generate(2048)
		#generate a new private key, store it in the placeholder variable and place it into the directory
		try:
			key_private = key.export_key()
			write_to_file = open(self.directory_key_private, 'wb')
			write_to_file.write(key_private)
			write_to_file.close() #close the file handler
			self._privateKey = key_private
		except Exception as e:
			print(e)
			#raise Exception(f'There was a problem creating a private key: check if the directoryKeyPrivate path is valid')
		#generate a new public key, store it in the placeholder variable and place it into the directory
		try:
			key_public = key.publickey().export_key()
			write_to_file = open(self.directory_key_public, 'wb')
			write_to_file.write(key_public)
			write_to_file.close() #close the file handler
			self._publicKey = key_public
		except:
			raise Exception(f'There was a problem creating a public key: check if the directoryKeyPublic path is valid')
	
	def formatForEncryption(message):
		'''
			(Handler, string) -> (utf8)
			:turns a string into a utf8 encryptable form for RSA
			
			@returns a utf8 encoded form for encryption
		'''
		if ( isinstance(message, int) ):
			return six.binary_type(message)
		for str_type in six.string_types:
			if isinstance(message, str_type):
				return value.encode('utf8')
		if ( isinstance(message, six.binary_type) ):
			return message
	
	def encrypt(self, message, key_public):
		'''
			(Handler, string, string) -> (string)
			:transforms a plain text into a cyhpher text
			
			@paramaters no value for a password will leave it as an empty string
			@default keyPublic defaults to your public keys path for debugging
		'''
		#python doesn't like us using self declarations in the default tab so in case we are given an
		#empty keyPublic field we need to adhere to using our own publicKey for default testing possibly
		if ( key_public == '' ):
			key_public = self._publicKey
		cypher_rsa = RSA.importKey(key_public)
		cypher_rsa = PKCS1_OAEP.new(cypher_rsa)
		#encrypt the given message using a given (or our own) public RSA key 
		message_base64 = b64encode(message.encode('ascii')) #text needs to be in base64 to be encrypted
		return cypher_rsa.encrypt(message_base64)
	
	def decrypt(self, text_cyphered):
		'''
			(Handler, string) -> (string)
			:transforms a cypher text into a plain text
		'''
		if (self.directory_key_private != None):
			cypher_rsa = RSA.importKey(self._privateKey)
			cypher_rsa = PKCS1_OAEP.new(cypher_rsa)
			text_plain = cypher_rsa.decrypt(text_cyphered)
			return b64decode( text_plain ).decode()
		else:
			return ''
	
	def __eq__(self, other):
		'''
			(Handler) -> (boolean)
			:compares two encryption handlers and compares them based on directories
			
			@returns boolean true if both directories are the same
			@exception returns boolean false if the directories are not the same
		'''
		#check to see if the public key directories are the same
		if (self.directory_key_public != other.directory_key_public):
			return False
		#check to see if the private key directories are the same
		elif (self.directory_key_private != other.directory_key_private):
			return False
		#they are the same; all checks have passed
		return True