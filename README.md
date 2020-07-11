# SCMS Protocol ~ Secure Communication and Messaging Protocol

## Description

A (S)ecure (C)ommunication and (M)essaging (S)ervice is a lightweight tool for providing encrypted client-server messaging with path-routing features.

### Installation

	pip install quickscms==1.1.2

[To The Documentation ->](https://github.com/GabeCordo/scms-protocol/tree/master/docs)

* TCP Socket Networking 
* Uses the GORM Markup Language
* Default asymmetric encryption (RSA keysets) and salting that can be toggled
* Out of the box packet-routing (tor-like) capabilities for message-origin concealment
	1. Relays
	2. Entry/Exit Nodes
	3. Indexing Server (Creating IP-ID Account related pairs)
* Customizable Traffic Receivers/Transfer Routines

## Documentation
The documentation covers the various aspects being introduced with the SCMP including advanced concepts relating to 
high-level security and mock tor-like relaying.

## GORMarkup
[GORM](https://github.com/GabeCordo/rust-gorm) is an object-relational markup language with built in data-encapsulation and quick data-manipulation.

## Extensions

### Manakin
Manakin is a secure messenger implemented using the SCMS Protocol and is the officially supported messenger of the protocol.

## Credits

scms-p
> Gabriel Cordovado

	Functionality of all classes are not limited to this README, I encourage your to view the source :octocat:
