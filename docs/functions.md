## Framework Documentation
As the framework is programmatically updated, primary functions and hooks can be found here. The goal being, to provide a quick-lookup spot for features that will assist in creating your decentralized architecture without needing to scrape through code. I encourage you to read over the documentation covering the overall-architectural decisions for classes and underlining functions as this document does not go beyond the scope of functionality.

---

#### 1.0 Bitstream

##### 1.1 Basic

* Instance Variables
    1. (String) request
    2. (String) data_primary
    3. (String) data_secondary
    4. (List of Strings) data_other

###### 1.1.1 __init__(self, message='')
The constructor class for the simple parser.  

*(Parser, string) -> None*  

###### 1.1.2 parse(self)
Using indexing, parses the pieces of data into the class variables.  

*(Parser) -> None*  

**@returns** nothing to the main program but initializes the class variables.  
**@exception** if an incorrect syntax is provided, throws MismatchedSyntax() Error.  

###### 1.1.3 getRequest(self)
The getter function for the messages request field.

*(Parser) -> (string)*  

**@returns** the request parsed from the message during initialization.  
**@exception** returns an empty string if invalid syntax was provided.  

###### 1.1.4 getPrimaryData(self)
The getter function for the messages primary data field.  

*(Parser) -> (string)*  

**@returns** the primary data parsed from the message during initialization.  
**@exception** returns an empty string if invalid syntax was provided.  
		

###### 1.1.5 getSecondaryData(self)
The getter function for the messages secondary data field.  

*(Parser) -> (string)*  

**@returns** the secondary data parsed from the message during initialization.  
**@exception** returns an empty string if invalid syntax was provided.  

###### 1.1.6 getOtherData(self)
The getter function for the messages other data field(s).  

*(Parser) -> (list of strings)*  

**@returns** any other data appended to the simple request as a list of strings.  
**@exception** returns an empty string if invalid syntax was provided.  
		
###### 1.1.7 __str__(self)
Returns a string representation of the class variables in the proper simple bitstream syntax.  

*(Parser) -> (string)*  

**@returns** a string representation of the class variables in the proper simple bitstream syntax.  

###### 1.1.8 __repr__(self)
Returns a string representation of the class type.  

*(Parser) -> (string)*  

**@returns** a string representation of the class type.  

---

#### 2.0 Encryption


##### 2.1 Type

###### 2.1.1 __init__(self, type_encryption, directory_key_private, directory_key_public)
Constructor function of the RSA Key Pair Class.  

*(Keys, Encryption, string, string) -> None*  

**@condition** directories must point to a valid path.  

###### 2.1.2 verifyPath(self)  
Checks whether the pathways provided are a valid key pair.  

*(Keys) -> None*  

**@returns** nothing reveals the key pairs are not corrupted.  
**@exception** throws MismatchedKeys() error.  

###### 2.1.3 getPublicKey(self)  
The getter function for the public encryption key.  

*(Keys) -> (string)*  
 
**@returns** the public encryption key.  

###### 2.1.4 getPrivateKey(self)  
The getter function for the private encryption key.  

*(Keys) -> (string)*  

**@returns** the private encryption key.  



##### 2.2 rsa

###### 2.2.1 __init__(self, directory_key_private=None, directory_key_public=None)    
Constructor function of the end-to-end encryption handler.  

*(Handler, string, string) -> None*  

**@parameters** directories must point to a valid path.   

###### 2.2.2 getPublicKey(self)  
The getter function for the public encryption key.  

*(Handler) -> (string)*  

**@parameters** a public key must exist.  
**@returns** the public key found within the placeholder variable.  
**@exception** returns an empty string if no key was generated or restored.  

###### 2.2.3 getPrivateKey(self)  
The getter function for the private encryption key.  

*(Handler) -> (string)*  

**@parameters** a private key must exist.  
**@returns** the private key found within the placeholder variable.  
**@exception** returns an empty string if no key was generated or restored.  

###### 2.2.4 restoreKeySet(self) 
Loads all public and private keys from text-files to class variables. 

*(Handler) -> (boolean)*  

**@parameters** keys must be pre-initialized within the file directories, password must be valid.  
**@returns** boolean true if the keys were transferred from file to instance variable.  
**@exception** returns boolean false if there was an issue (password likely INVALID).  

###### 2.2.5 generateKeySet(self)  
Creates a random private key deleting the old private key.

*(Handler) -> (list of strings)*  

**@returns** a list of keys: public at index [0], private at index [1].  

###### 2.2.6 formatForEncryption(self, message)  
Turns a string into a utf8 encoded string before using RSA.

*(Handler, string) -> (utf8 string)*  

**@returns** a utf8 encoded string for encryption.  

###### 2.2.7 encrypt(self, message, key_public)
Transforms the utf8 encoded string into an RSA cypher text.  

*(Handler, string, string) -> (string)*  

**@parameters** no value for a password will leave it as an empty string.  
**@default** keyPublic defaults to your public keys path for debugging.  


###### 2.2.8 decrypt(self, text_cyphered) 
Transforms the RSA cypher-text back into a plain-text using your private .pem key.  

*(Handler, string) -> (string)*  

###### 2.2.9 __eq__(self, other) 
The getter function for the private encryption key.  

*(Handler) -> (boolean)*  

**@returns** boolean true if both directories are the same.  
**@exception** returns boolean false if the directories are not the same.  



---

#### 3.0 Linker


##### 3.1 linkerTemplate

###### 3.1.1 __init__(self, *args)
The constructor function of the linkerJSON handler class takes in as many files as are required by the Node or element.  

*(Handler, n strings) -> None*  
 
**@exception** throws a FileNotFound() error if one or more of the files are not valid.

###### 3.1.2 template_push(self, dump_function)
Responsible for pushing the class dictionaries in data into the JSON files linearly.  

*(Handler, Markup Dump Function) -> None*  

**@exception** throws a FileNotFound() error if one or more of the files are not valid.  

###### 3.1.3 template_pull(self, load_function)
Responsible for pulling the data from the JSON files into the class dictionaries linearly.  

*(Handler, Markup Loader Function) -> None*  
 
**@exception** throws a FileNotFound() error if one or more of the files are not valid.  

###### 3.1.4 cleanerFunctionality(self, element) [HOOK]
Adds special functionality to the Markup updater file.    

*(Handler) -> None*  


###### 3.1.5 cleaner(self, timer)
Responsible for manipulating and pushing the dictionary data to the Markup files every 'timer' seconds.  

*(Handler) -> None*  


###### 3.1.6 startCleaner(self, timer)
Starts the cleaner, we want to avoid using it (wastes cpu thread) if we don't need it.  

*(Handler, int) -> None*  


##### 3.2 linkerJSON

###### 3.2.1 __init__(self, *args)
Constructor function for the JSON handler. This function allows any number of JSON files to be entered under args*.    

*(List of Strings) -> None*  

###### 3.2.2 push(self)
Pushes to the changes in the class dictionary to all the JSON files.  

*(self) -> None*  

###### 3.2.3 pull(self)
Pulls all the data within the JSON files that have been pushed as class parameters.  

*(self) -> None*  

##### 3.3 linkerYAML

###### 3.3.1 __init__(self, *args)
Constructor function for the YAML handler. This function allows any number of JSON files to be entered under args*.    

*(List of Strings) -> None*  

###### 3.3.2 push(self)
Pushes to the changes in the class dictionary to all the YAML files.  

*(self) -> None*  

###### 3.3.3 pull(self)
Pulls all the data within the YAML files that have been pushed as class parameters.  

*(self) -> None*  

---

#### 4.0 Routines

##### 4.1 Generator

###### 4.1.1 __init__(self, container_routine_author, container_routine_settings,container_addresses, container_paths, container_customizations)
The constructor function for the Routine generator. Required to initialize the various data-containers needed by the generator to create a proper route-line directory, furthermore creating holder-class variables for YAML and directory handlers.  

*(Routine, Addresses, Paths, Customizations) -> None*  

###### 4.1.2 _generate_template_routine(self, directory_root)
Copies the template for protocol routines found within the source code and creates a deep-copy in the directory provided as an argument to the function.  
		
*(Routine, String) -> None*  

###### 4.1.3 _dictionary_create_author(self)
Creates a YAML file for the author/routine information that does not effect the functionality of the.  

*(Routine) -> (boolean)*  

**@returns** boolean True if the YAML file was successfully created with the data in the containers passed as class arguments.  
**@parameters** the _generate_template_routine must have been called creating the blank directories and markup files.  

###### 4.1.4 _dictionary_create_config(self)
Creates a YAML file for the config information that effects the functionality of the routine being implemented.  

*(Routine) -> (boolean)*    

**@returns** boolean True if the YAML file was successfully created with the data in the containers passed as class arguments.  
**@parameters** the _generate_template_routine must have been called creating the blank directories and markup files.  

###### 4.1.5 _negate_custom_settings_bool(self)
Due to the verbose syntax, this is a form of syntactical sugar  to make the manipulation of this deep-data in the dictionary easily changeable.  

*(Routine) -> (None)*  

###### 4.1.6 _check_custom_settings(self)
If the use of custom settings are turned off, it will be turned on to true.

*(Routine) -> (None)*  

**@note** this function should be called at the call of any function adding custom content to make sure it is up-to-date.  

###### 4.1.7 add_custom_setting(self, identifier, Y)
Add an key-data pair to the custom-settings dictionary to the config file for storing information custom to the created routine.

*(String, Generic Y) -> (None)*  

**@parameters** the generic must be a primitive type supported by the YAML markup language.  

###### 4.1.8 add_script(self, script_name, directory_script)
Add a custom python script to the folder in the routine, these are to be called by the official python files.  

*(Routine, String, String) -> (None)*  

**@note** this custom directory will standardize the location for custom code that has been abstracted from the official scripts (this directory will be imported by default in all official python scripts).  

###### 4.1.9 add_markup(self, markup_name, markup_enum, directory_markup)
Add a custom markup file to the folder in the routine, this is for detailed data-sheets that ARE NOT CONFIG SETTINGS (Config settings are added to the official config yaml markup).  

*(Routine, String, RoutineSettings, String) -> (None)*  

###### 4.1.10 generate_new_routine(self, directory_root)
Creates a bare-bone routine (based off of the template within the library) and customizes the author and config sheets based on data passed to the class.  

*(Routine, String) -> (None)*  

##### 4.2 Handler

---

#### 5.0 Server

##### 5.1 cmd
##### 5.2 Console
##### 5.3 Container
##### 5.4 Protocol

---

#### 6.0 Sockets

##### 6.1 Node
##### 6.2 Balancer
##### 6.3 Entry
##### 6.4 Index
##### 6.5 Relay
##### 6.6 Exit

---

#### 7.0 Timing

##### 7.1 Alarm
##### 7.2 Event
##### 7.3 Stopwatch
##### 7.4 Timer

---

#### 8.0 Utils

##### 8.1 Authenticator
##### 8.2 Caching
##### 8.3 Containers
##### 8.4 Enums
##### 8.5 Logging
##### 8.6 Terminal