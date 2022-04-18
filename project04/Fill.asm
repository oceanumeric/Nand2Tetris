// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
// 256 rows * 512 pixels / 16 = 8292 
// Infinite loop 

(LOOP)
    @KBD
    D=M
    @FILL
    D;JNE
    @CLEAR
    D;JEQ
    @LOOP
    0;JMP

// fill up the screen manually 
// 256 * 512 pixels = 131072/16 = 8192, set count i = 8192 using JGT 

(FILL)
    @8192
    D=A
    @i
    M=D
    @1
    D=A
    @pixel
    M=D
    @SCREEN
    D=A 
    @address
    M=D
    (BLOOP)
        @address
        A=M
        M=-1
        @address
        D=M
        @pixel
        D=D+M
        @address
        M=D
        @i
        D=M-1
        @i
        M=D
        @BLOOP
        D;JGT
    @LOOP
    0;JMP

(CLEAR)
    @8192
    D=A
    @i
    M=D
    @1
    D=A
    @pixel
    M=D
    @SCREEN
    D=A
    @address
    M=D
    (CLOOP)
        @address
        A=M
        M=0
        @address
        D=M
        @pixel
        D=D+M
        @address
        M=D
        @i
        D=M-1
        @i
        M=D
        @CLOOP
        D;JGT
   
    @LOOP
    0;JMP




