## Project 7 : Virtual Machine I - Stack Arithmetic

### Hack's Assembly Language Examples

```cpp
// addition 

@5  // A-register holds 5
D=A  // D-register holds 5
@7  // A-register holds 7
D=D+A  // D = 5 + 7 

// memory access 
@99
D = M  // load RAM[99] to the D-register

// create an array c starting with RAM[100]
@100
D=A  // D-register holds 100
@c  // A-register holds c or set an address for c
M=D  // load 100 into C --> RAM[&c] = RAM[100]
@c
D=M  // get array base address 
@1
A=D+A  // A-register holds 101 
M=7  // set RAM[101] = 7 

// RAM[SP] = D, SP++
@SP
A=M
M=D
@SP
M=M+1
``` 





```
