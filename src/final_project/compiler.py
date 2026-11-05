class Compiler:
    def __init__(self):
        self.registers = {
            "$zero": 0, "$at": 0, "$v0": 0, "$v1": 0, 
            "$a0": 0, "$a1": 0, "$a2": 0, "$a3": 0,
            "$t0": 0, "$t1": 0, "$t2": 0, "$t3": 0,
            "$t4": 0, "$t5": 0, "$t6": 0, "$t7": 0,
            "$s0": 0, "$s1": 0, "$s2": 0, "$s3": 0,
            "$s4": 0, "$s5": 0, "$s6": 0, "$s7": 0,
            "$t8": 0, "$t9": 0, "$k0": 0, "$k1": 0,
            "$gp": 0, "$sp": 0, "$fp": 0, "$ra": 0
        }

    def update_register(self, destination_register: str, value: int):
        self.registers[destination_register] = value

    def get_registers(self):
        return self.registers

    def program_split(self, program: str) -> list:
        """Divides the program from a big string into a list of individual words and floats"""
        program_lines = program.split("\n")
        program_words = []
        for i in range(len(program_lines)):
            program_words.append(program_lines[i].split(" "))
            for j in range(len(program_words[i])):
                try:
                    program_words[i][j] = int(program_words[i][j])
                except ValueError:
                    pass
        return program_words

    def compile(self, program: str):
        program_list = self.program_split(program)

        # https://www.dsi.unive.it/~gasparetto/materials/MIPS_Instruction_Set.pdf
        instruction_dictionary = {
            "add": self.instr_add, "sub": self.instr_sub, "addi": self.instr_addi, "mul": self.instr_mul, "li": self.instr_li
        }

        for i in range(len(program_list)):
            args = program_list[i].copy()
            args.pop(0)
            instruction_dictionary[program_list[i][0]](args)

    def instr_add(self, args: list) -> None:
        """
            adds registers
            args[0] = destination register
            args[1] = addend register
            args[2] = addend register 2 judgement day
        """
        self.update_register(args[0], self.registers[args[1]] + self.registers[args[2]])

    def instr_sub(self, args: list) -> None:
        """
            subtracts registers
            args[0] = destination register
            args[1] = minuend register
            args[2] = subtrahend register
            (minuend - subtrahend = difference)
        """
        self.update_register(args[0], self.registers[args[1]] - self.registers[args[2]])

    def instr_addi(self, args: list) -> None:
        """
            add immediate
            args[0] = destination register
            args[1] = addend register
            args[2] = addend immediate
        """
        self.update_register(args[0], self.registers[args[1]] + args[2])

    def instr_mul(self, args: list) -> None:
        """
            multiply without overflow
            args[0] = destination register
            args[1] = factor register
            args[2] = factor register 2 electric boogaloo
        """
        self.update_register(args[0], self.registers[args[1]] * self.registers[args[2]])

    def instr_li(self, args: list) -> None:
        """
            load immediate
            args[0] = destination register
            args[1] = what value
        """
        self.update_register(args[0], args[1])