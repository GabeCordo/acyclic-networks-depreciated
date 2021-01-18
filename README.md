# SCMS Protocol ~ Secure Communication and Messaging Protocol

## Description

A (S)ecure (C)ommunication and (M)essaging (S)ervice is a lightweight framework at the application layer of the OSI model. Promoting the use of decentralized architectures involving messaging, data-storage, and API-requests.

* TCP Socket Networking 
* Uses the SORL (Syntax) Language
* Default asymmetric encryption (RSA keysets) and salting that can be toggled
* Out of the box packet-routing (tor-like) capabilities for message-origin concealment
	1. Relays
	2. Entry/Exit Nodes
	3. Indexing Server (Creating IP-ID Account related pairs)
* Customizable Traffic Receivers/Transfer Routines

### Installation

	pip install quickscms==1.1.6

### Further Reading

* [Documentation](https://github.com/GabeCordo/scms-protocol/tree/master/docs/reference.md)
* [Framework](https://github.com/GabeCordo/scms-protocol/tree/master/docs/functions.md)
* [Server-Setup](https://github.com/GabeCordo/scms-protocol/tree/master/extensions/manakin/docs/server.md)

## Extensions

### SORL
[Segment Oriented Routing Language](https://github.com/GabeCordo/scms-protocol/tree/master/extensions/sorl) is a (simplistic) syntactical structure for encapsulating encoded-data required for segmented("stage") routing blocks. 

* [Documentation] (https://github.com/GabeCordo/scms-protocol/tree/master/extensions/sorl/docs/markdown.md)

### Manakin
[Manakin](https://github.com/GabeCordo/scms-protocol/tree/master/extensions/manakin) is a command-line interface for interacting with the SCMS frameworks built-in server tools. This allows nodes, traffic-managements, logging, scheduling, and events to be initialized with minimal overhead.

* [Documentation] (https://github.com/GabeCordo/scms-protocol/tree/master/extensions/manakin/docs/server.md)

## Credits

scms-p
> Gabriel Cordovado

* Functionality of all classes are not limited to this README, I encourage your to view the source
