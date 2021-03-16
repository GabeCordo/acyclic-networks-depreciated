from quickscmp.sockets.node import Node
from quickscmp.utils import containers

from time import sleep

addresses = containers.Addresses(
ip, port [, ip_index [, ip_backup ]]
)

paths = containers.Paths(
directory_key_public, directory_key_private, directory_key_public
)

options = containers.Customizations(
[ encryption [, listening [, monitoring [, recovery [, supports_console_cout ]]]]]
)

n1 = Node(
	container_addresses = addresses,
	container_paths = paths,
	container_customizations = options
)

'''
	ip='',
	port=1052,
	directory_key_public='keys/public1.pem',
	directory_key_private='keys/private1.pem',
	directory_file_logging='index/json/log_node1.json',
	supports_console_cout=True,
	supports_backup_ip=False
'''

while True:

		sleep(0.01) #stop the cpu from constantly running at 100% cpu
		
		if (n1.sizeOfQueue() > 0):
			
			bitsream_received = n1.deQueue()
			
			print(bitsream_received)
		