# Segment Oriented Routing Language
The network routing markdown is a simple text format for advanced 

### Reserved Characters
The following characters cannot be used within the syntax-wrappers in order to
avoid possible parsing errors. As a result, the markup provides mnemonic substitutes to avoid
any conflicts.

---

#### Char : Mnemonic
2. '!' : 'exe'
3. '@' : 'amp'
4. '%' : 'mod'
7. ':' : 'col'
8. '(' : 'ids'
9. ')' : 'ide'
10. '{' : 'bls'
11. '}' : 'ble'
12. ',' : 'cma'
13. '"' : 'qte'

___

### Syntax Structure

```
(metadata) {
    request: string @ "",
    exit: string @ "",
    origin: string @ "",
    target: string @ "",
}
(blockdata) {
    pathway: complex % [
        stop_one,
        stop_two
    ],
    message: string ! ""
}
(procdata) {
    pat: string @ "",
    lck: string @ "",
}
```