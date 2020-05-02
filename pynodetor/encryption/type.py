###############################
#	   pynodetor imports
###############################
from pynodetor.encryption import rsa
from pynodetor.utils import enums, errors

###############################
#		   main code
###############################
class Keys:
	def __init__(self, encryptionType ,directoryKeyPrivate, directoryKeyPublic):
		'''(Keys, Encryption, string, string) -> None
			:constructor function of the RSA Key Pair Class
			
			@paramaters directories must point to a valid path
		'''
		##class variables##
		self.encryptionType = encryptionType
		self.directoryKeyPrivate = directoryKeyPrivate
		self.directoryKeyPublic = directoryKeyPublic
		
		##check keys##
		self._publicKey = ''
		self._privateKey = ''
		self.verifyPath() #verify the are not corrupted
	
	def verifyPath(self):
		'''(Keys) -> None
			:checks whether the pathways provided are a valid key pair
			
			@returns nothing reveals the key pairs are not corrupted
			@exception throws MismatchedKeys() error
		'''
		try:
			if (self.encryptionType == enums.Encryption.RSA):
				
				#use the directory of the public key to encrypt a test message
				h = rsa.Handler(self.directoryKeyPrivate, self.directoryKeyPublic)
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
		'''(Keys) -> (string)
			:the getter function for the public encryption key
			
			@returns the public encryption key
		'''
		return self._publicKey
		
	def getPrivateKey(self):
		'''(Keys) -> (string)
			:the getter function for the private encryption key
			
			@returns the private encryption key
		'''
		return self._privateKey