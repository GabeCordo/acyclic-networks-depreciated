'''
	INTERFACE FOR PARSING RAW SERVER BITSTREAMS USING RUST
		-          DO NOT MODIFY THIS FILE          -
		
	*** hot-fixes a layer of rust on-top of the python codes 
	to handle performance issues with string-handling
	@returns the associated segment of the bitstream
	as requested by the class instance variables		***
'''

###############################
#	   quickscmp imports
###############################
from quickscmp.utils.errors import *
from cffi import FFI

###############################
#		   CONSTANTS
###############################

NUM_OF_RSV_CHARS = 7
MNEUMONIC_LENGTH = 3

MNEUMONIC_PAIRS = {
	'hsh': '#',
	'exe': '!',
	'amp': '@',
	'lbk': '<',
	'rbk': '>',
	'til': '~',
	'col': ':'
}

###############################
#		   main code
###############################
class Parser:
	
	def __init__(self, message=''):
		'''
			(String) -> (None)
			@conditions the bitstream used as the function argument,
						aka. the class parameters must be a valid
						syntactical statement according to the def.
						showed within the comments of the rust parser
		'''
		self.message = message
		
		self.ffi = FFI()
		self.lib = ffi.dlopen("stringparser/target/release/liblibstringparser.dylib")
		
	def get_restricted_chars():
		'''
		'''
		return MNEUMONIC_PAIRS
	
	def stripRestrictedChars(request):
		'''
		'''

		self.ffi.cdef('char* replaceCharacter(const char *n, int);')
		
		try:
			request_val = self.ffi.new('char[]', bytes(self.message.decode(), 'utf-8'))
			stream_modified = self.ffi.string(lib.parse(request_val, request)).decode('utf-8')
			
			return stream_modified
		except Exception as e:
			raise MismatchedSyntax()
		
	def stripMneumonics():
		'''
		'''
		self.ffi.cdef('char* replaceSubstitute(const char *n);')
		
		try:
			request_val = self.ffi.new('char[]', bytes(self.message.decode(), 'utf-8'))
			stream_modified = self.ffi.string(lib.parse(request_val)).decode('utf-8')
			
			return stream_modified
		except Exception as e:
			raise MismatchedSyntax()
		
	def parse(request):
		'''
		'''
		self.ffi.cdef('char* parse(const char *n, int);')
		
		try:
			request_val = self.ffi.new('char[]', bytes(self.message.decode(), 'utf-8'))
			stream_modified = self.ffi.string(lib.parse(request_val, request)).decode('utf-8')
			
			return stream_modified
		except Exception as e:
			raise MismatchedSyntax()
			
	def grouping_split(grouping):
		'''
			(string) -> (list of strings)
			@returns a string-split based on the '~' tilda character
					 for more efficient data-manipulation techniques
		'''
		return grouping.split('~')
	
	def message_format(message):
		'''
			(list of strings) -> (string)
			@returns a string concatenation of list indexes making up
					 the message body of the bitstream
		'''
		message = ';'.join(message)
		return f'<#{message}#>'
		
	def request_format(request):
		'''
			(int) -> (string)
			@returns a string representation of the request syntax block
					 for the specific data-block request
		'''
		return f'<?{request}?>'
		
	def pathway_format(pathways):
		'''
			(list of strings) -> (string)
			@returns a string concatenation of list indexes making up
					 the routing pathway for the bitsream
		'''
		pathways = ';'.join(pathways)
		return f'<^{pathways}^>'
		
	def exit_format(exit):
		'''
			(string) -> (string)
			@returns a string representation of the exit syntax, wrapping
					 the id-ip linker to the exit-node of the network
		'''
		return f'<@{exit}@>'
		
	def origin_format(origin):
		'''
			(string) -> (string)
			@returns a string representation of the origin syntax, the
					 the id-ip linker to the routing starting-point
		'''
		return f'<<{origin}<>'
		
	def destination_format(destination):
		'''
			(string) -> (string)
			@returns a string representation of the origin syntax, the
					 the id-ip linker to the routing ending-point
		'''
		return f'<>{destination}>>'
	
	def bitstream_format(message=[], request, pathways, ):
		'''
		'''
		return self.
		
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
			@returns the request embedded in the bitstream
			
			***		Shortcut for the pull function		***
		'''
		return self.pull(1)
		
	def get_relay_path(self):
		'''
			(None) -> (String)
			@returns the ids of the relay path
			
			***		Shortcut for the pull function		***
		'''
		return self.pull(2)
				
	def replace_paths(self, relays, exitnode):
		'''
			(None) -> (String)
			@returns a modified bitstream with the new modified pathways
			
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
		return self.pull(3)
		
	def get_origin_id(self):
		'''
			(None) -> (String)
			@returns the origin id embedded in the bitstream
			
			***		Shortcut for the pull function		***
		'''
		return self.pull(4)
		
	def get_target_id(self):
		'''
			(None) -> (String)
			@returns the target id embedded in the bitstream
				
			***		Shortcut for the pull function		***
		'''
		return self.pull(5)
		
	def __retr__(self):
		'''
			(None) -> (String)
			@returns a string representation of the class in the
					 form of the bitstream passed to it during the
					 the initialization of the class
		'''
		return self.message