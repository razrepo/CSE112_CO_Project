import MEMORY as rem
import FUNCTIONS as Fu

rem.initialize()
halted = False
next_instruction = 0

while not halted:
    instruction = rem.getInstruction(rem.PC)

    next_instruction, halted = Fu.execute(instruction)

    rem.printRF()

    rem.PC = next_instruction
    rem.occurances = rem.occurances + 1


rem.dump()
