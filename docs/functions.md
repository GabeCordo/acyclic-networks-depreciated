## Framework Documentation
As the framework is programmatically updated, primary functions and hooks can be found here. The goal being, to provide a quick-lookup spot for features that will assist in creating your decentralized architecture without needing to scrape through code. I encourage you to read over the documentation covering the overall-architectural decisions for classes and underlining functions as this document does not go beyond the scope of functionality.

---

#### 1.0 Bitstream

##### Basic

* Instance Variables
    1. (String) request
    2. (String) data_primary
    3. (String) data_secondary
    4. (List of Strings) data_other

###### __init__
* parameters
    1. message

* returns: 
* exception: 

###### parse

* parameters
    1. self

###### getRequest

* parameters

##### nrm

---

#### 2.0 Encryption

##### 2.1 Type
##### 2.2 rsa

---

#### 3.0 Linker

##### 3.1 linkerTemplate
##### 3.2 linkerJSON
##### 3.3 linkerYAML

---

#### 4.0 Routines

##### 4.1 Generator
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