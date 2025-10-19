import time

from registers import Registers
from alu import ALU

class CPU:
    memory = []
    registers = None
    alu = None

    clock_rate = 0

    def __init__(self, max_memory=16, _clock_rate=20):
        self.memory = [0x00 for _ in range(max_memory)]
        self.registers = Registers()
        self.alu = ALU()
        self.clock_rate = _clock_rate
    
    def load_rom(self, rom):
        if len(self.memory) < len(rom):
            raise Exception("ROM larger than cpu memory")
        elif len(self.memory) > len(rom):
            rom = rom + [0x00 for _ in range(len(self.memory) - len(rom))]
        self.memory = rom
    
    def cycle(self):
        self.registers.MAR = self.registers.PC
        self.registers.PC += 1
        self.registers.MDR = self.memory[self.registers.MAR]

        self.cu()
    
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