import time
from registers import Registers
from alu import ALU

class Bus:
    def __init__(self, name="BUS"):
        self.value = 0
        self.name = name

    def write(self, value):
        self.value = value

    def read(self):
        return self.value

class CPU:
    def __init__(self, max_memory=16, _clock_rate=20):
        self.memory = [0x00] * max_memory
        self.registers = Registers()
        self.alu = ALU()
        self.clock_rate = _clock_rate

        # Buses
        self.address_bus = Bus("Address Bus")
        self.data_bus = Bus("Data Bus")
        self.control_bus = Bus("Control Bus")

        # Pipeline registers
        self.IF_ID = {"MDR": 0}
        self.ID_EX = {"instruction": 0, "operand": 0}
        self.EX_MEM = {"instruction": 0, "operand": 0}

        # Stage control
        self.stage = 0  # 0=IF, 1=ID, 2=EX

    def load_rom(self, rom):
        if len(rom) > len(self.memory):
            raise Exception("ROM larger than memory")
        self.memory[:len(rom)] = rom

    # --- Pipeline stages ---
    def fetch(self):
        self.address_bus.write(self.registers.PC)
        self.registers.MAR = self.address_bus.read()
        self.data_bus.write(self.memory[self.registers.MAR])
        self.IF_ID["MDR"] = self.data_bus.read()
        self.registers.PC += 1
        self.stage = 1

    def decode(self):
        MDR = self.IF_ID["MDR"]
        instruction = (MDR >> 8) & 0xFF
        operand = MDR & 0xFF
        self.ID_EX["instruction"] = instruction
        self.ID_EX["operand"] = operand
        self.stage = 2

    def execute(self):
        inst = self.ID_EX["instruction"]
        data = self.ID_EX["operand"]
        name = instructionset.get(inst, "DAT")

        match name:
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
                self.registers.ACC = self.alu.add(self.registers.ACC, self.data_bus.read())
            case "SUB":
                self.address_bus.write(data)
                addr = self.address_bus.read()
                self.data_bus.write(self.memory[addr])
                self.registers.ACC = self.alu.sub(self.registers.ACC, self.data_bus.read())
            case "MUL":
                self.address_bus.write(data)
                addr = self.address_bus.read()
                self.data_bus.write(self.memory[addr])
                self.registers.ACC = self.alu.mul(self.registers.ACC, self.data_bus.read())
            case "DIV":
                self.address_bus.write(data)
                addr = self.address_bus.read()
                self.data_bus.write(self.memory[addr])
                self.registers.ACC = self.alu.div(self.registers.ACC, self.data_bus.read())
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

        # Move executed instruction to EX_MEM (for future MEM/WB stages)
        self.EX_MEM["instruction"] = inst
        self.EX_MEM["operand"] = data

        self.stage = 0  # Next tick: fetch new instruction

    def cycle(self):
        if self.registers.PC >= len(self.memory):
            return False

        # Pipeline: IF -> ID -> EX per tick
        if self.stage == 0:
            self.fetch()
        elif self.stage == 1:
            self.decode()
        elif self.stage == 2:
            self.execute()

        return True

    def process(self):
        while self.registers.PC < len(self.memory):
            t0 = time.process_time()
            self.cycle()
            dt = time.process_time() - t0
            time.sleep(max(0, (1.0 / self.clock_rate) - dt))
        print(self.memory)

# Instruction set
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
    0x0A : "DAT",
    0x0B : "MUL",
    0x0C : "DIV"
}
