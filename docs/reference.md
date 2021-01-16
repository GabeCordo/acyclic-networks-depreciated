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
        1. Containers
	2. Basic Sockets
		1. Handshake
		2. Data Transfer
	3. Syntax
		1. Basic Syntax
		2. Advanced Syntax
    4. Enums
	5. Routing
	6. Shotgunning
    7. Decentralized Storage
2. [Error Handling](#Error-Handling)
    1. Response Codes
    2. Offical Framework Errors
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

---

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

### Routing

![Packet Routing](https://github.com/GabeCordo/scms-protocol/blob/master/docs/diagrams/flow.png)
The above diagram is a simplified overview of the routing procedure, segmented into identifiable zones used by reponse codes of the protocol post-completion.  

#### Preliminary Phase
The preliminary-phase comprises of computationaly intesive node operations that maintain the security and anonymous nature of the connected routing network. Hence, the nodes within this ficitcoious-region are controlled by the SCMS team, meaning that 3rd-party nodes installed on possibly unsecure devices do not have control over the business-logic regions of the routing protocol.  

##### Balancers (BL)
The notion of a blancer should be trivial, (in essence) the purpose being to: (1) conceal the origin-ip of the entry nodes that communicate with the indexers, (2) reduce the traffic flow into any given entry-gateway, and (3) allow for non-critical nodes to be easily changable over an interval of n-time.

It is important to not confuse balancers as being the entry-way into the SCMS routing network. While they are the first node within the routing segment, they do not contribute to computing routing-pathways or verifying requests (which are done by entries and indexers dicussed in the next segments). They are incharge of distributing traffic to entries with a lower request-queue and mitigating overload attempts by devices attempting to connect to the network. In later of the framework, balancer nodes were also in-charge of enforcing the "advanced-syntax" used by SCMS, dropping connections that have attempted to queue invalid requests.

###### Node Requirments
1. Concealing the Origin-IP of Entries
- Origin-IPs are the only nodes with authorization to contact the Indexers.
- Avoid making the IPs of nodes that control logical-functionalities public.
- If the Entries-IP is concealed, traffic cannot be snooped to find the Indexers-IP. 
2. Reducing Traffic Flow into Entires
- Nodes (by default) monitor for queue overloads, reduces the chance of entries being forced to dump/ignore requests.
- Balancers maintain a manifest of all traffic flowing into each entry, Entries with reduced-traffic are preffered for request processing.
3. Balancer Swapping
- The balancers are non-crictial with respect to network logic as they act as relays into the network. This means that they can be swapped, retired, or added onto the network without needing to distrupt SCMS logical functionality.

##### Entries (EN)
Entries are the first logical-component of the network, alternativly reffered to as "entry-gateways" or "entry-nodes" into the SCMS. Unlike balancers, these are logically-intensive components that: (1) receive validated request from balancers, (2) pattern-match the request to a given routine, (3) request a pathway, entry, or retreival from an Indexer, and (4) send the processed request with routing-headers into the network. Entries are the glue or "conductors" that mitigate the responisbilites of nodes at all layers of the SCMS, hence, why it is important to maintaing there anonyminity with balancers. If an entry is leaked or discovered by an individual, the network is not compramised but the node must be retired to risk snooping for connections to Indexers, Route-Stops, etc.

##### Indexers (IN)
Indexers are the heart of data-collection within the network. Similar to a Certificate Authority, there origional operations was to monitor IP-ID associations the have been logged, and their associative public-keys to facilitate "pathways" to follow within the advanced-syntax. This responisiblity has been expanded to observing the ongoing pathways of packets and verifying each received packet is from an "ordered" routing-phase node. This will be described in further detail under the packet-relay section of this documentation.

###### Indexers Designation
Both designations must be paired in order to communicate sensitive data in a P2P transmision. 
1. ID-IP Association Authority (IDP)
- Handle requests for ID/IP lookups, insertions, and deletions.
- Maintiain an Public-Key association to an ID that is used to protect information to them or protect the IP they must send a packet too in the next sequence of the route. This is so that the next IP in the routing sequence can be seen by the ID that must transmit the packet.
- Generate new pathways 
2. Pathway Verification Authority (PAT)
- Once a node has received a packet, they will verify the origin of the packet is apart of the Pathway given by the ID-IP Association.
- NOTE: while it may seem the PAT has less-respinsibilites, it must facilitate verifications with N nodes of a given pathway. This is a significant increase in-contrast to a IDP with one-transmition per pathway

#### Routing Phase
The routing phase revolves around the transfer of encoded SCMS blocks using the encrypted pathway enforced by the indexer. This involves the process of decrypting the next ip-address located within the pathway segment of the block and sending a verification request with the indicated PAT attached to the pathway segment.

##### Route-Stop (RN)
Each SCMS block is segments into various sections holding vital information for the routing process. This data is encrypted primarly because a RN can be any 3rd-party device permiting the network to make data-passing operations through their device. This allows the network to grow expedentially, allowing more complex routing techniques, and a truly decentralized network of pathways. 

* Operations of a Route-Stop
    1. Store de-centralized data that has been requested by the system.
    2. Open a port to permit 3rd-party traffic to be anonymized.

###### Decentralized Data Storage [future]
Each device will have the ability (once implemented) to store encrypted portions of 3rd-party data on there device. In a simillar fasion of creating pathways to route traffic, these pathways are used to "store" byte-segments of an encrypted stream on multiple devices. In the case of a node breach, without knowledge of the entire pathway or encryption key the data cannot be decyphered. 

* Note, devices that wish to store data-decentralized must also permit other users to do the same.

#### Post-Transfer Phase
The post-transfer phase implies the final transfer of the SMCS encoded-block. This involves transfering a data-packet from the 3rd-party network of devices, to an officialy controlled node that acts as an exit gateway to the messages final destination.

#### Exit(EX)
The exit node is a final assurance that a 3rd-party route-stop node has not been established in order to snoop on traffic destinations. This means all traffic being received from the SCMS system comes from a secure server, the IP of your device is never revealed to any non-trusted member of the network. In saying this, it is important exit nodes change frequently as to reduce the posibility of known exit-node IPs being breached. As the exit node is essentailly just an officially controlled Route-Stop, they can easily be added, swapped, or deleted from the network. 

* an Indexer node will have an updated list of exit nodes to place into a encoded pathway

### Verificiation
![VerificationProcedure](https://github.com/GabeCordo/scms-protocol/blob/master/docs/diagrams/pat.png)
A hash of the messages: (1) route-stop id and (2) timestamp is created before the transfer from one pathway point to another. This is appended to the end of an encoded SCMS block and then extracted by the received route-stop and verified by the PAT encoded into the pathway. The PAT will then: (1) ensure the route-stop id was chosen as the next destination id and (2) verify the time between transfers does not exceed a time that might indicate a delayed or intercepted transfer. This is the method of authentication currently being implemented into the SCMS.

* A packet injected to appear as if it originated from the network will be detected as fradulant as either the encoded pathway will be missing a CAT-ID or the CAT will not be able to verify it signed off on the transfer.

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

---

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

### Response Codes
These will be added during the next documentation update.

---

### Shotgunning <span style="color:blue">*[future]*</span>
The process of sending messages over a pre-determined interval with independent routed paths. This will make
the transfer of one message look like a spider-web of pathways instead of a linear path.

### Decentralized Storage <span style="color:blue">*[future]*</span>
The protocol plans to not only let individuals send data over a network but store data within the relays that
it has initialized, the idea is to make it harder for breaches to obtain entire data-blocks.

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

### Enums

##### Nodes
Represents the official nodes of the scms protocol.

0. NODE
1. ENTRY
2. RELAY
3. EXIT
4. INDEX
5. BALANCER

##### Encrypted
Represents whether the node supports asymetric encryption or not.

0. DISABLED
1. ENABLED

##### Listening
Represents whether the node supports listening or is intented only for sending packets.

0. DISABLED
1. ENABLED

##### Encryption
Represents the type of encryption the node is currently supporting, allowing for routines to adopt various encryption algorithms depending on the level of security required.

0. RSA
1. AES

##### DataTransfer
For the use of Node networks, represents the complexity of data-routing.

* basic - A "middle-man" node is used to transfer packets between two clients to avoid P2P comms.
* advanced - Supports full path-routing between gateway and relay nodes, for more information read the data-transfer section of this documentation.

0. BASIC
1. ADVANCED

##### OfficialMarkups
These represent the official enums supported by the framework for use within routine for storing data-sets specific to there use case, though it is possible to use others.

0. JSON
1. YAML
2. GORM

### Standard Port

### Blueprint Node

### Clearance Levels 
 
0. no authentication required
1. known IP + logged ID
2. passphrase required
3. passphrase + known IP/ID required

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