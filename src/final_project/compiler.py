def program_split(self, program):
    program = "li $t0 3\naddi $t1 $t0 5"

    program_lines = program.split("\n")
    program_words = []
    for i in range(len(program_lines)):
        program_words.append(program_lines[i].split(" "))
    return program_words

class Compiler:
    def __init__(self):
        self.registers = {
            "$zero": 0, "$at": 0, "$v0": 0, "$v1": 0, 
            "$a0": 0, "$a1":0, "$a2": 0, "$a3": 0, 
            "$t0": 0, "$t1": 0, "$t2": 0, "$t3": 0,
            "$t4": 0, "$t5": 0, "$t6": 0, "$t7": 0,
            "$s0": 0, "$s1": 0, "$s2": 0, "$s3": 0,
            "$s4": 0, "$s5": 0, "$s6": 0, "$s7": 0,
            "$t8": 0, "$t9": 0, "$k0": 0, "$k1": 0,
            "$gp": 0, "$sp": 0, "$fp": 0, "$ra": 0
        }

    def program_split(program):
        """Divides the program from ne big string into a list of individual words"""
        program_lines = program.split("\n")
        program_words = []
        for i in range(len(program_lines)):
            program_words.append(program_lines[i].split(" "))
        return program_words

    def compile(self, program):
        program = "li $t0 3\naddi $t1 $t0 5"
        program = self.program_split(program)
        for i in range(len(program)):
            if program[i][0] == "li":
                func_li(program[i])
            elif program[i][0] == "addi":
                func_addi(program[i])