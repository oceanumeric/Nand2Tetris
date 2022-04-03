## Project 8: Virtual Machine II 


__WARNING__: there is no `M-5` computation instruction, only `M-1` works
```assembly
@5
D=A   // D=5
@R13
M=M-D  // RAM[R13] = RAM[R13]-5
```

### if-goto label 

```assembly
// pop the top value of the stack
@SP
AM=M-1
D=M
// D != 0
@LABEL
D;JNE
```

### function function_name nVars 

```assembly
(function_name)  // label the entry point 
push constant 0  // for nVars time:
@0
D=A
@SP
AM=M+1
A=A-1
M=D

// LCL points to the address of the first local variable = 0
// after nVars time 
// now sp moves to LCL+nVars+1
```


### Return

```assembly
// get the address of the frame end 
@LCL
D=M  // get the address and save it to the D-register
@R13
M=D  // save the address of the frame end into R13
@5
D=A
@R13
A=M-D // A-register points to the address of the return address 
D=M  // D-register holds the return address now
@R14
M=D  // R14 saves the return address 

// reposition the return value for the caller 
// which means pop the value into RAM[ARG]
// *ARG = pop
@SP
AM=M-1
D=M
// then we save it to ARG
@ARG
A=M  // A-register points to RAM[ARG]
M=D 

// Now reposition SP of the caller
// SP = ARG + 1
@ARG
D=M+1
@SP
M=D

// restore that of the caller
// THAT = *(endframe-1)
@R13
A=M-1
D=M 
@THAT
M=D

// restore THIS, ARG, LCL
@2
D=A
@R13
A=M-D
D=M 
@THIS
M=D

@3
D=A
@R13
A=M-D
D=M 
@ARG
M=D

@4
D=A
@R13
A=M-D
D=M 
@LCL
M=D

// go to the caller's return address
```
