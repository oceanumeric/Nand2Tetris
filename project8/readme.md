## Project 8: Virtual Machine II 

### How does a-5 works

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

### Big Picture of Function Run-Time

Functions were saved either in different files or different classes. We could 
have different scenarios. Let's take a look at the simplest one. 

Two functions calling in a file called `Main.vm`:

```vm
function Main.main():
    // do something
    call function Main.foo() num_arguments
    // do something
    push constant 10
    add
    call function Main.bar()
    // do something
    neg
    return 

function Main.foo() num_variables 
    // do something
    return 

function Main.bar() num_variables
    // do something
    return 
```

When we translate the above code into the assembly code, the order matters.
It should be like the following one.

```assembly
// Entry point: sys.init 
function Sys.init 0:
    // do something
    call function Main.main() num_arguments 
    // prepare for the call
    // construct the calling block
    // go to function Main.main() num_variables
    // once it finished, it should come back 
    (return_address_label)
    // do something 
    call function Main.foo() num_arguments
    // prepare for the call
    // go to function Main.foo() num_arguments 
    // once it finished it should come back
    (return_address_label2)
    // do something 

    call function Main.bar() num_arguments

    // prepare for the call
    // go to Main.bar()

    (return_address_label)

    END // one has to make sure Sys.init ends properly

function Main.main():
    return

function Main.foo():
    return

function Main.bar():
    return
```

__WARNING__: one has to be very careful about the order of function blocks

THIS is wrong as it will run Main.main() twice. 

```assembly
function Sys.init 0:
    // do something
    call function Main.main():
        // prepare for the call
        // go to Main.main()
        (return_address_label)
    // do something

    function Main.main():
        // do something
        return   // return to (return_address_label)

    End
```

__TIP__: Every function has to end properly before another function blocks starts,
meaning each function is a closed block with independent _branching_ labels except
for those labels that link to another functions. 

Here is the implementation protocols:

Each function has four parts: arguments - function_name - local variables - return.
And we have to save all those essential addresses for the caller and callee. 

### `call f_name num_args`:

```assembly
push return_address_i  // (i = sequential counter)
push LCL  // save LCL for the caller 
push ARG  // save ARG for the caller 
push THIS
push THAT
ARG = SP-5-num_args   // update arguments position 
LCL=SP   // update LCL for the callee 
goto function
(return_address_i)
```

`function f_name num_variables`:

```assembly
repreat num_variables times:
    push 0  // initializing local variables = 0 
```

### Return

```assembly
// frame = LCL, frame a temporary variable frame = address of LCL
@LCL
D=M
@frame
M=D 

// ret_address = *(frame-5)  // put the return address into a temporary variable
@frame
D=M
@5
D=D-A  // frame-5
A=D  // pointer 
D=M
@ret_address
M=D


// reposition the return value for the caller 
// which means pop the value into RAM[ARG]
// *ARG = pop()
@SP
AM=M-1
D=M  // pop the value
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
@frame
A=M-1
D=M 
@THAT
M=D

// restore THIS, ARG, LCL
@2
D=A
@frame
A=M-D
D=M 
@THIS
M=D

@3
D=A
@frame
A=M-D
D=M 
@ARG
M=D

@4
D=A
@frame
A=M-D
D=M 
@LCL
M=D

// go to the caller's return address
@ret_address
A=M   // THIS IS VERY IMPORTANT, red_address = address, using pointer
0;JMP
```

### BootStrap Loader

BootStrap ClassLoader: A Bootstrap Class loader is a Machine code which kickstarts
the operation when the JVM calls it. It is not a java class. 
Its job is to load the first pure Java ClassLoader. Bootstrap ClassLoader 
loads classes from the location rt.jar.

In Hack computer, we also need to load the first pure VM, which is included in
the OS libraries, called `Sys.vm` that includes a method called `init`. The
`Sys.init` starts with some OS initializations and then it called `Main.main`.

Why do we need it? As every calling action will be put into a function called
`main()` which needs to initialize key values of the running-time stack, such
as `SP, LCL, ARG, THIS, THAT`. 

```assembly
// bootstrap initializiation
// Setting the LCL, ARG, THIS and THAT point­ers to known illegal values that help
// to identify when a pointer is used before it is initial­ized.
@256
D=A
@SP
M=D  // SP = 256

// call Sys.init 0 
```

### function Sys.init 0

```assembly 
// construct the function frame
// push initial returned address = SP = 256
@SP
D=M
@SP
AM=M+1
A=A-1
M=D 
//  push LCL 
@LCL
D=M
@SP
AM=M+1
A=A-1
M=D 
// push ARG
@ARG
D=M
@SP
AM=M+1
A=A-1
M=D 
// push this
@THIS
D=M
@SP
AM=M+1
A=A-1
M=D 
// push THAT
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D 
// update ARG
// initialize the RETURN state: *ARG = pop()
// ARG = base address of the ARGUMENT segment = 256
@256
D=A
@ARG
M=D 
// update LCL = SP
@SP
D=M
@LCL
M=D
```

### call function_name 1 

We prepare all essential variables for the calling frame, 
then we will go to the function.

* nArgs tell us how many arguments have been pushed

```assembly
// push the return address
@function_name_Return_Address
D=A
@SP
AM=M+1
A=A-1
M=D

// push LCL 
@LCL
D=M
@SP
AM=M+1
A=A-1
M=D

// push ARG
@ARG
D=M
@SP
AM=M+1
A=A-1
M=D

// push THIS
@THIS
D=M
@SP
AM=M+1
A=A-1
M=D

// push TATH
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D

// repositions ARG
// ARG = SP-5-num_args
@SP
D=M
@5
D=D-A  // SP-5
@n_args  // from the VM code 
D=D-A  // SP-5-num_args
@ARG
M=D

// repositions LCL 
// update LCL = SP
@SP
D=M
@LCL
M=D

// go to function name
@function_name
0;JMP

// generate return label
(function_name_Return_Address)
```
