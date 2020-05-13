from pynodetor.sockets.node import Node

n1 = Node(
	ip='',
	port=1052,
	directory_key_public='keys/public1.pem',
	directory_key_private='keys/private1.pem',
	supports_backup_ip=False
)
n1.settup()

while True:
		
		if (n1.sizeOfQueue() > 0):
			
			bitsream_received = n1.deQueue()
			
			print(bitsream_received)
		