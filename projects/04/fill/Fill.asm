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

// Initialize variable screenend as start of screen + number of pixel-blocks -1
@8192
D=A
@SCREEN
D=D+A
D=D-1
@screenend
M=D

// Initial position is at screen end
@pos
M=D


// Main loop
(MAIN)

    // Read Keyboard input
    @KBD
    D=M

    // Blacken one block if something is pressed
    @BLACKEN
    D;JGT

    // Clear one block if nothing is pressed
    @CLEAR
    D;JEQ




// Blacken one pixel-block at position pos and decrement pos
(BLACKEN)

    // Read pos into A and D
    @pos
    AD=M

    // Set pixels at pos to black
    M=-1

    // Check if start of screen is reached, go back to main if it is
    @SCREEN
    D=D-A
    @MAIN
    D;JEQ

    // Decrement pos if start of screen is not reached yet and return to main
    @pos
    M=M-1
    @MAIN
    0;JMP



// Clear one pixel-block at position pos and increment pos
(CLEAR)

    // Read pos into A and D
    @pos
    AD=M

    // Clear pixels at pos
    M=0

    // Check if end of screen is reached, go back to main if it is
    @screenend
    D=D-M
    @MAIN
    D;JEQ

    // Increment pos if end of screen is not reached yet and return to main
    @pos
    M=M+1
    @MAIN
    0;JMP