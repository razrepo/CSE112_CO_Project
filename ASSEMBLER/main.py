import sys
# instruction name: (opcode, type)
opcode_table = {
	"add": ("00000", "A"), 
	"sub": ("00001", "A"), 
	"mov": (("00010", "B"), ("00011", "C")),  
	"ld": ("00100", "D"), 
	"st": ("00101", "D"),
	"mul": ("00110", "A"), 
	"div": ("00111", "C"), 
	"rs": ("01000", "B"), 
	"ls": ("01001", "B"), 
	"xor": ("01010", "A"), 
	"or": ("01011", "A"), 
	"and": ("01100", "A"),
	"not": ("01101", "C"), 
	"cmp": ("01110", "C"), 
	"jmp": ("01111", "E"), 
	"jlt": ("10000", "E"), 
	"jgt": ("10001", "E"), 
	"je": ("10010", "E"), 
	"hlt": ("10011", "F")
	}

# type name: (no. of operands, no. of unused bytes, type of operand1, type of operand2 ....)
type_table = {
	"A": (3, 2, "reg", "reg", "reg"),
	"B": (2, 0, "reg", "imm"),
	"C": (2, 5, "reg", "reg"),
	"D": (2, 0, "reg", "mem_addr_var"),
	"E": (1, 3, "mem_addr_label"),
	"F": (0, 11)
}
registers = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}
# address: 0 based indexing, error generation: 1 based indexing

program = [] # input assembly program
bin_program = [] # output binary code
# location_counter = 0  reset in every pass
instruction_location = 0 # reset in every pass
last_valid_instruction_count = 0
address_table = {} # address of vars and labels. {name: (address, isVariable)}
output=''
output_error=''
errorflag=True


def EXIT():
    f=open('error.txt','w')
    f.write(output)
    f.close()
    exit()



# checks if immediate is a valid immediate
def validImmediate(immediate):
	flag=True
	if len(immediate) == 0:
		flag=False
	elif immediate[0] != "$":
		flag=False
	elif not immediate[1:].isdecimal():
		flag=False
	elif int(immediate[1:]) > 255 or int(immediate[1:]) < 0:
		flag=False
	return flag


		
# checks if it is a valid laber or var address
def validMemoryAddress(memory_address, isVariable):
	flag=False
	if memory_address in address_table:
		if isVariable == address_table[memory_address][1]:
			flag=True
	return flag



def validRegister(name, canBeFlags):
	if name in registers:
		if name == "FLAGS":
			if not canBeFlags: 
				return False
			else:
				return True
		return True
	return False


# converts decimal address val to 8 bit adress string
def memoryLocation(int_address):
	address = bin(int_address)
	address=address[2:]
	leng=len(address)
	if leng < 8:
		i = 8 - leng
		address = i*"0" + address
	return address



def validLabelVar(name):
    global error
    global output
    global output_error
    if name in address_table:
     fr=f"Declaration of {name} already exists. Error on line: {instruction_location}"
     output=fr+'\n'
     errorflag=False
     EXIT()
    elif name in opcode_table or name == "var":
        fr=f"Reserved words can't be used as identifiers for vars or labels. Error on line: {instruction_location}"
        output=fr+'\n'
        errorflag=False
        EXIT()
    for j,i in enumerate(name):
        if not i.isalnum() and not i == "_":
            fr=f"Invalid identifier used on line: {instruction_location}"
            output=fr+'\n'
            errorflag=False
            EXIT()
    return True
