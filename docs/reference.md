# Secure Communication and Messaging Protocol
The (S)ecure (C)ommunication and (M)essaging (S)ervice is a lightweight tool for 
providing encrypted client-server messaging with path-routing features. Initial development
and planning began in September 2019 and has been progressively growing with weekly updates.
Version 1.0 was released May 8, 2020 bringing stable, encrypted messaging for socket nodes. The current
focus within the development process is increasing the reliability of the protocol and releasing
a stable routing scheme.

    Developed by Gabriel Cordovado

---

# Table of Contents
The protocol can be broken up into the respective categories of Theory, Error Handling, Routines and Data
Sheets to assist developers in building applications. Some sections may be either labeled as deprecated or
future, it is important to be attentive to these labels to avoid tricky errors. 

1. [Theory](#Theory)
	1. Node
	2. Basic Sockets
		1. Handshake
		2. Data Transfer
	3. Syntax
		1. Basic Syntax
		2. Advanced Syntax
	4. Routing
	5. Shotgunning
    6. Decentralized Storage
2. [Error Handling](#Error-Handling)
    1. Response Codes
3. [Routines](#Routines)
4. [Data Sheet](#Data-Sheet)
	1. Standard Port
	2. Blueprint Node
	3. Entry Node
	4. Indexing Node

---

## Theory
The process of obscuring data-transfer pathways has become an effective method in providing anonymity over networks.
SCMP has been designed to support packet-routing on-top of standard encryption for developers that wish to protect
the locations and identities of users. In a general overview of how the protocol works, a grouping of "primary" sockets 
establish entry and exit gates to a dynamic collection of relay sockets. This can increase in complexity with the
introduction of balancing sockets but this will not be discussed until section 4 which examines more complex situations
of how network traffic is routed. The entire network is reliant on an indexing server or database which is responsible for
the collection of: ip, associative-id and public-RSA of registered sockets on the network. The role of the indexing socket
is to create partially-randomized pathways for data-transfer requests and encrypt segments of data based on the socket which
is responsible for interpreting the information. The various segments of the network are encrypted differently, this will
be discussed in depth in section 1.2.2 in data-transfer. Departing from the initial protocol, the SCMP allows for minimized
networks that take advantage for the indexing socket to provide standard associative-id messaging rather than peer-to-peer
messaging in applications such as Skype which exposes user-IPs to strangers.

### Node
The node referred to as "socket" till now, is the parent class of all specialized nodes within the SCMP. This means that
the node class does not implement advanced features such as network-routing nore does any individual socket as that is
achieved through the collaboration of a network of nodes or what will be discussed later: entries, relays, indexers and 
exits. The node class provides fundamental templates for standard implementations: sending/receiving data, asynchronous
encryption, message queues, and primitive packet-spamming filters. Therefore, it is the job of the Node to provide out-
of-the-box security and not anonymity or sudo-anonymity.

* Required Parameters
    1. ip
    2. port = *8075*
    3. ip_index
    4. ip_backup
    
* Node Encryption
    1. directory_key_private
    2. directory_key_public
    
* Customizable Features
    1. supports_encryption = *true*
    2. supports_listening = *true*
    3. supports_monitoring = *true*
    4. supports_backup_ip = *true*


* Children of Node
    1. Balancer
    2. Entry
    3. Relay
    4. Exit

### Basic Sockets
The role of the standard socket is to the accept incoming requests and send data-packets
to other sockets


#### Handshake

![Standard Hanshake](https://github.com/GabeCordo/scms-protocol/blob/master/docs/diagrams/transfer.png)

1. Connection
    * initializes the FTP connection, a confirmation is sent to the connecting node that communication
      has been securely established.
2. Pre-Transfer
    * the node acting as the "server" will send a packet containing the public RSA Key(if encryption is enabled)
    and timing information (latency between each data-packet transfer).
    * if the "client" node receives a RSA public key, one will be sent back.
3. Transfer
    * "client" node sends the request and parameters to the "server" node.
4. Post-Transfer
    * any response codes or data-packets will be sent from the "client" to "server" node.

#### Data Transfer
Request and Response packet transfer is not always a strait-forward task. When dealing with routing packets
over a complex network the notions of packet-loss (The Two General's Problem) and over-sized plain-texts need
to come into account during the design process.

* Packet Loss
We can experience packet-loss as a result of compensating for over-sized plaint-text issues and low-internet speeds. 
    * scmp implements the error code **2** which is thrown when packet-transfer exceeds 5 seconds. 
    * the timeout value can be changed as the parameter latency-timeout

* Over-sized Plaintext

RSA Encryption requires plaintext to be maximum 256 bytes long, if the plaintext exceeds the byte length
we need to break-up the text into various packets and encrypt them individually. As a result, the protocol
requires an N number of data-packet transfers concluded by an end of transfer (EOT) characters '<<'. If the
latency between each socket is not the same, we can run into errors.

-> Valid Transfers

Node | Trial 1 | Trial 2 | Trial 3 | Trial 4 |
------------ | ------------- | ------------- | ------------- | ------------- |
client | 0.026 | 0.027 | 0.02788 | 0.01796
server | 0.00122 | 0.0018 | 0.00144 | 0.00119233

-> Invalid Transfers

Node | Trial 1 | Trial 2 |
------------ | ------------- | -------------
client | 0.029129 | 0.02327
server | 0.082100 | 0.03383

What we can conclude from the data-set is that if the logged latency by the server (used to determine the interval
to read packets) exceeds the logged latency by the client, we experience a packet-loss and run into errors.
**There is a redesign in the process to deprecate the EOT method and send latency-data through the pre-transfer
phase of the transfer.**

### Syntax
The protocol supports two forms of syntax: basic and advanced. Taking the approach that there is no
one solution to fit all circumstances, the use of either syntax is dependent on the use-case. It is 
encouraged to use the basic syntax for packets that transfer small variants of data to avoid the use
of a more expensive markup language.

#### Basic Syntax <span style="color:red">*[deprecated]*</span>
A simple syntax for formatting parameters around a hard-coded request within the node, it is planned
to be deprecated in future updates when a more flexible "advanced syntax" is released.

`` request:primary~secondary~...``
#### Advanced Syntax
Using a simple markup language written in Rust, the markup language provides a looser syntax (as
not elements must be present other than the reserved characters for the field). The goal is to make
it easier for both the programmer and program to understand the contents of packet through character-labels.

`` #message#?request?^pathway^@exit@<origin<>target>``

The design goal of the markup language was to provide intuitive mnemonics and characters to represent the various
elements found within the network packet.

### Routing

![Packet Routing](https://github.com/GabeCordo/scms-protocol/blob/master/docs/diagrams/flow.png)

### Shotgunning <span style="color:blue">*[future]*</span>
The process of sending messages over a pre-determined interval with independent routed paths. This will make
the transfer of one message look like a spider-web of pathways instead of a linear path.

### Decentralized Storage <span style="color:blue">*[future]*</span>
The protocol plans to not only let individuals send data over a network but store data within the relays that
it has initialized, the idea is to make it harder for breaches to obtain entire data-blocks.

## Error Handling
The secure communication and messaging protocol implements various fail-safes that prevent processing failures when
interpreting request codes.

* scmp implements the following fail-safes
    1. request data-transfer
    2. processing data
    3. response data-transfer

### Response Codes
Response code's are built in to assist the developer in debugging possibly faulty code or requests that
do not return any values.

Code | Response | Details
------------ | ------------- |  -------------
0 | General Failure | There was a failure in the Connection or Pre-Transfer Phase.
1 | Successful | There were no issues, a response was either sent or not.
2 | Transfer Failure | There was a failure in the Transfer or Post-Transfer Phase.

---

## Routines <span style="color:blue">*[future]*</span>
Routines are packages of socket configurations, routing standards and data-manipulation scripts for the modification of standard
SCMP Parent Nodes. The standardization of these packages for the protocol allows for plug and play (PnP) solutions that require little
or no intervention by developers which require the use of modified routines.

### author sheet (YAML)
The author sheet is a standard data-sheet holding information pertaining to the developer and routine that can be used to log information
independent of the routines functionality.

The information required on all author sheets follows:
1. Developers First and Last Name
2. Site the Routine is publicly available
3. Date of the routines creation
4. The name of the routine
5. the current version of the routine package
6. a short description on the functionality and purpose of the routine
7. the licence associated with the routine for further modification/fair-use

### config sheet (YAML)
The config sheet is a configuration data-sheet for socket configuration and routing standards. The config sheet must contain the data
required parameters outlined within the SCMP Parent Node containers: Addresses, Paths and Customizations.

    The config sheet is flexible to additional configurations settings that must be outlined within the 'custom' section of the sheet.
    The routines class responsible for the creation/interpretation of the YAML sheets will store the additional information under the
    dictionary key 'custom'. It is the responsibility of scripts to utilize this within their python code.

#### scripts directory (.PY)
The scripts directory provides specialty functions for handling data-manipulation of packets stored within the queue

#### path directory (.N)
Outlines a standard location for where confidential information should be held on the local machine that is used by the routine.

---

## Data Sheet
This portion of the documentation highlights the parameters of each parent/child class required
during the initialization phase.

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