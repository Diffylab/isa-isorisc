def toSigned(num, n):
    lval = 2**(n-1)
    if num > lval:
        return -(2**n - num)
    else:
        return num  
memory = []
pc = 0
nextPC = 0
writeBack = 0
while pc >= 0:
    # fetch PC stage
    instr = memory[pc]
    # decode stage
    opcode = (instr>>30 & 0x3) # 0 to 3, actually only 2 instructions are implemented
    instr_A = toSigned(instr>>20 & 0x3ff, 10) # Convert 10bit unsigned address to 10bit signed address
    instr_B = toSigned(instr>>10 & 0x3ff, 10) # Convert 10bit unsigned address to 10bit signed address
    # Special jump instruction
    instr_CR = instr & 0x3ff # Extract full jump/result instruction
    instr_CR_type = instr_CR>>10 # Extract type of jump/result
    instr_CR_val = toSigned(instr_CR & 0x1ff, 9) # Convert 9bit unsigned address to 9bit signed address
    # fetch operands
    instr_A2 = memory[pc+instr_A]
    instr_B2 = memory[pc+instr_B]
    # Execute
    r = instr_A2 - instr_B2
    if opcode == 0:
        writeBack = pc+instr_B
        if r <= 0:
            if instr_CR_type == 1:
                nextPC = memory[pc+instr_CR_val]
            else:
                nextPC = pc+instr_CR_val
        else:
            nextPC += 1
    elif opcode == 1:
        if instr_CR_type == 1:
            writeBack = memory[pc+instr_CR_val]
        else:
            writeBack = pc+instr_CR_val
        nextPC += 1
    memory[writeBack] = r