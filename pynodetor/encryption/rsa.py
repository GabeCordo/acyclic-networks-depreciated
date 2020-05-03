###############################
#		python imports
###############################
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
import base64

###############################
#		   main code
###############################
#an out-of the box and easy to use object-oriented RSA encryption handler for developers
#to implement end-to-end encryption within socket communication
class Handler:
	def __init__(self, directoryKeyPrivate, directoryKeyPublic):
		'''
			(Handler, string, string) -> None
			:constructor function of the end-to-end encryption handler
			
			@paramaters directories must point to a valid path
		'''
		##class variables##
		self.directoryKeyPrivate = directoryKeyPrivate
		self.directoryKeyPublic = directoryKeyPublic
		
		#check to see that the directories given for the encryption keys are valid
		try:
			#check the private key pathway
			pathwayCheck = open(directoryKeyPrivate, 'r')
			pathwayCheck.close()
			#check the public key pathway
			pathwayCheck = open(directoryKeyPublic, 'r')
			pathwayCheck.close()
		except:
			raise FileNotFoundError('RSA Key Error: one or more key paths are invalid')
			
		##instance variables
		self._privateKey = ''
		self._publicKey = ''
	
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
		#Open the file containing the private key and store in the class instance variable
		try:
			keyPrivate = open(directoryKeyPrivate, 'rb').read()
			self._privateKey = RSA.importKey(keyPrivate)
		except:
			raise Exception(f'There was a problem restoring the private key: check if the directoryKeyPrivate path is valid or that the file is not empty')
		#Open the file containing the public key and store in the class instance variable
		try:
			keyPublic = open(directoryKeyPublic, 'rb').read()
			self._publicKey = RSA.import_key(keyPublic)
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
			keyPrivate = key.export_key()
			toPrivateKeyFile = open(self.directoryKeyPrivate, 'wb')
			toPrivateKeyFile.write(keyPrivate)
			toPrivateKeyFile.close() #close the file handler
			self._privateKey = keyPrivate
		except Exception as e:
			print(e)
			#raise Exception(f'There was a problem creating a private key: check if the directoryKeyPrivate path is valid')
		#generate a new public key, store it in the placeholder variable and place it into the directory
		try:
			keyPublic = key.publickey().export_key()
			toPublicKeyFile = open(self.directoryKeyPublic, 'wb')
			toPublicKeyFile.write(keyPublic)
			toPublicKeyFile.close() #close the file handler
			self._publicKey = keyPublic
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
	
	def encrypt(self, message, keyPublic):
		'''
			(Handler, string, string) -> (string)
			:transforms a plain text into a cyhpher text
			
			@paramaters no value for a password will leave it as an empty string
			@default keyPublic defaults to your public keys path for debugging
		'''
		#python doesn't like us using self declarations in the default tab so in case we are given an
		#empty keyPublic field we need to adhere to using our own publicKey for default testing possibly
		if ( keyPublic == '' ):
			keyPublic = self._publicKey
		cypherRSA = RSA.importKey(keyPublic)
		cypherRSA = PKCS1_OAEP.new(cypherRSA)
		#encrypt the given message using a given (or our own) public RSA key 
		messageBase64 = base64.b64encode( message.encode('ascii') ) #text needs to be in base64 to be encrypted
		return cypherRSA.encrypt( messageBase64 )
	
	def decrypt(self, cyphertext):
		'''
			(Handler, string) -> (string)
			:transforms a cypher text into a plain text
		'''
		cypherRSA = RSA.importKey(self._privateKey)
		cypherRSA = PKCS1_OAEP.new(cypherRSA)
		decryptedMSG = cypherRSA.decrypt(cyphertext)
		return base64.b64decode( decryptedMSG ).decode()
	
	def __eq__(self, other):
		'''
			(Handler) -> (boolean)
			:compares two encryption handlers and compares them based on directories
			
			@returns boolean true if both directories are the same
			@exception returns boolean false if the directories are not the same
		'''
		#check to see if the public key directories are the same
		if (self.directoryKeyPublic != other.directoryKeyPublic):
			return False
		#check to see if the private key directories are the same
		elif (self.directoryKeyPrivate != other.directoryKeyPrivate):
			return False
		#they are the same; all checks have passed
		return True