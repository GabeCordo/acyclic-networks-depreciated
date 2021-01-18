#!/usr/bin/perl
package parser;
#Parser.pm

use strict;
use warnings;
use utils;

my %parsed_text = ();

sub run {
	my ($bitstream, $known_identifier) = @_;
	
	foreach $char (split //, $bitsream) {
		
		if ($char = "(") {
			@metadata = utils::encapsulate_identifier();
			$bistream = substr $bitsream, @metadata[2];
			%parsed_text{@metadata[0]} = @metadata[1];
		}
	}
	return @output_list;
}

sub pull {
	
}

sub push {
	
}

sub swap {
	
}

1;