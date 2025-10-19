from cpu import CPU
from assembler import assemble

cpu = CPU(128, 20)

rom = [
    0b0000010000000100,  # LDA 0x01
    0b0000110000000101,  # ADD 0x02
    0b0000100000000111,  # STA 0x03
    0b0000000000000000,   # END
    0b0000000000000011,
    0b0000000000000110
]

rom = assemble("main.asm")
print(rom)

cpu.load_rom(rom)
cpu.process()