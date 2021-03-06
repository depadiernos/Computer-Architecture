"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        self.running = True

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print("Usage: ls8.py filename.ls8")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as file:
                for line in file:
                    split_line = line.split("#")
                    value = split_line[0].strip() 

                    if value == "":
                        continue 
                    instruction = int(value, 2)
                    self.ram[address] = instruction
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[1]}: File not found")
            sys.exit(2)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def LDI(self):
        address = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        self.reg[address] = value
        self.pc += 3


    def PRN(self):
        register = self.ram_read(self.pc + 1)
        value = self.reg[register]
        print(value)
        self.pc += 2

    def PUSH(self):
        register = self.ram_read(self.pc + 1)
        value = self.reg[register]
        address = self.reg[self.sp]
        self.ram_write(address, value)
        self.reg[self.sp] -= 1
        self.pc += 2

    def POP(self):
        value = self.ram_read(self.reg[self.sp])
        register = self.ram_read(self.pc + 1)
        self.reg[register] = value
        self.reg[self.sp] += 1
        self.pc += 2

    def CALL(self):
        return_address = self.pc + 2
        self.reg[6] -= 1
        self.ram[self.reg[6]] = return_address
        self.pc = self.reg[self.ram_read(self.pc + 1)]

    def RET(self):
        self.pc = self.reg[self.sp]
        self.reg[self.sp] += 1

    def ADD(self):
        op_a = self.ram_read(self.pc + 1)
        op_b = self.ram_read(self.pc + 2)
        self.alu("ADD", op_a, op_b)
        self.pc += 3

    def MUL(self):
        op_a = self.ram_read(self.pc + 1)
        op_b = self.ram_read(self.pc + 2)
        self.alu("MUL", op_a, op_b)
        self.pc += 3

    def HLT(self):
        self.running = False
        self.pc += 1

    def run(self):
        """Run the CPU."""

        while self.running:
            instruction = self.ram[self.pc]
            if instruction == 0b10000010: # LDI
                self.LDI()
            elif instruction == 0b01000111: #PRN
                self.PRN()
            elif instruction == 0b00000001: #HLT
                self.HLT()
            elif instruction == 0b01000101: #PUSH
                self.PUSH()
            elif instruction == 0b01000110: #POP
                self.POP()
            elif instruction == 0b10100010: #MUL
                self.MUL()
            elif instruction == 0b10100000:
                self.ADD()
            elif instruction == 0b01010000:
                self.CALL()
            elif instruction == 0b00010001:
                self.RET()
            else:
                print(f"Bad input: {instruction}")
                sys.exit(1)

