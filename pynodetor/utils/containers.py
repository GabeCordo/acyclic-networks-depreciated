class Addresses:
	def __init__(self, ip, port, ip_index, ip_backup):
		self.ip = ip
		self.port = port
		self.ip_index = ip_index
		self.ip_backup = ip_backup
		
class Keys:
	def __init__(self, key_public, key_private):
		self.key_public = key_public
		self.key_private = key_private

class Supports:
	def __init__(self, encryption, listening, monitoring, recovery):
		self.encryption = encryption
		self.listening = listening
		self.monitoring = monitoring
		self.recovery = recovery