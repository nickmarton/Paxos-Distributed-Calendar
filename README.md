#Distributed Calendar application using the Paxos algorithm
---
##TODO:
* **UML**:
    * log attribute in Acceptor should be moved to Node to keep everything as decoupled as possible.
    * Proposer should not have attribute v; v is transient to a Proposer and only matters to an Acceptor
    * updates according to constructors of Proposer and Acceptor
    * Node needs attributes "log" and "calendar"
* **Code**
    * All TCP/UDP stuff
    * Need to decide on how to structure Node, then Proposer and Acceptor will follow