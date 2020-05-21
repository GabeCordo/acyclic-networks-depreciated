from pynodetor.sockets.node import Node

n2 = Node(
	ip='',
	port=1053,
	directory_key_public='keys/public2.pem',
	directory_key_private='keys/private2.pem',
	supports_backup_ip=False
)
n2.settup()

pk = n2.handler_keys.getPublicKey().decode()
message = f'8:bob'


result = n2.send('159.89.120.107', message, 8075)
print(result)