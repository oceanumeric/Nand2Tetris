// Booting
// call Sys.init
@256
D=A
@SP
M=D
@BOOTING_Return
D=A
@SP
AM=M+1
A=A-1
M=D
@LCL
D=M
@SP
AM=M+1
A=A-1
M=D
@ARG
D=M
@SP
AM=M+1
A=A-1
M=D
@THIS
D=M
@SP
AM=M+1
A=A-1
M=D
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D
@SP
D=M
@5
D=D-A
@n_args
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(BOOTING_Return)
// FUNCTION: function Sys.init 0
(Sys.init)
//push constant 4
@4
D=A
@SP
AM=M+1
A=A-1
M=D
// FUNCTION: call Main.fibonacci 1
@Main.fibonacci$ret.0
D=A
@SP
AM=M+1
A=A-1
M=D
@LCL
D=M
@SP
AM=M+1
A=A-1
M=D
@ARG
D=M
@SP
AM=M+1
A=A-1
M=D
@THIS
D=M
@SP
AM=M+1
A=A-1
M=D
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci$ret.0)
//label WHILE
(Sys.init$WHILE)
//goto WHILE
@Sys.init$WHILE
0;JMP
// FUNCTION: function Main.fibonacci 0
(Main.fibonacci)
// push argument 0
@ARG
D=M
@0
A=A+D
D=M
@SP
AM=M+1
A=A-1
M=D
//push constant 2
@2
D=A
@SP
AM=M+1
A=A-1
M=D
// compare whether lt
@SP
AM=M-1
D=M
A=A-1 
M=M-D
@SP
A=M-1
D=M
@LESS0
D;JLT
@SP
A=M-1
M=0
@LTEND0
0;JMP
(LESS0)
@SP
A=M-1
M=-1
(LTEND0)
//if-goto IF_TRUE
@SP
AM=M-1
D=M
@Main.fibonacci$IF_TRUE
D;JNE
//goto IF_FALSE
@Main.fibonacci$IF_FALSE
0;JMP
//label IF_TRUE
(Main.fibonacci$IF_TRUE)
// push argument 0
@ARG
D=M
@0
A=A+D
D=M
@SP
AM=M+1
A=A-1
M=D
@LCL
D=M
@frame
M=D
@frame
D=M
@5
D=D-A
A=D
D=M
@ret_address
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@frame
A=M-1
D=M
@THAT
M=D
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
@ret_address
A=M
0;JMP
//label IF_FALSE
(Main.fibonacci$IF_FALSE)
// push argument 0
@ARG
D=M
@0
A=A+D
D=M
@SP
AM=M+1
A=A-1
M=D
//push constant 2
@2
D=A
@SP
AM=M+1
A=A-1
M=D
// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// FUNCTION: call Main.fibonacci 1
@Main.fibonacci$ret.1
D=A
@SP
AM=M+1
A=A-1
M=D
@LCL
D=M
@SP
AM=M+1
A=A-1
M=D
@ARG
D=M
@SP
AM=M+1
A=A-1
M=D
@THIS
D=M
@SP
AM=M+1
A=A-1
M=D
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci$ret.1)
// push argument 0
@ARG
D=M
@0
A=A+D
D=M
@SP
AM=M+1
A=A-1
M=D
//push constant 1
@1
D=A
@SP
AM=M+1
A=A-1
M=D
// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// FUNCTION: call Main.fibonacci 1
@Main.fibonacci$ret.2
D=A
@SP
AM=M+1
A=A-1
M=D
@LCL
D=M
@SP
AM=M+1
A=A-1
M=D
@ARG
D=M
@SP
AM=M+1
A=A-1
M=D
@THIS
D=M
@SP
AM=M+1
A=A-1
M=D
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci$ret.2)
// add
@SP
AM=M-1
D=M
A=A-1
M=M+D
@LCL
D=M
@frame
M=D
@frame
D=M
@5
D=D-A
A=D
D=M
@ret_address
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@frame
A=M-1
D=M
@THAT
M=D
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
@ret_address
A=M
0;JMP
// FUNCTION: function Sys.init 0
(Sys.init)
//push constant 4
@4
D=A
@SP
AM=M+1
A=A-1
M=D
// FUNCTION: call Main.fibonacci 1
@Main.fibonacci$ret.3
D=A
@SP
AM=M+1
A=A-1
M=D
@LCL
D=M
@SP
AM=M+1
A=A-1
M=D
@ARG
D=M
@SP
AM=M+1
A=A-1
M=D
@THIS
D=M
@SP
AM=M+1
A=A-1
M=D
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci$ret.3)
//label WHILE
(Sys.init$WHILE)
//goto WHILE
@Sys.init$WHILE
0;JMP
// FUNCTION: function Main.fibonacci 0
(Main.fibonacci)
// push argument 0
@ARG
D=M
@0
A=A+D
D=M
@SP
AM=M+1
A=A-1
M=D
//push constant 2
@2
D=A
@SP
AM=M+1
A=A-1
M=D
// compare whether lt
@SP
AM=M-1
D=M
A=A-1 
M=M-D
@SP
A=M-1
D=M
@LESS1
D;JLT
@SP
A=M-1
M=0
@LTEND1
0;JMP
(LESS1)
@SP
A=M-1
M=-1
(LTEND1)
//if-goto IF_TRUE
@SP
AM=M-1
D=M
@Main.fibonacci$IF_TRUE
D;JNE
//goto IF_FALSE
@Main.fibonacci$IF_FALSE
0;JMP
//label IF_TRUE
(Main.fibonacci$IF_TRUE)
// push argument 0
@ARG
D=M
@0
A=A+D
D=M
@SP
AM=M+1
A=A-1
M=D
@LCL
D=M
@frame
M=D
@frame
D=M
@5
D=D-A
A=D
D=M
@ret_address
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@frame
A=M-1
D=M
@THAT
M=D
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
@ret_address
A=M
0;JMP
//label IF_FALSE
(Main.fibonacci$IF_FALSE)
// push argument 0
@ARG
D=M
@0
A=A+D
D=M
@SP
AM=M+1
A=A-1
M=D
//push constant 2
@2
D=A
@SP
AM=M+1
A=A-1
M=D
// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// FUNCTION: call Main.fibonacci 1
@Main.fibonacci$ret.4
D=A
@SP
AM=M+1
A=A-1
M=D
@LCL
D=M
@SP
AM=M+1
A=A-1
M=D
@ARG
D=M
@SP
AM=M+1
A=A-1
M=D
@THIS
D=M
@SP
AM=M+1
A=A-1
M=D
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci$ret.4)
// push argument 0
@ARG
D=M
@0
A=A+D
D=M
@SP
AM=M+1
A=A-1
M=D
//push constant 1
@1
D=A
@SP
AM=M+1
A=A-1
M=D
// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// FUNCTION: call Main.fibonacci 1
@Main.fibonacci$ret.5
D=A
@SP
AM=M+1
A=A-1
M=D
@LCL
D=M
@SP
AM=M+1
A=A-1
M=D
@ARG
D=M
@SP
AM=M+1
A=A-1
M=D
@THIS
D=M
@SP
AM=M+1
A=A-1
M=D
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci$ret.5)
// add
@SP
AM=M-1
D=M
A=A-1
M=M+D
@LCL
D=M
@frame
M=D
@frame
D=M
@5
D=D-A
A=D
D=M
@ret_address
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@frame
A=M-1
D=M
@THAT
M=D
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
@ret_address
A=M
0;JMP
// FUNCTION: function Sys.init 0
(Sys.init)
//push constant 4
@4
D=A
@SP
AM=M+1
A=A-1
M=D
// FUNCTION: call Main.fibonacci 1
@Main.fibonacci$ret.6
D=A
@SP
AM=M+1
A=A-1
M=D
@LCL
D=M
@SP
AM=M+1
A=A-1
M=D
@ARG
D=M
@SP
AM=M+1
A=A-1
M=D
@THIS
D=M
@SP
AM=M+1
A=A-1
M=D
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci$ret.6)
//label WHILE
(Sys.init$WHILE)
//goto WHILE
@Sys.init$WHILE
0;JMP
// FUNCTION: function Main.fibonacci 0
(Main.fibonacci)
// push argument 0
@ARG
D=M
@0
A=A+D
D=M
@SP
AM=M+1
A=A-1
M=D
//push constant 2
@2
D=A
@SP
AM=M+1
A=A-1
M=D
// compare whether lt
@SP
AM=M-1
D=M
A=A-1 
M=M-D
@SP
A=M-1
D=M
@LESS2
D;JLT
@SP
A=M-1
M=0
@LTEND2
0;JMP
(LESS2)
@SP
A=M-1
M=-1
(LTEND2)
//if-goto IF_TRUE
@SP
AM=M-1
D=M
@Main.fibonacci$IF_TRUE
D;JNE
//goto IF_FALSE
@Main.fibonacci$IF_FALSE
0;JMP
//label IF_TRUE
(Main.fibonacci$IF_TRUE)
// push argument 0
@ARG
D=M
@0
A=A+D
D=M
@SP
AM=M+1
A=A-1
M=D
@LCL
D=M
@frame
M=D
@frame
D=M
@5
D=D-A
A=D
D=M
@ret_address
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@frame
A=M-1
D=M
@THAT
M=D
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
@ret_address
A=M
0;JMP
//label IF_FALSE
(Main.fibonacci$IF_FALSE)
// push argument 0
@ARG
D=M
@0
A=A+D
D=M
@SP
AM=M+1
A=A-1
M=D
//push constant 2
@2
D=A
@SP
AM=M+1
A=A-1
M=D
// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// FUNCTION: call Main.fibonacci 1
@Main.fibonacci$ret.7
D=A
@SP
AM=M+1
A=A-1
M=D
@LCL
D=M
@SP
AM=M+1
A=A-1
M=D
@ARG
D=M
@SP
AM=M+1
A=A-1
M=D
@THIS
D=M
@SP
AM=M+1
A=A-1
M=D
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci$ret.7)
// push argument 0
@ARG
D=M
@0
A=A+D
D=M
@SP
AM=M+1
A=A-1
M=D
//push constant 1
@1
D=A
@SP
AM=M+1
A=A-1
M=D
// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// FUNCTION: call Main.fibonacci 1
@Main.fibonacci$ret.8
D=A
@SP
AM=M+1
A=A-1
M=D
@LCL
D=M
@SP
AM=M+1
A=A-1
M=D
@ARG
D=M
@SP
AM=M+1
A=A-1
M=D
@THIS
D=M
@SP
AM=M+1
A=A-1
M=D
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci$ret.8)
// add
@SP
AM=M-1
D=M
A=A-1
M=M+D
@LCL
D=M
@frame
M=D
@frame
D=M
@5
D=D-A
A=D
D=M
@ret_address
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@frame
A=M-1
D=M
@THAT
M=D
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
@ret_address
A=M
0;JMP
