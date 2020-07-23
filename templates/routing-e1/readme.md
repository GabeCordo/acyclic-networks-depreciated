# Secure Messaging Protocol Routine

The (S)ecure (C)ommunication and (M)essaging (S)ervice is a lightweight tool for providing encrypted client-server messaging with path-routing features. Routines are an extensible feature integrated into the protocol that allow developers to open-source there modifications to the
original protocol that are designed to securely-transfer data for various purposes.

All official routines can be found on the scmp web-page and are reviewed by the protocol team to ensure the security and anonymity enforced
by the protocol is neither diminished or faulty.

The edits made locally to a pre-developed routine are at the developers risk holding neither the protocol team or routine developer reliable
for the foreseen or unforeseen resulting errors. Furthermore, developers should include the standard readme.md template for all routines to provide
the appropriate data to downloaders.

1. The 'author.yaml' sheet provides the appropriate information regarding the developer and routine
2. the 'config.yaml' establishes boolean configurations and other modifications required by the routine
3. Individual python scripts extend the functionality of the Node base class and are subject to intellectual property laws independent of the protocols open-source nature.
4. The path folder standardizes the location of encryption keys and log files required by the protocol. This is required rather than the storage of these files on arbitrary locations in the machine.

Any questions pertaining to this routine should be directed towards the developer of the routine indicated within the 'author.yaml' file as the  protocol group has no affiliation with the independent routines developed using it's open-source code.

---