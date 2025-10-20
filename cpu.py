import time

from registers import Registers
from alu import ALU

class CPU:
    memory = []
    registers = None
    alu = None

    clock_rate = 0
    stage = 0

    current_instruction = None
    current_data = None

    def __init__(self, max_memory=16, _clock_rate=20):
        self.memory = [0x00 for _ in range(max_memory)]
        self.registers = Registers()
        self.alu = ALU()
        self.clock_rate = _clock_rate

        self.address_bus = Bus("Address Bus")
        self.data_bus = Bus("Data Bus")
        self.control_bus = Bus("Control Bus")

    
    def load_rom(self, rom):
        if len(self.memory) < len(rom):
            raise Exception("ROM larger than cpu memory")
        elif len(self.memory) > len(rom):
            rom = rom + [0x00 for _ in range(len(self.memory) - len(rom))]
        self.memory = rom
    
    def fetch(self):
        self.address_bus.write(self.registers.PC)
        self.registers.MAR = self.address_bus.read()

        self.data_bus.write(self.memory[self.registers.MAR])

        # Move data from bus to MDR
        self.registers.MDR = self.data_bus.read()

        # Increment PC
        self.registers.PC += 1

        # Next stage: decode
        self.stage = 1

    def decode(self):
        instruction = self.registers.MDR >> 8
        data = self.registers.MDR & 0xFF
        self.current_instruction = instruction
        self.current_data = data
        # Ready for execute next tick
        self.stage = 2

    def execute(self):
        inst_name = instructionset[self.current_instruction]
        data = self.current_data

        match inst_name:
            case "END":
                self.registers.PC = len(self.memory)
            case "LDA":
                self.address_bus.write(data)
                addr = self.address_bus.read()
                self.data_bus.write(self.memory[addr])
                self.registers.ACC = self.data_bus.read()
            case "STA":
                self.address_bus.write(data)
                addr = self.address_bus.read()
                self.data_bus.write(self.registers.ACC)
                self.memory[addr] = self.data_bus.read()
            case "ADD":
                self.address_bus.write(data)
                addr = self.address_bus.read()
                self.data_bus.write(self.memory[addr])
                operand = self.data_bus.read()
                self.registers.ACC = self.alu.add(self.registers.ACC, operand)
            case "SUB":
                self.address_bus.write(data)
                addr = self.address_bus.read()
                self.data_bus.write(self.memory[addr])
                operand = self.data_bus.read()
                self.registers.ACC = self.alu.sub(self.registers.ACC, operand)
            case "INP":
                val = int(input("Input: "))
                self.data_bus.write(val)
                self.registers.ACC = self.data_bus.read()
            case "OUT":
                self.data_bus.write(self.registers.ACC)
                print(f"Output: {self.data_bus.read()}")
            case "BRP":
                if self.registers.ACC >= 0:
                    self.registers.PC = data
            case "BRZ":
                if self.registers.ACC == 0:
                    self.registers.PC = data
            case "BRA":
                self.registers.PC = data
            case "DAT":
                pass

        # Reset control signals (future use)
        self.control_bus.write(0)
        self.stage = 0  # Return to fetch stage


    def cycle(self):
        if self.registers.PC >= len(self.memory):
            return False  # Program ended
        
        if self.stage == 0:
            self.fetch()
        elif self.stage == 1:
            self.decode()
        elif self.stage == 2:
            self.execute()
        
        return True
    
    def cu(self):
        instruction = self.registers.MDR >> 8  
        data = self.registers.MDR & 0xFF      
        
        print(f'Instruction: {instruction:08b}')
        print(f'Data: {data:08b}')
        
        inst = instructionset[instruction]

        match inst:
            case "END":
                self.registers.PC = len(self.memory)
            case "LDA":
                self.registers.ACC = self.memory[data]
            case "STA":
                self.memory[data] = self.registers.ACC
            case "ADD":
                self.registers.ACC = self.alu.add(self.registers.ACC, self.memory[data])
            case "SUB":
                self.registers.ACC = self.alu.sub(self.registers.ACC, self.memory[data])
            case "INP":
                self.registers.ACC = int(input("Input: "))
            case "OUT":
                print(f"Output: {self.registers.ACC}")
            case "BRP":
                if self.registers.ACC >= 0:
                    self.registers.PC = data
            case "BRZ":
                if self.registers.ACC == 0:
                    self.registers.PC = data
            case "BRA":
                self.registers.PC = data
            case "DAT":
                pass  #No operation in runtime

    def process(self):
        while self.registers.PC < len(self.memory):
            t = time.process_time()
            self.cycle()
            dt = time.process_time() - t
            time.sleep(max(0, (1.0 / self.clock_rate) - dt))
        print(self.memory)

class Bus:
    def __init__(self, name="BUS"):
        self.value = 0
        self.name = name

    def write(self, value):
        self.value = value

    def read(self):
        return self.value



instructionset = {
    0x00 : "END",
    0x01 : "LDA",
    0x02 : "STA",
    0x03 : "ADD",
    0x04 : "SUB",
    0x05 : "INP",
    0x06 : "OUT",
    0x07 : "BRP",
    0x08 : "BRZ",
    0x09 : "BRA",
    0x0A : "DAT"
}