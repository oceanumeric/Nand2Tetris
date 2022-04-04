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
//push constant 6
@6
D=A
@SP
AM=M+1
A=A-1
M=D
//push constant 8
@8
D=A
@SP
AM=M+1
A=A-1
M=D
// CALL: call Class1.set 2
@Class1.set$ret.0
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
@2
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class1.set
0;JMP
(Class1.set$ret.0)
// pop temp 0
@SP
AM=M-1
D=M
@5
M=D
//push constant 23
@23
D=A
@SP
AM=M+1
A=A-1
M=D
//push constant 15
@15
D=A
@SP
AM=M+1
A=A-1
M=D
// CALL: call Class2.set 2
@Class2.set$ret.1
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
@2
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class2.set
0;JMP
(Class2.set$ret.1)
// pop temp 0
@SP
AM=M-1
D=M
@5
M=D
// CALL: call Class1.get 0
@Class1.get$ret.2
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
@0
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class1.get
0;JMP
(Class1.get$ret.2)
// CALL: call Class2.get 0
@Class2.get$ret.3
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
@0
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class2.get
0;JMP
(Class2.get$ret.3)
//label WHILE
(Sys.init$WHILE)
//goto WHILE
@Sys.init$WHILE
0;JMP
// FUNCTION: function Class1.set 0
(Class1.set)
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
// pop static 0
@SP
AM=M-1
D=M
@Class10
M=D
// push argument 1
@ARG
D=M
@1
A=A+D
D=M
@SP
AM=M+1
A=A-1
M=D
// pop static 1
@SP
AM=M-1
D=M
@Class11
M=D
//push constant 0
@0
D=A
@SP
AM=M+1
A=A-1
M=D
// RETURN: return
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
// FUNCTION: function Class1.get 0
(Class1.get)
// push static 0
@Class10
D=M
@SP
AM=M+1
A=A-1
M=D
// push static 1
@Class11
D=M
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
// RETURN: return
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
// FUNCTION: function Class2.set 0
(Class2.set)
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
// pop static 0
@SP
AM=M-1
D=M
@Class20
M=D
// push argument 1
@ARG
D=M
@1
A=A+D
D=M
@SP
AM=M+1
A=A-1
M=D
// pop static 1
@SP
AM=M-1
D=M
@Class21
M=D
//push constant 0
@0
D=A
@SP
AM=M+1
A=A-1
M=D
// RETURN: return
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
// FUNCTION: function Class2.get 0
(Class2.get)
// push static 0
@Class20
D=M
@SP
AM=M+1
A=A-1
M=D
// push static 1
@Class21
D=M
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
// RETURN: return
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
