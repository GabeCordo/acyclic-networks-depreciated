#!/usr/bin/perl

package utils;
#Utils.pm

use strict;
use warnings;

sub encapsulate_string {
	my ($bitsream) = @_;
	
	$flag = 0;
	$count = 0;
	$final_string = "";
	foreach $char (split //, $bitstream) {
		
		if ($char == "\"") {
			if ($flag == 2) {
				break;
			}
			$flag = 2;
		}
		elsif ($flag == 2) {
			$final_string = $final_string . $char;
		}
		$count++;
	}
	return ($final_string, $count);
}

sub encapsualate_complex {
	my ($bitsream) = @_;
	
	$flag = 0;
	$count = 0;
	$index_string = "";
	@final_complex = [];
	foreach $char (split //, $bitstream) {
		
		if ($flag == 2) {
			if ($char == ",") {
				push(@final_complex, $index_string);
			}
			if ($char == "]") {
				push(@final_complex, $index_string);
				break;
			}
			$index_string = $index_string . $char;
		}
		elsif ($char == "[") {
			$flag = 2;
		}
	}
	return [@final_complex, $count];
}

sub encapsulate_block {
	my ($identifier, $block_segment) = @_;
	
	%block = ($identifier, ());
	#0 : identifier, 1 : type, 2 : encapsulator, 3 : data, 4 : post-data
	$state = 0;
	#0 : string, 1 : complex
	$type = 0;
	
	$data = "";
	$identifier = "";
	foreach $char (split //, $block_segment) {
		
		#we are still looking for the identifier
		if (%state = 0) {
			if ($char == ":") {
				%block{$data} = ();
				$identifier = $data;
			}
		}
		#we are looking for the type of data that's going to be stored
		elsif (%state = 1) {
			if ($data == "string") {
				$type = 0;
			}
			elsif ($data == "complex") {
				$type = 1;
			}
		}
		#we are looking for the encapsualtor attached to the data
		elsif (%state = 2) {
			if ($char == "@") {
				%block{$identifier}{"enc"} = "public";
				$state = 3;
			}
			elsif ($char == "%") {
				%block{$identifier}{"enc"} = "protected";
				$state = 3;
			}
			elsif ($char == "!") {
				%block{$identifier}{"enc"} = "private";
				$state = 3;
			}
		}
		#we are looking to see if anymore identifiers exist within the block
		elsif (%state = 3) {
			
			@metadata = [];
			#we want to store a string type
			if ($type = 0) {
				@metadata = encapsulate_string(substr $block_segment, $count);
			}
			#we want to store a complex (list) type
			elsif ($type = 1) {
				@metadata = encapsulate_complex(substr $block_segment, $count);
			}
			%block{$identifier}{"data"} = @metadata[0];
			$block_segment = @metadata[1];
		}
		elsif ($state = 4) {
			
			if ($char == ",") {
				%state = 0;
			}
			elsif ($char == "}") {
				break;
			}
		}
		$data = $data . $char;
		$count++;
	}
	return [%block, $count];
}

sub encapsulate_identifier {
	my ($bitsream) = @_;
	
	$count = 0;
	$identifier = "";
	@metadata = [];
	foreach $char (split //, $bitsream) {
		
		if ($char == ")") {
			@metadata = encapsulate_block(substr $bitsream, $count)
			break;
		}
		$identifier = $identifier . $char;
		$count++;
	}
	return [$identifier, @metdata[0], @metdata[1]];
}

1;