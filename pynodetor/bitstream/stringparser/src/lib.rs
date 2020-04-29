/*
* the following code is a string parser for a bitstream received by a python socket
* @returns the message, request type, status, or location based on the respective req
* 0, 1, 2, 3 as located in the bitstream b'[msg][req type][relay_pathway][exit_node][origin_userid][target_userid]'
* @example the bitsream b'#message#?request?^pathway^@exit@^<origin<>destination>' is received by the function with
* the request type '0', the returned string will be parsed into 'test'
*/

extern crate libc;
use libc::{c_char};
use std::ffi::CStr;
use std::ffi::CString;
use std::str;

#[derive(Copy, Clone)]
enum DataType {
	Default, //artificial NULL enum
	Message, //message from user to user
	Request, //pre-defined pathway
	Pathway, //an array of relay ip-addresses to mesh through the network
	Exit, //the exit nodes ip-address where the message will be sent to the destination
	Origin, //the userid associate with the senders ip-address
	Desitnation //the userid associated with the the receivers ip-address,
}

fn handler(datat: DataType, c: char, req: u32) -> (Option<char>, DataType) {
	use self::DataType::*;
	match (datat, c, req) {
		(Default, '#', _req) => (None, Message),
		(Default, '?', _req) => (None, Request),
		(Default, '^', _req) => (None, Pathway),
		(Default, '@', _req) => (None, Exit),
		(Default, '<', _req) => (None, Origin),
		(Default, '>', _req) => (None, Desitnation),
		(Default, _other, _req) => (None, Default),
		(Message, '#', _req) => (None, Default),
		(Message, _other, 0) => (Some(_other), Message),
		(Message, _other, _req) => (None, Message),
		(Request, '?', _req) => (None, Default),
		(Request, _other, 1) => (Some(_other), Request),
		(Request, _other, _req) => (None, Request),
		(Pathway, '^', _req) => (None, Default),
		(Pathway, _other, 2) => (Some(_other), Pathway),
		(Pathway, _other, _req) => (None, Pathway),
		(Exit, '@', _req) => (None, Default),
		(Exit, _other, 3) => (Some(_other), Exit),
		(Exit, _other, _req) => (None, Exit),
		(Origin, '<', _req) => (None, Default),
		(Origin, _other, 4) => (Some(_other), Origin),
		(Origin, _other, _req) => (None, Origin),
		(Destination, '>', _req) => (None, Default),
		(Destination, _other, 5) => (Some(_other), Destination),
		(Destination, _other, _req) => (None, Destination)
	}
}

#[no_mangle]
pub extern fn parse(bitstream: *const c_char, choice: u32) -> *mut c_char {
	let c_str: &CStr = unsafe { CStr::from_ptr(bitstream) };
	let str_slice: &str = c_str.to_str().unwrap();
	
	let mut data = DataType::Default;
	let mut processed_stream = String::new();
	
	for character in str_slice.chars() {
			let (output, new_state) = handler(data, character, choice);
			
			if let Some(c) = output {
				processed_stream.push(c);
			}
			
			data = new_state;
		}
		
	let return_val = CString::new(processed_stream).unwrap();
	return return_val.into_raw();
}