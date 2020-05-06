from random import randrange

def generate():
	'''
		None -> (string)
		@returns a randomized string of alphanumerical and decimal
				 characters of 20 bits of length
	'''
	new_auth_key = list(str(randrange(10**20, 10**21)))
	for i in range(0, 10, 2):
		rand_char = chr(randrange(65, 122))
		new_auth_key[i] = str(rand_char)
	return ''.join(new_auth_key)