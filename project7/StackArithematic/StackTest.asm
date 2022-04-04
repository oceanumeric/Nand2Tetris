//push constant 17
@17
D=A
@SP
AM=M+1
A=A-1
M=D
//push constant 17
@17
D=A
@SP
AM=M+1
A=A-1
M=D
// compare whether eq
@SP
AM=M-1
D=M  
A=A-1 
M=M-D
@SP
A=M-1  
D=M
@EQUAL0
D;JEQ
@SP
A=M-1
M=0
@EQEND0
0;JMP
(EQUAL0)
@SP
A=M-1
M=-1
(EQEND0)
//push constant 17
@17
D=A
@SP
AM=M+1
A=A-1
M=D
//push constant 16
@16
D=A
@SP
AM=M+1
A=A-1
M=D
// compare whether eq
@SP
AM=M-1
D=M  
A=A-1 
M=M-D
@SP
A=M-1  
D=M
@EQUAL1
D;JEQ
@SP
A=M-1
M=0
@EQEND1
0;JMP
(EQUAL1)
@SP
A=M-1
M=-1
(EQEND1)
//push constant 16
@16
D=A
@SP
AM=M+1
A=A-1
M=D
//push constant 17
@17
D=A
@SP
AM=M+1
A=A-1
M=D
// compare whether eq
@SP
AM=M-1
D=M  
A=A-1 
M=M-D
@SP
A=M-1  
D=M
@EQUAL2
D;JEQ
@SP
A=M-1
M=0
@EQEND2
0;JMP
(EQUAL2)
@SP
A=M-1
M=-1
(EQEND2)
//push constant 892
@892
D=A
@SP
AM=M+1
A=A-1
M=D
//push constant 891
@891
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
//push constant 891
@891
D=A
@SP
AM=M+1
A=A-1
M=D
//push constant 892
@892
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
//push constant 891
@891
D=A
@SP
AM=M+1
A=A-1
M=D
//push constant 891
@891
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
//push constant 32767
@32767
D=A
@SP
AM=M+1
A=A-1
M=D
//push constant 32766
@32766
D=A
@SP
AM=M+1
A=A-1
M=D
// compare whether gt
@SP
AM=M-1
D=M
A=A-1 
M=M-D  
@SP
A=M-1
D=M
@GREATER0
D;JGT
@SP
A=M-1
M=0
@GTEND0
0;JMP
(GREATER0)
@SP
A=M-1
M=-1
(GTEND0)
//push constant 32766
@32766
D=A
@SP
AM=M+1
A=A-1
M=D
//push constant 32767
@32767
D=A
@SP
AM=M+1
A=A-1
M=D
// compare whether gt
@SP
AM=M-1
D=M
A=A-1 
M=M-D  
@SP
A=M-1
D=M
@GREATER1
D;JGT
@SP
A=M-1
M=0
@GTEND1
0;JMP
(GREATER1)
@SP
A=M-1
M=-1
(GTEND1)
//push constant 32766
@32766
D=A
@SP
AM=M+1
A=A-1
M=D
//push constant 32766
@32766
D=A
@SP
AM=M+1
A=A-1
M=D
// compare whether gt
@SP
AM=M-1
D=M
A=A-1 
M=M-D  
@SP
A=M-1
D=M
@GREATER2
D;JGT
@SP
A=M-1
M=0
@GTEND2
0;JMP
(GREATER2)
@SP
A=M-1
M=-1
(GTEND2)
//push constant 57
@57
D=A
@SP
AM=M+1
A=A-1
M=D
//push constant 31
@31
D=A
@SP
AM=M+1
A=A-1
M=D
//push constant 53
@53
D=A
@SP
AM=M+1
A=A-1
M=D
// add
@SP
AM=M-1
D=M
A=A-1
M=M+D
//push constant 112
@112
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
// neg
@SP
A=M-1
D=-M
M=D
// bitwise operation and
@SP
AM=M-1
D=M 
A=A-1 
M=D&M
//push constant 82
@82
D=A
@SP
AM=M+1
A=A-1
M=D
// bitwise operation or
@SP
AM=M-1
D=M
A=A-1 
M=D|M
// bitwise operation not
@SP
A=M-1
D=!M
M=D
(END)
@END
0;JMP
