import time

from registers import Registers
from alu import ALU

class CPU:
    memory = []
    registers = None
    alu = None

    clock_rate = 0

    def __init__(self, max_memory = 16, _clock_rate = 20):
        self.memory = [0x00 for i in range(max_memory)]
        self.registers = Registers()
        self.alu = ALU()
        self.clock_rate = _clock_rate
    
    def cycle(self):
        
        self.registers.PC = self.registers.PC + 1

    def process(self):
        while self.registers.PC < len(self.memory)-1:
            t = time.process_time()
            self.cycle()
            dt = time.process_time() - t

            print(dt)
            print(self.registers.PC)
            time.sleep(max(0, (1.0/self.clock_rate)- dt))


instructionset = {
    "END" : 0x00,
    "LDA" : 0x01,
    "STA" : 0x02,
    "ADD" : 0x03,
    "SUB" : 0x04
}