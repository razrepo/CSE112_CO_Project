import MEMORY as rem
from TABLES import opcode_table


def add(command):
    rem.resetFlags()
    reg3_addr = command[13:16]
    reg1_addr = command[7:10]
    reg2_addr = command[10:13]

    reg3 = rem.getData(reg3_addr)
    reg2 = rem.getData(reg2_addr)

    reg1 = sum([reg2, reg3])

    rem.setData(reg1_addr, reg1)


import operator


def sub(command):
    rem.resetFlags()
    reg2_addr = command[10:13]
    reg3_addr = command[13:16]
    reg1_addr = command[7:10]

    reg3 = rem.getData(reg3_addr)
    reg2 = rem.getData(reg2_addr)

    reg1 = operator.sub(reg2, reg3)

    rem.setData(reg1_addr, reg1)


def mov_imm(command):
    rem.resetFlags()
    imm = command[9:16]
    reg1_addr = command[5:8]

    imm = int(imm, 2)
    imm = imm << 0  # Bitwise left shift by 0 positions, effectively no shift

    rem.setData(reg1_addr, imm)


def mov_reg(command):
    reg2_addr = command[13:16]
    reg1_addr = command[10:13]

    reg2 = rem.getData(reg2_addr)

    if reg2_addr == "111":
        val = "".join(["1" if i == 1 else "0" for i in reg2])
        reg2 = int(val, 2)
    rem.setData(reg1_addr, reg2)
    rem.resetFlags()


def ld(command):
    rem.resetFlags()
    address = command[9:16]
    reg1_addr = command[5:8]

    val_mem = rem.getData(address)

    rem.setData(reg1_addr, val_mem)


def st(command):
    rem.resetFlags()
    address = command[9:16]
    reg1_addr = command[5:8]

    reg1 = rem.getData(reg1_addr)

    rem.setData(address, reg1)


def mul(command):
    rem.resetFlags()
    reg2_addr = command[10:13]
    reg3_addr = command[13:16]
    reg1_addr = command[7:10]

    reg3 = rem.getData(reg3_addr)
    reg2 = rem.getData(reg2_addr)

    reg1 = reg2 << reg3
    rem.setData(reg1_addr, reg1)


def div(command):
    rem.resetFlags()
    reg2_addr = command[13:16]
    reg1_addr = command[10:13]

    reg2 = rem.getData(reg2_addr)
    reg1 = rem.getData(reg1_addr)

    remainder = reg1 % reg2
    quotient = int(reg1 / reg2)

    rem.setData("001", remainder)
    rem.setData("000", quotient)


def rs(command):
    rem.resetFlags()
    imm = command[8:16]
    reg1_addr = command[5:8]

    reg1 = rem.getData(reg1_addr)
    imm = int(imm, 2)

    reg1 = reg1 >> imm
    rem.setData(reg1_addr, reg1)


def ls(command):
    rem.resetFlags()
    imm = command[8:16]
    reg1_addr = command[5:8]

    reg1 = rem.getData(reg1_addr)
    imm = int(imm, 2)

    reg1 = reg1 << imm
    rem.setData(reg1_addr, reg1)


def XOR(command):
    rem.resetFlags()
    reg2_addr = command[10:13]
    reg3_addr = command[13:16]
    reg1_addr = command[7:10]

    reg3 = rem.getData(reg3_addr)
    reg2 = rem.getData(reg2_addr)

    reg1 = int(
        "".join(
            [
                "1" if bit1 != bit2 else "0"
                for bit1, bit2 in zip(bin(reg2)[2:].zfill(16), bin(reg3)[2:].zfill(16))
            ]
        ),
        2,
    )

    rem.setData(reg1_addr, reg1)


def OR(command):
    rem.resetFlags()
    reg2_addr = command[10:13]
    reg3_addr = command[13:16]
    reg1_addr = command[7:10]

    reg3 = rem.getData(reg3_addr)
    reg2 = rem.getData(reg2_addr)

    reg1 = int(
        "".join(
            [
                "1" if bit1 == "1" or bit2 == "1" else "0"
                for bit1, bit2 in zip(bin(reg2)[2:].zfill(16), bin(reg3)[2:].zfill(16))
            ]
        ),
        2,
    )

    rem.setData(reg1_addr, reg1)


def AND(command):
    rem.resetFlags()
    reg2_addr = command[10:13]
    reg3_addr = command[13:16]
    reg1_addr = command[7:10]

    reg3 = rem.getData(reg3_addr)
    reg2 = rem.getData(reg2_addr)

    reg1 = int(
        "".join(
            [
                "1" if bit1 == "1" and bit2 == "1" else "0"
                for bit1, bit2 in zip(bin(reg2)[2:].zfill(16), bin(reg3)[2:].zfill(16))
            ]
        ),
        2,
    )

    rem.setData(reg1_addr, reg1)


def NOT(command):
    rem.resetFlags()
    reg2_addr = command[13:16]
    reg1_addr = command[10:13]

    reg2 = rem.getData(reg2_addr)

    reg2 = format(reg2, "016b")

    reg2 = "".join(["0" if bit == "1" else "1" for bit in reg2])

    reg2 = int(reg2, 2)

    rem.setData(reg1_addr, reg2)


def cmp(command):
    rem.resetFlags()
    reg2_addr = command[13:16]
    reg1_addr = command[10:13]

    reg2 = rem.getData(reg2_addr)
    reg1 = rem.getData(reg1_addr)

    flag = "L" if reg1 < reg2 else "G" if reg1 > reg2 else "E"
    rem.setFlag(flag)


def jmp(command):
    rem.resetFlags()
    return int(command[8:16], 2)


def jlt(command):
    FLAGS = rem.getData("111")

    next_command = int(command[8:16], 2) if FLAGS[1] == 1 else rem.PC + 1

    rem.resetFlags()
    return next_command


def jgt(command):
    FLAGS = rem.getData("111")

    next_command = int(command[8:16], 2) if FLAGS[2] == 1 else rem.PC + 1

    rem.resetFlags()
    return next_command


def je(command):
    FLAGS = rem.getData("111")

    next_command = int(command[8:16], 2) if FLAGS[3] == 1 else rem.PC + 1

    rem.resetFlags()
    return next_command


def execute(command):
    opcode = opcode_table[command[0:5]][0]
    halted = False
    PC = rem.PC + 1

    if opcode == "xor":
        XOR(command)
    elif opcode == "sub":
        sub(command)
    elif opcode == "mul":
        mul(command)
    elif opcode == "ld":
        ld(command)
    elif opcode == "jlt":
        PC = jlt(command)
    elif opcode == "div":
        div(command)
    elif opcode == "hlt":
        rem.resetFlags()
        halted = True
    elif opcode == "mov_imm":
        mov_imm(command)
    elif opcode == "or":
        OR(command)
    elif opcode == "add":
        add(command)
    elif opcode == "ls":
        ls(command)
    elif opcode == "mov_reg":
        mov_reg(command)
    elif opcode == "not":
        NOT(command)
    elif opcode == "and":
        AND(command)
    elif opcode == "je":
        PC = je(command)
    elif opcode == "st":
        st(command)
    elif opcode == "jgt":
        PC = jgt(command)
    elif opcode == "rs":
        rs(command)
    elif opcode == "cmp":
        cmp(command)
    elif opcode == "jmp":
        PC = jmp(command)

    return (PC, halted)
