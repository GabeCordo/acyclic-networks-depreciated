'''
	INTERFACE FOR PARSING RAW SERVER BITSREAMS USING RUST
		-          DO NOT MODIFY THIS FILE          -
		
	*** hotfixes a layer of rust on-top of the python codes 
	to handle performance issues with string-handling
	@returns the associated segment of the bitsream
	as requested by the class instance variables		***
'''

from cffi import FFI

class Parser:
	
	def __init__(self, message=''):
		'''
			(String) -> (None)
			@conditions the bitream used as the function argument,
						aka. the class paramaters must be a valid
						syntatical statement acording to the def.
						showed within the comments of the rust parser
		'''
		self.message = message
	
	def pull(self, request):
		'''
			(int) -> (String)
			@paramaters the request (int argument) must be a valid
						integer between 0 and 3 representing the
						various pieces of data present within the
						bitsream:
							a) int 0 : message (text)
							b) int 1 : request type (security type)
							c) int 2 : status (how far from target)
							d) int 3 : userids (origin/target ids)
			@returns the datatype associated with the integer provided
					 by the function argument
			@exception returns None type if an unsupported bitsream is
					   provided by the user
		'''
		ffi = FFI()
		lib = ffi.dlopen("stringparser/target/release/liblibstringparser.dylib")

		ffi.cdef('char* parse(const char *n, int);')
		
		try:
			request_val = ffi.new('char[]', bytes(self.message.decode(), 'utf-8'))
			stream_modified = ffi.string(lib.parse(request_val, request)).decode('utf-8')
			
			return stream_modified
		except Exception as e:
			return f'{e}: An Error Occured: unsupported bitsream was provided.'
	
	def get_message(self):
		'''
			(None) -> (String)
			@returns the message embedded in the bitsream
			***		Shortcut for the pull function		***
		'''
		return self.pull(0)
	
	def get_request_type(self):
		'''
			(None) -> (String)
			@returns the request embedded in the bitsream
			***		Shortcut for the pull function		***
		'''
		return self.pull(1)
	
	def get_relay_path(self):
		'''
			(None) -> (String)
			@returns the ids of the relay path
			***		Shortcut for the pull function		***
		'''
		origin_and_target_ids = self.pull(2)
		try:
			path_character_seperator = origin_and_target_ids.index('/')
			return origin_and_target_ids[:path_character_seperator]
		except:
			return 'An Error Occured: unsupported bitsream was provided'
			
	def replace_paths(self, relays, exitnode):
		'''
			(None) -> (String)
			@returns a modified bitsream with the new modified pathways
			***		Shortcut for multiple pull function		***
		'''
		message = self.get_message()
		request = self.get_request_type()
		origin = self.get_origin_id()
		final = self.get_target_id()
		return f'<{message}<!{request}!?{relays}/{exitnode}?^{origin}/{final}^'
	
	def get_exit_node(self):
		'''
			(Node) -> (String)
			@returns the exit node ip-address of the bitstream
			***		Shortcut for the pull function		***
		'''
		origin_and_target_ids = self.pull(2)
		try:
			path_character_seperator = origin_and_target_ids.index('/')
			return origin_and_target_ids[path_character_seperator+1:]
		except:
			return 'An Error Occured: unsupported bitsream was provided'
	
	def get_origin_id(self):
		'''
			(None) -> (String)
			@returns the origin id embedded in the bitsream
			***		Shortcut for the pull function		***
		'''
		origin_and_target_ids = self.pull(3)
		try:
			id_character_seperator = origin_and_target_ids.index('/')
			return origin_and_target_ids[:id_character_seperator]
		except:
			return 'An Error Occured: unsupported bitsream was provided'
	
	def get_target_id(self):
		'''
			(None) -> (String)
			@returns the target id embedded in the bitsream
			***		Shortcut for the pull function		***
		'''
		origin_and_target_ids = self.pull(3)
		try:
			id_character_seperator = origin_and_target_ids.index('/')
			return origin_and_target_ids[id_character_seperator+1:]
		except:
			return 'An Error Occured: unsupported bitsream was provided'
		
	def __retr__(self):
		'''
			(None) -> (String)
			@returns a string representation of the class in the
					 form of the bitsream passed to it during the
					 the initialization of the class
		'''
		return self.message