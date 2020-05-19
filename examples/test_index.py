from pynodetor.sockets.index import Index
from time import sleep

index = Index(
	ip = '',
	port = 1052, 
	directory_key_private = 'index/private/private.pem',
	directory_key_public = 'index/private/public.pem',
	directory_index = 'index/json/index.json',
	directory_log = 'index/json/log.json',
	directory_collected_keys = 'index/keys/'
	)
index.settup()

while True:
		
		sleep(0.01) #stop the cpu from constantly running at 100% cpu
		#keep the program running to test the listener