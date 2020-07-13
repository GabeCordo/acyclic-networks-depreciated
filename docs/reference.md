#Secure Communication and Messaging Protocol

# Table of Contents
1. [Theory](#example)
	1. Node
	2. Basic Sockets
		1. Handshake
		2. Data Transfer
		3. Error Handling
	3. Syntax
		1. Basic Syntax
		2. Advanced Syntax
		3. Object Relational Markup
	4. Routing
	5. Shotgunning
    6. Decentralized Storage
2. [Error Handling](#example2)
    1. Response Codes
3. [Routines](#third-example)
4. [Data Sheet](#fourth-examplehttpwwwfourthexamplecom)
	1. Standard Port
	2. Blueprint Node
	3. Entry Node
	4. Indexing Node

## Theory



### Node



### Basic Sockets



#### Handshake

#### Data Transfer

#### Error Handling



### Syntax



#### Basic Syntax

#### Advanced Syntax

#### Object Relational Markup

### Routing

### Shotgunning

### Decentralized Storage



## Error Handling


### Response Codes



## Routines



## Data Sheet



### Standard Port

### Blueprint Node

### Entry Node

Function | Request | Parameters | Bitstream
------------ | ------------- |  ------------- | -------------
lookupIndex | 0 | UserID | 0:UserID~None
addIndex | 2 | UserID; connecting-ip | 2:UserID~None
deleteIndex | 3 | UserID; connecting-ip | 3:UserID~None
sendMessage | 4 | UserID; TargetID | 4:TargetID~Message

### Indexing Node

Function | Request | Parameters | Bitstream
------------ | ------------- |  ------------- | -------------
lookupIndex | 0 | UserID | 0:UserID~None
lookupIP | 1 | UserIP   | [Not Callable]
addIndex | 2 | UserID; connecting-ip | 2:UserID~None
deleteIndex | 3 | UserID; connecting-ip | 3:UserID~None
sendMessage | 4 | UserID; TargetID | 4:TargetID~Message