from cpu import CPU
from assembler import assemble

cpu = CPU(16, 64, 128, 200)

rom = assemble("main.asm")
print(rom)

cpu.load_rom(rom)
cpu.process()