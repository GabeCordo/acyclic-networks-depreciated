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
print(pk)
message1 = f'2:bob~{pk[6:]}~127.0.0.1'
message2 = f'3:bob~127.0.0.1'


result = n2.send('127.0.0.1', message1, 1052)
print(result)

print(n2.handler_keys.getPublicKey())