from pynodetor.sockets.node import Node

n2 = Node(
	ip='',
	port=1053,
	directory_key_public='keys/public2.pem',
	directory_key_private='keys/private2.pem',
	supports_backup_ip=False
)
n2.settup()

result = n2.send('127.0.0.1', 'testing', 1052)
print(result)