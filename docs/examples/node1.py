from quickscms.network.node import Node
from quickscms.types import containers

from os.path import abspath
from time import sleep

addresses = containers.Addresses(
	ip='', 
	port=1052
)

FILE_PATH = abspath(__file__)[:-8]

paths = containers.Paths(
	directory_key_public = FILE_PATH + 'keys/public1.pem',
	directory_key_private =  FILE_PATH + 'keys/private1.pem',
	directory_file_logging = FILE_PATH + 'index/json/log_node1.json'
)

options = containers.Customizations(
	supports_console_cout=True,
	supports_backup_ip=False
)

n1 = Node(
	container_addresses = addresses,
	container_paths = paths,
	container_customizations = options
)
n1.settup()

while True:

		sleep(0.01) #stop the cpu from constantly running at 100% cpu
		
		if (n1.sizeOfQueue() > 0):
			
			bitsream_received = n1.deQueue()
			
			print(bitsream_received)
		