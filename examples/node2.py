from quickscmp.sockets.node import Node

n2 = Node(
	ip='',
	port=1053,
	directory_key_public='keys/public2.pem',
	directory_key_private='keys/private2.pem',
	directory_file_logging='index/json/log_node2.json',
	supports_console_cout=True,
	supports_backup_ip=False
)
n2.settup()

pk = n2.handler_keys.getPublicKey().decode()
message1 = f'2:bob~{pk}~127.0.0.1'
message2 = f'3:bob~127.0.0.1'


result = n2.send('127.0.0.1', message2, 1052)
print(result)