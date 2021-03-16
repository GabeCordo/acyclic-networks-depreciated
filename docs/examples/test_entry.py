from pynodetor.sockets.entry import NodeEntry

entry = NodeEntry(
	ip = '',
	port = 1052,
	ip_index = '',
	ip_backup = '',
	directory_key_private = '',
	directory_key_public = ''
	)
entry.settup()

while True:
	
		sleep(0.01) #stop the cpu from constantly running at 100% cpu
		#keep the program running to test the listener
