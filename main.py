from cpu import CPU
from assembler import assemble

cpu = CPU(16, 64, 128, 200)

rom = assemble("main.asm")

cpu.load_rom(rom)
cpu.process()
