import sys

register = [0, 0, 0, 0, 0, 0, 0, [0, 0, 0, 0]]
occurances = 0
no_of_instructions = 0
variables = []
program = []
PC = 0
memoryoccurance = []
occurances = 0
memory = []


def initialize():
    global program
    global no_of_instructions
    global PC
    global occurances
    global variables

    while 1:
        try:
            line = input()
            if line == "e":
                break
            program.append(line)
        except EOFError:
            break

    no_of_instructions = len(program)

    for i in range(128 - no_of_instructions):
        variables.append(0)


def to16Bit(value):
    value = f"{value:016b}"
    return value


def to8Bit(value):
    value = bin(value)[2:]
    no_of_zeroes = 7 - len(value)

    if no_of_zeroes > 0:
        value = "0" * no_of_zeroes + value

    return value


def resetFlags():
    global register
    register[7] = [0 for _ in range(4)]


def setFlag(flag_type):
    global register

    flag_mapping = {"V": 0, "L": 1, "G": 2, "E": 3}

    if flag_type in flag_mapping:
        register[7][flag_mapping[flag_type]] = 1
    else:
        print("Invalid flag type")
        exit()


def getData(mem_addr):
    global memoryoccurance
    global memory

    return (
        register[int(mem_addr, 2)]
        if len(mem_addr) == 3
        else variables[int(mem_addr, 2) - no_of_instructions]
    )


def getInstruction(mem_addr):
    global memoryoccurance
    global memory

    memory.append(mem_addr)
    memoryoccurance.append(occurances)

    return program[mem_addr]


def setData(mem_addr, value):
    global memory
    global memoryoccurance
    global register
    global variables

    if value < 0:
        value = 0
        setFlag("V")

    value = bin(value & 0xFFFF)[2:]
    if len(value) > 16:
        value = value[-16:]
        setFlag("V")

    value = int(value, 2)

    if len(mem_addr) == 3:
        register[int(mem_addr, 2) + 1] = value
    elif len(mem_addr) == 7:
        variables[int(mem_addr, 2) - no_of_instructions] = value
        memory.append(int(mem_addr, 2))
        memoryoccurance.append(occurances)


def printRF():
    print(to8Bit(PC), end="        ")

    register_bits = [to16Bit(register[i]) for i in range(7)]
    FLAGS = "".join("1" if i == 1 else "0" for i in register[7])
    FLAGS = "0" * 12 + FLAGS

    print(*register_bits, FLAGS)


def dump():
    for i in program:
        print(i, end="")
        if i != "1101000000000000":
            print()

    if program[len(program) - 1][-1] != "\n":
        print()

    for i in variables:
        print(to16Bit(i))
