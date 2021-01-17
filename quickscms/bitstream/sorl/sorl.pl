#!/usr/bin/perl

use strict
use warnings
use Data::Dumper qw(Dumper);

print Dumper \@ARGV;

sub narrow_identifiers(@argument_list) {
	
	for (my$arg = 0; $arg<=$#VAR1; $arg++) {
		
		#the input-type of the SORL syntax is a string encapsulated by a ""
		if ($VAR1[$arg] == "-s") {
			
		}
		#the input-type of the SORL syntax is an external file with the .sorl postfix
		elsif ($VAR1[$arg] == "-f") {
			
		}
		#specify the identifier-object we are trying to read from
		elsif ($VAR1[$arg] == "--identifier") {
			
			$arg++;
			#insert a value into the specified identifier path
			# ... --identifier smith_family/bob/dob -i "2021/01/16"
			if ($VAR1[$arg] == "-i") {
				
				
			}
			#swap the next two argument values, we will care about type
			# ... --identifier smith_familt/bob/dob smith_family/tim/dob
			elsif ($VAR1[$arg] == '-s') {
				
			}
			#delete the value from the identifier pathway
			# ... --identifier smith_family/bob
			elsif ($VAR1[$arg] == "-d") {
				
			}
		}
		#perform an operation on two values currently existing within the markdown
		# ... -o [operator(s)] [path1-value] [path2-value]
		elsif ($VAR[$arg] == "-o") {
			narrow_operators()
		}
		#the argument cannot be understood by the interpreter
		else {
			print("SORL Error, the command either doesn't exist or is misused.")
		}
	}
}

sub narrow_specifiers(@argument_list) {
	
	#when swapping two types of variables, we won't care if they are either complex or string
	if ($VAR1[$arg] == "--ignore-type") {
		
	}
	#when performing any type of operation the privacy guard will be ignored, though this is dangerous
	elsif ($VAR1[$arg] == "--ignore-encapsualtor") {
		
	}
	#when the request is complete, we will output to the same file we were provided (if that was the case)
	elsif ($VAR1[$arg] == "--output-to-file") {
		
	}
	#when the request is complete, we will output to the console
	elsif ($VAR1[$arg] == "--output-to-console") {
		
	}
}

sub narrow_operators(@argument_list) {
	
	#concatinate two string together
	if ($VAR1[$arg] == ".") {
		
	}
	#start a substring of an element
	elsif ($VAR1[$arg] == "\$") {
	}
	#overwrite string 2, with string 1
	elsif ($VAR1[$arg] == "->") {
		
	}
	#overwrite string 1, with string 2
	elsif ($VAR1[$arg] == "<-") {
		
	}
	#capture the length of a string
	elsif ($VAR1[$arg] == "_") {
		
	}
	#capture the pathway of a current string
	elsif ($VAR1[$arg] == "&") {
		
	}
	#repeat a string n times
	elsif ($VAR1[$arg] == "*") {
		
	}
}