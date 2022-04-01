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

### Stack Base and Memory Segments Mapping

The Hack computer anchors the stack base at address 256, that is 

```cpp
@256
D=A
@SP
M=D
```

The base addresses of _local, argument, this, that_ segments are stored in the registers _LCL, ARG, THIS, and THAT_, respectively. There any access to the i-th entry of a virtual segment (in the context of a VM `push/pop segment_name i` command) should be translated into assembly code that accesses address __(base + i)__ in the RAM, where base is one of the pointers _LCL, ARG, THIS, or THAT_. However, the _constant_ segment is truly virtual as it does not occupy any physical RAM space. 

`push constant 22` 

```cpp
@22
D=A  // D-register holds 22
@SP
AM=M+1  // A-register and RAM[A]=RAM[SP++], now A-register points RAM[SP++]
A=A-1
M=D  // RAM[SP] holds 22 now
```
The alternative way (more lines):
```cpp
@22
D=A  // D-register holds 22
@SP
A=M  // A-register holds the address RAM[SP]
M=D  // RAM[SP] holds 22 now
@SP
M=M+1  // RSM[SP++]
```

`pop local 0`: access address of RAM_Local[base+0] = RAM_Local[LCL+0]

__Failed__: 
```cpp
// move the top value of the stack into RAM_Local[LCL+0]
@SP
AM=M-1  // A-register and RAM[A] = RAM[SP--], now A register points RAM[SP--]
D=M  // D-register holds the value of the stack
@lcl
D=M  // access the base address D-register holds LCL
@0
D=D+A  // D-register holds LCL+0 but NO LONGER holds the value from the stack !!
```
The correct order should be:




