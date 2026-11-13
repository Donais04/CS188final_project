from final_project.custom_datatypes import Int_32_Bit


class Compiler:
    def __init__(self):
        self.registers = {
            "$zero": Int_32_Bit(), "$at": Int_32_Bit(), "$v0": Int_32_Bit(), "$v1": Int_32_Bit(), 
            "$a0": Int_32_Bit(), "$a1": Int_32_Bit(), "$a2": Int_32_Bit(), "$a3": Int_32_Bit(),
            "$t0": Int_32_Bit(), "$t1": Int_32_Bit(), "$t2": Int_32_Bit(), "$t3": Int_32_Bit(),
            "$t4": Int_32_Bit(), "$t5": Int_32_Bit(), "$t6": Int_32_Bit(), "$t7": Int_32_Bit(),
            "$s0": Int_32_Bit(), "$s1": Int_32_Bit(), "$s2": Int_32_Bit(), "$s3": Int_32_Bit(),
            "$s4": Int_32_Bit(), "$s5": Int_32_Bit(), "$s6": Int_32_Bit(), "$s7": Int_32_Bit(),
            "$t8": Int_32_Bit(), "$t9": Int_32_Bit(), "$k0": Int_32_Bit(), "$k1": Int_32_Bit(),
            "$gp": Int_32_Bit(), "$sp": Int_32_Bit(), "$fp": Int_32_Bit(), "$ra": Int_32_Bit(),
            "$pc": Int_32_Bit(), "$hi": Int_32_Bit(), "$lo": Int_32_Bit()
        }

    def set_register(self, destination_register: str, value: int):
        self.registers[destination_register].set_value(value)

    def get_registers(self):
        return self.registers

    def print_registers(self) -> None:
        print("### Start ###")
        for i in self.registers:
            print(i, self.get_signed_value(self.registers[i].get_value()))
        print("### End ###")

    def get_signed_value(self, value) -> int:
        """
            converts values into their signed versions. Made by ChatGPT
        """
        if value & 0x80000000:
            return value - 0x100000000
        return value

    def program_split(self, program: str) -> list:
        """Divides the program from a big string into a list of individual words and floats"""
        program_lines = program.split("\r\n")
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
            "add": self.instr_add, "sub": self.instr_sub, "addi": self.instr_addi, "mul": self.instr_mul, "mult": self.instr_mult, "div": self.instr_div,
            "and": self.instr_and, "or": self.instr_or, "andi": self.instr_andi, "ori": self.instr_ori, "sll": self.instr_sll, "srl": self.instr_srl,
            "li": self.instr_li
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
        register_1 = self.registers[args[1]].get_value()
        register_2 = self.registers[args[2]].get_value()
        self.set_register(args[0], register_1 + register_2)

    def instr_sub(self, args: list) -> None:
        """
            subtracts registers
            args[0] = destination register
            args[1] = minuend register
            args[2] = subtrahend register
            (minuend - subtrahend = difference)
        """
        register_1 = self.registers[args[1]].get_value()
        register_2 = self.registers[args[2]].get_value()
        self.set_register(args[0], register_1 - register_2)

    def instr_addi(self, args: list) -> None:
        """
            add immediate
            args[0] = destination register
            args[1] = addend register
            args[2] = addend immediate
        """
        register_1 = self.registers[args[1]].get_value()
        self.set_register(args[0], register_1 + args[2])

    def instr_mul(self, args: list) -> None:
        """
            multiply without overflow
            args[0] = destination register
            args[1] = factor register
            args[2] = factor register 2 electric boogaloo
        """
        register_1 = self.registers[args[1]].get_value()
        register_2 = self.registers[args[2]].get_value()
        self.set_register(args[0], register_1 * register_2)

    def instr_mult(self, args: list) -> None:
        """
            multiply
            args[0] = factor register Sr.
            args[1] = factor register Jr.
            upper 32 bits stored in special register hi, lower 32 bits in lo
        """
        MASK = 0xFFFFFFFF # ChatGPT taught me how bitmasks work

        register_1 = self.registers[args[0]].get_value()
        register_2 = self.registers[args[1]].get_value()

        # Convert to signed 32-bit integers
        if register_1 & 0x80000000:
            register_1 -= 0x100000000

        if register_2 & 0x80000000:
            register_2 -= 0x100000000

        product = register_1 * register_2

        self.set_register("$lo", (product & MASK))
        self.set_register("$hi", ((product >> 32) & MASK))

    def instr_div(self, args: list) -> None:
        """
            divide
            args[0] = dividend register
            args[1] = divisor register
            quotient stored in special register lo, remainder in hi
        """
        MASK = 0xFFFFFFFF # ChatGPT taught me how bitmasks work
        
        register_1 = self.registers[args[0]].get_value()
        register_2 = self.registers[args[1]].get_value()

        # Convert to signed 32-bit integers
        register_1 = self.get_signed_value(register_1)
        register_2 = self.get_signed_value(register_2)

        if register_2 == 0:
            raise ZeroDivisionError("Division by zero error")

        quotient = abs(register_1) // abs(register_2)

        if (register_1 < 0) != (register_2 < 0):
            quotient = -quotient

        remainder = register_1 - (quotient * register_2)

        self.set_register("$lo", (quotient & MASK))
        self.set_register("$hi", (remainder & MASK))

    def instr_and(self, args: list) -> None:
        """
            bitwise and
            args[0] = destination register
            args[1] = operand register
            args[2] = operand register squared
        """
        register_1 = self.registers[args[1]].get_value()
        register_2 = self.registers[args[2]].get_value()

        self.set_register(args[0], register_1 & register_2)

    def instr_or(self, args: list) -> None:
        """
            bitwise or
            args[0] = destination register
            args[1] = operand register
            args[2] = operand register 2 (I'm running out of sequel jokes)
        """
        register_1 = self.registers[args[1]].get_value()
        register_2 = self.registers[args[2]].get_value()

        self.set_register(args[0], register_1 | register_2)

    def instr_andi(self, args: list) -> None:
        """
            bitwise and immediate
            args[0] = destination register
            args[1] = operand register
            args[2] = operand immediate
        """
        register_1 = self.registers[args[1]].get_value()

        self.set_register(args[0], register_1 & args[2])

    def instr_ori(self, args: list) -> None:
        """
            bitwise or immediate
            args[0] = destination register
            args[1] = operand register
            args[2] = operand immediate
        """
        register_1 = self.registers[args[1]].get_value()

        self.set_register(args[0], register_1 | args[2])

    def instr_sll(self, args: list) -> None:
        """
            shift left logical
            args[0] = destination register
            args[1] = operand register
            args[2] = constant number of bits to shift by
        """
        register_1 = self.registers[args[1]].get_value()

        self.set_register(args[0], register_1 << args[2])

    def instr_srl(self, args: list) -> None:
        """
            shift right logical
            args[0] = destination register
            args[1] = operand register
            args[2] = constant number of bits to shift by
        """
        register_1 = self.registers[args[1]].get_value()

        self.set_register(args[0], register_1 >> args[2])

    def instr_li(self, args: list) -> None:
        """
            load immediate
            args[0] = destination register
            args[1] = what value
        """
        self.set_register(args[0], args[1])