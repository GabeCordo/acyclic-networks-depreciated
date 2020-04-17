/*
* the following code is a string parser for a bitstream received by a python socket
* @returns the message, request type, status, or location based on the respective req
* 0, 1, 2, 3 as located in the bitstream b'[msg][req type][status][location/userid]'
* @example the bitsream b'<test<!000!?0?^1000^' is received by the function with
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
	Status, //whether the server should relay to another server or to client
	Location //the userid associated with the the receivers ip-address
}

fn handler(datat: DataType, c: char, req: u32) -> (Option<char>, DataType) {
	use self::DataType::*;
	match (datat, c, req) {
		(Default, '<', _req) => (None, Message),
		(Default, '!', _req) => (None, Request),
		(Default, '?', _req) => (None, Status),
		(Default, '^', _req) => (None, Location),
		(Default, _other, _req) => (None, Default),
		(Message, '<', _req) => (None, Default),
		(Message, _other, 0) => (Some(_other), Message),
		(Message, _other, _req) => (None, Message),
		(Request, '!', _req) => (None, Default),
		(Request, _other, 1) => (Some(_other), Request),
		(Request, _other, _req) => (None, Request),
		(Status, '?', _req) => (None, Default),
		(Status, _other, 2) => (Some(_other), Status),
		(Status, _other, _req) => (None, Status),
		(Location, '^', _req) => (None, Default),
		(Location, _other, 3) => (Some(_other), Location),
		(Location, _other, _req) => (None, Location)
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