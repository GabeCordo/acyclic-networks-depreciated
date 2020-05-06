###############################
#	   pynodetor imports
###############################
from pynodetor.encryption import rsa
from pynodetor.utils import enums, errors

###############################
#		   main code
###############################
class Keys:
	def __init__(self, type_encryption, directory_key_private, directory_key_public):
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
			if (self.type_encryption == enums.Encryption.RSA):
				
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
			raise MismatchedKeys()
			
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