#####################################
#		 Output Handler
#####################################

def handler(client, ip, request):
	'''
		(NodeRelay, string) -> (string)
	'''
	status_code = client.send(ip, request)
	
	if (status_code == '' or status_code == '1'):
		output = (f'Console: The request({request}) failed.\n'
				  + f'-> Sent to the open node({ip}).')
	else:
		output = (f'Console: The request({request}) was successful.\n'
				  + f'-> Returned({status_code})')
				
	print(output)
