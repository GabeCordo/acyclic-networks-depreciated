/*
* the following code is a string parser for a bitstream received by a python socket
* @returns the message, request type, status, or location based on the respective req
* 0, 1, 2, 3 as located in the bitstream b'[msg][req type][relay_pathway][exit_node][origin_userid][target_userid]'
* @example the bitsream b'#message#?request?^pathway^@exit@^<origin<>destination>' is received by the function with
* the request type '0', the returned string will be parsed into 'test'
*/

// Crate Imports

extern crate libc;
use libc::{c_char};
use std::ffi::CStr;
use std::ffi::CString;
use std::str;

// Enum Deffinitions

enum Identifier {
	Default,
	Wrapper,
	Substitute
}

#[derive(Copy, Clone)]
enum DataType {
	Default, //artificial NULL enum
	Message, //message from user to user
	Request, //pre-defined pathway
	Pathway, //an array of relay ip-addresses to mesh through the network
	Exit, //the exit nodes ip-address where the message will be sent to the destination
	Origin, //the userid associate with the senders ip-address
	Destination //the userid associated with the the receivers ip-address,
}

// Pattern Matching

fn handler_data(datat: DataType, c: char, req: u32) -> (Option<char>, DataType) {
	use self::DataType::*;
	match (datat, c, req) {
		(Default, '#', _req) => (None, Message),
		(Default, '?', _req) => (None, Request),
		(Default, '^', _req) => (None, Pathway),
		(Default, '@', _req) => (None, Exit),
		(Default, '<', _req) => (None, Origin),
		(Default, '>', _req) => (None, Destination),
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

fn handler_identifier(iden: Identifier, c: char, req: u32) -> (Option<char>, Identifier) {
	use self::Identifier::*;
	
	match (iden, c, req) {
		(Default, '<', _req) => (None, Wrapper),
		(Default, ':', _req) => (None, Substitute),
		(Default, _other, _req) => (None, Default),
		(Wrapper, '>', _req) => (None, Default),
		(Wrapper, _other, 0) => (Some(_other), Wrapper),
		(Wrapper, _other, _req) => (None, Wrapper),
		(Substitute, ':', _req) => (None, Default),
		(Substitute, _other, 1) => (Some(_other), Substitute),
		(Substitute, _other, _req) => (None, Substitute)
	}
}

// Public Crate Functions

#[no_mangle]
pub extern fn replaceSubstitute(bitstream: *const c_char) -> *mut c_char {
	let c_str: &CStr = unsafe { CStr::from_ptr(bitstream) };
	let str_slice: &str = c_str.to_str().unwrap();
	
	let mut iden = Identifier::Default;
	
	let mut temp_identifier = String::new();
	let mut processed_stream = String::new();
	
	for character in str_slice.chars() {
		let (output, new_state) = handler_identifier(iden, character, 1);
		
		if let Some(c) = output {
			temp_identifier.push(c);
			
			match temp_identifier.as_str() {
				"hsh" => {
					processed_stream.push('#');
					temp_identifier.clear();
				},
				"exe"  => {
					processed_stream.push('!');
					temp_identifier.clear();
				},
				"amp"  => {
					processed_stream.push('@');
					temp_identifier.clear();
				},
				"lbk" => { 
					processed_stream.push('<');
					temp_identifier.clear();
				},
				"rbk" => {
					processed_stream.push('>');
					temp_identifier.clear();
				},
				"ubk" => {
					processed_stream.push('^');
					temp_identifier.clear();
				},
				"til"  => {
					processed_stream.push('~');
					temp_identifier.clear();
				}
				"col"  => {
					processed_stream.push(':');
					temp_identifier.clear();
				},
				_other => {
					processed_stream.push(c);
				}
			}
		}
		
		iden = new_state;
	}
	
	let return_val = CString::new(processed_stream).unwrap();
	return return_val.into_raw();
}

fn check_bounds_and_syntax(str_slice: &str, processed_stream: &mut String, i: usize, mneumonic: &str) {
	if str_slice.len() > i+1 && str_slice.chars().nth(i+1) != Some('>') {
		processed_stream.push_str(mneumonic);
	}
}

#[no_mangle]
pub extern fn replaceCharacter(bitstream: *const c_char, choice: u32) -> *mut c_char {
	let c_str: &CStr = unsafe { CStr::from_ptr(bitstream) };
	let str_slice: &str = c_str.to_str().unwrap();
		
	let mut iden = Identifier::Default;
	let mut processed_stream = String::new();
	
	for (i, character) in str_slice.chars().enumerate() {
		let (output, new_state) = handler_identifier(iden, character, 0);
		
		if let Some(c) = output {
			match c {
				'#' => check_bounds_and_syntax(str_slice, &mut processed_stream, i, ":hsh:"),
				'!' => check_bounds_and_syntax(str_slice, &mut processed_stream, i, ":exe:"),
				'@' => check_bounds_and_syntax(str_slice, &mut processed_stream, i, ":amp:"),
				'<' => check_bounds_and_syntax(str_slice, &mut processed_stream, i, ":lbk:"),
				'>' => check_bounds_and_syntax(str_slice, &mut processed_stream, i, ":rbk:"),
				'^' => check_bounds_and_syntax(str_slice, &mut processed_stream, i, ":ubk:"),
				'~' => check_bounds_and_syntax(str_slice, &mut processed_stream, i, ":til:"),
				_other => processed_stream.push(c)
			}
		}
		
		iden = new_state;
	}
	
	let return_val = CString::new(processed_stream).unwrap();
	return return_val.into_raw();
}

#[no_mangle]
pub extern fn parse(bitstream: *const c_char, choice: u32) -> *mut c_char {
	let c_str: &CStr = unsafe { CStr::from_ptr(bitstream) };
	let str_slice: &str = c_str.to_str().unwrap();
	
	let mut data = DataType::Default;
	let mut iden = Identifier::Default;
	
	let mut processed_stream = String::new();
	
	for character in str_slice.chars() {
		let (output_iden, new_state_iden) = handler_identifier(iden, character, 0);
		
		if let Some(c1) = output_iden {
			
			let (output_data, new_state_data) = handler_data(data, c1, choice);
			if let Some(c2) = output_data {
				processed_stream.push(c2);
			}
			
			data = new_state_data
		}
		
		iden = new_state_iden;
	}
		
	let return_val = CString::new(processed_stream).unwrap();
	return return_val.into_raw();
}