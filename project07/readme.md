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
__Failed Again__:
```cpp
// move the top value of the stack into RAM_Local[LCL+0]
@SP
AM=M-1  // A-register and RAM[A] = RAM[SP--], now A register points RAM[SP--]
D=M  // D-register holds the value of the stack
@R13  // a free register
M=D  // R13 holds the value from the stack now 
@lcl
D=M  // access the base address of LCL
@0
D=D+A  // update the address
A=D  // A-register holds the address of LCL+0
// at this stage, one could not move R13 to M
```
The correct order should be:
```cpp
@LCL
D=M  // D-register holds the base address of LCL
@0
D=D+A // D-register holds the address at LCL+0

// Now save the address LCL+0 into R13
@R13
M=D

// now move the value from the stack to LCL+0
@SP
AM=M-1  // [SP--]
D=M  // D-register holds the value of Stack[SP--]
@R13
A=M  // points to RAM[LCL+0]
M=D  // RAM[LCL+0] = Stack[SP--]
```

`push this 6`

```cpp
// move RAM[This+6] into the stack
@THIS
D=M 
@6
A=A+D
D=M  // D-register holds the value of RAM[THIS+6]
@SP
AM=M+1
A=A-1
M=D 
```
`push temp 6`

```cpp
// move RAM[This+6] into the stack
@11  // 6+5
D=M  // D-register holds the value of RAM[THIS+6]
@SP
AM=M+1
A=A-1
M=D 
```

`pop temp 6`

```cpp
@SP
AM=M-1
D=M
@11
M=D
```

`add`:

```cpp
// add RAM[SP--] + RAM[SP-2]
@SP
AM=M-1
D=M  // D-register holds RAM[SP--]
A=A-1 
M=D+M  // RAM[SP--] + RAM[SP-2]
```

`sub`:

```cpp
// add RAM[SP--] + RAM[SP-2]
@SP
AM=M-1
D=M  // D-register holds RAM[SP--]
A=A-1 
M=M-D  // RAM[SP-2] - RAM[SP--]
```

`neg`:

```cpp
@SP
A=M-1  // pointer DOES NOT MOVE
M=-M
```

`eq`:

```cpp
// compute two values first
@SP
AM=M-1
D=M  // D-register holds RAM[SP--] D=M=y , SP = SP-1
A=A-1 
M=M-D  // RAM[SP-2] - RAM[SP--] x= x- y RAM[SP-2] = 
// compare it with 0
@SP
A=M-1  // A points to x  but SP does not change 
D=M  // D = x D=RAM[SP-2] == 0 or not 
@EQUAL  // if == 0 jump to equal
D;JEQ
// if != 0 then do
@SP
A=M-1
M=0
// jump to the end, THIS IS CRUCIAL!
@END
0;JMP
(EQUAL)
@SP
A=M-1  // points to x 
M=1
(END)
```

`gt`:

```cpp
// compute two values first
@SP
AM=M-1
D=M  // D-register holds RAM[SP--] D=M=y 
A=A-1 
M=M-D  // RAM[SP-2] - RAM[SP--] x= x- y 
// compare it with 0
@SP
A=M-1  // A points to x  but SP does not change 
D=M  // D = x 
@GREATER
D;JGT
@SP
A=M-1
M=0
(GREATER)
@SP
A=M-1  // points to x 
M=1
```

`lt`:

```cpp
// compute two values first
@SP
AM=M-1
D=M  // D-register holds RAM[SP--] D=M=y 
A=A-1 
M=M-D  // RAM[SP-2] - RAM[SP--] x= x- y 
// compare it with 0
@SP
A=M-1  // A points to x  but SP does not change 
D=M  // D = x 
@LESS
D;JLT
@SP
A=M-1
M=0
(LESS)
@SP
A=M-1  // points to x 
M=1
```

`and`:

```cpp
// add RAM[SP--] + RAM[SP-2]
@SP
AM=M-1
D=M  // D-register holds RAM[SP--]
A=A-1 
M=D&M  // RAM[SP--] + RAM[SP-2]
```

`or`:

```cpp
// add RAM[SP--] + RAM[SP-2]
@SP
AM=M-1
D=M  // D-register holds RAM[SP--]
A=A-1 
M=D|M  // RAM[SP--] + RAM[SP-2]
```

`not`:

```cpp
@SP
A=M-1
M=!M
```




### Summary

* pop segment i: 
    - move value from stack to segment
    - saving the address of segment first
    - points the value of stack into `RAM[segment+i]`
* push segment i:
    - move value from segment to stack
    - access the value directly 
    - points to `RAM[SP]`
