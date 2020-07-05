from pynodetor.sockets import entry

entry = entry.NodeEntry(
	ip = '',
	port = 8075,
	ip_index = '167.99.178.6',
	ip_backup = '',
	directory_key_private = 'keys/private.pem',
	directory_key_public = 'keys/public.pem'
)

entry.settup()

#for i in range (0, 10):
#	print( entry.isThreadOneRuning() )