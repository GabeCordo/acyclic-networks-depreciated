from quickscms.network.node import Node
from quickscms.types import containers

from os.path import abspath

addresses = containers.Addresses(
	ip='', 
	port=1053
)

FILE_PATH = abspath(__file__)[:-8]

paths = containers.Paths(
	directory_key_public = FILE_PATH + 'keys/public2.pem',
	directory_key_private =  FILE_PATH + 'keys/private2.pem',
	directory_file_logging = FILE_PATH + 'index/json/log_node2.json'
)

options = containers.Customizations(
	supports_console_cout=True,
	supports_backup_ip=False
)

n2 = Node(
	container_addresses = addresses,
	container_paths = paths,
	container_customizations = options
)
n2.settup()

pk = n2.handler_keys.getPublicKey().decode()
message1 = f'2:bob~{pk}~127.0.0.1'
message2 = f'3:bob~127.0.0.1'


result = n2.send('127.0.0.1', message2, 1052)
print(result)