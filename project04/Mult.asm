// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.
// R0 = 5
// R1 = 7 
// R2 = R0 * R1 = R0 + R0 + R0 + R1 times 
// if R0 == 0 or R1 == 0: R2 = 0 
// else 
// i = R1; sum = 0; for i >= 0 sum = sum + R0 

// initialize i = R1 and sum = 0
    @sum
    M=0
    @R1
    D=M
    @ZERO
    D;JEQ 
    @i
    M=D
    @R0
    D=M
    @ZERO
    D;JEQ
    @R2
    M=0
(LOOP)
    // if i == 0 goto END 
    @sum
    D=M
    @R0
    D=D+M
    @R2
    M=D
    @sum
    M=D
    @i
    D=M
    D=D-1
    @i
    M=D
    @END
    D;JEQ
    @LOOP
    0;JMP
(ZERO)
    @R2
    M=0
    @END
    0;JMP
(END)
    @END
    0;JMP
