// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// Create variable i and set to value of R0
@0
D=M     
@i
M=D

// Create variable res and set to 0
@res
M=0

// Start of loop -> loop R0 times by decrementing i after each iteration
// In each iteration add R1 to res 
(LOOP)

    // End loop if i = 0
    @i
    D=M
    @END
    D;JEQ

    // Read value from R1 and add to res 
    @1
    D=M
    @res
    M=M+D
    
    // Decrement i
    @i
    M=M-1

    // Unconditional jump back to loop beginning
    @LOOP
    0;JMP

// End of loop
(END)

// Write result to R2
@res
D=M
@2
M=D