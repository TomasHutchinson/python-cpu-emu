def assemble(file):
    binary = []
    memory = [] 
    label_to_address = {} 
    current_address = 0 
    

    with open(file) as f:
        lines = f.readlines()
        

        for line in lines:
            parts = line.strip().split()
            if len(parts) == 0:
                continue 
            
          
            if len(parts) == 3:
                label = parts[0]
                label_to_address[label] = current_address
                current_address += 1
            elif len(parts) == 2 or len(parts) == 1:

                current_address += 1
    

    with open(file) as f:
        lines = f.readlines()
        for line in lines:
            parts = line.strip().split()
            if len(parts) == 0:
                continue 
            
           
            if len(parts) == 3:
                label = parts[0]
                instruction_line = ' '.join(parts[1:])
                inst = assemble_line(instruction_line, memory, label_to_address)
                if inst is not None:
                    binary.append(inst)
            elif len(parts) == 2 or len(parts) == 1:

                inst = assemble_line(line.strip(), memory, label_to_address)
                if inst is not None:
                    binary.append(inst)
    

    binary.extend(memory)
    
    return binary

def assemble_line(line, memory, label_to_address):
    parts = line.strip().split()
    if len(parts) == 0:
        return None
    
    mnemonic = parts[0]

    if mnemonic not in mnemonic_to_opcode and mnemonic != "DAT":
        raise ValueError(f"Invalid mnemonic: {mnemonic}")
    

    if mnemonic == "DAT":
        if len(parts) > 1:
            value = int(parts[1], 10)
            memory.append(value) 
        else:
            raise ValueError(f"Invalid DAT format: {line}")
        return None

    opcode = mnemonic_to_opcode[mnemonic]
    address = 0
    
    if len(parts) > 1:
        address_part = parts[1]

        if address_part in label_to_address:
            address = label_to_address[address_part]
        else:
            try:
                address = int(address_part, 10)
            except ValueError:
                raise ValueError(f"Invalid address or label: {address_part}")
    
    instruction = (opcode << 8) | (address & 0xFF)
    
    return instruction

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

mnemonic_to_opcode = {v: k for k, v in instructionset.items()}
