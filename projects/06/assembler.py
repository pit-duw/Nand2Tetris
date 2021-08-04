import numpy as np
import os
import sys

input_lines = []

dest_dict = {
    "0":"000",
    "M":"001",
    "D":"010",
    "MD":"011",
    "A":"100",
    "AM":"101",
    "AD":"110",
    "AMD":"111",
}

jump_dict = {
    "0":"000",
    "JGT":"001",
    "JEQ":"010",
    "JGE":"011",
    "JLT":"100",
    "JNE":"101",
    "JLE":"110",
    "JMP":"111",
}

comp_dict = {
    "0"  :"0101010",
    "1"  :"0111111",
    "-1" :"0111010",
    "D"  :"0001100",
    "A"  :"0110000",
    "!D" :"0001101",
    "!A" :"0110001",
    "-D" :"0001111",
    "-A" :"0110011",
    "D+1":"0011111",
    "A+1":"0110111",
    "D-1":"0001110",
    "A-1":"0110010",
    "D+A":"0000010",
    "D-A":"0010011",
    "A-D":"0000111",
    "D&A":"0000000",
    "D|A":"0010101",
    "M"  :"1110000",
    "!M" :"1110001",
    "-M" :"1110011",
    "M+1":"1110111",
    "M-1":"1110010",
    "D+M":"1000010",
    "D-M":"1010011",
    "M-D":"1000111",
    "D&M":"1000000",
    "D|M":"1010101",
}

symbol_table = {
    "SP":0,
    "LCL":1,
    "ARG":2,
    "THIS":3,
    "THAT":4,
    "R0":0,
    "R1":1,
    "R2":2,
    "R3":3,
    "R4":4,
    "R5":5,
    "R6":6,
    "R7":7,
    "R8":8,
    "R9":9,
    "R10":10,
    "R11":11,
    "R12":12,
    "R13":13,
    "R14":14,
    "R15":15,
    "SCREEN":16384,
    "KBD":24576,
}

def translate_A(instruction):
    if int(instruction[1:]) >= 0:
        return "0"+'{:015b}'.format(int(instruction[1:]))
    else:
        temp = '{:015b}'.format(abs(int(instruction[1:]))-1)
        return "0"+"".join(["0" if i=="1" else "1" for i in temp])

def translate_C(instruction):
    comp = ""
    dest = ""
    jump = ""
    if len(instruction.split("=")) == 1:
        comp = comp_dict[instruction.split(";")[0]]
        jump = jump_dict[instruction.split(";")[1]]
        dest = "000"
    elif len(instruction.split("=")) == 2:
        dest = dest_dict[instruction.split("=")[0]]
        remainder = instruction.split("=")[1].split(";")
        if len(remainder) == 1:
            comp = comp_dict[remainder[0]]
            jump = "000"
        elif len(remainder) == 2:
            comp = comp_dict[remainder[0]]
            jump = jump_dict[remainder[1]]
        else:
            assert(False)
    else:
        assert(False)
    return "111"+comp+dest+jump

def translate_line(instruction):
    if instruction.startswith("@"):
        return translate_A(instruction)
    else:
        return translate_C(instruction)

        

with open(sys.argv[1], "r") as stream:
    # Read in the file
    input_lines = stream.readlines()
    # Remove blank lines
    input_lines = [l[:-1] for l in input_lines if not l.isspace()]
    # Remove comments and whitespace
    input_lines = [l.split("//")[0].strip() for l in input_lines if l.split("//")[0]]
    
    # Find labels and add them to the table
    n_labels = 0
    addresses = []
    for i, line in enumerate(input_lines):
        if line.startswith("("):
            label = line[1:-1]
            addresses.append(i-n_labels) 
            symbol_table[label] = addresses[-1]
            n_labels += 1

    # Find variables and add them to the table
    n_var = 16
    for i, line in enumerate(input_lines):
        if line.startswith("@"):
            if not (line[1:].isdigit() or line[1:] in symbol_table):
                symbol_table[line[1:]] = n_var
                n_var += 1


    # Remove label definitions from the code 
    input_lines = [l for l in input_lines if not l.startswith("(")]

    # Replace all instances where a label is used with the actual value
    for i,line in enumerate(input_lines):
        if line.startswith("@"):
            if line[1:] in symbol_table:
                input_lines[i] = "@"+str(symbol_table[line[1:]])

with open(sys.argv[1].split(".")[0]+".hack", "w") as outstream:
    hack = [translate_line(line) for line in input_lines]
    outstream.write("\n".join(hack))
