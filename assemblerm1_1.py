import sys
from collections import OrderedDict


# Constants
OP_code_type_R = {
    "add": "0110011",
    "sub": "0110011",
    "mul": "0110011",
    "slt": "0110011",
    "sltu": "0110011",
    "xor": "0110011",
    "sll": "0110011",
    "srl": "0110011",
    "or": "0110011",
    "and": "0110011",
    "mul": "0110011",
    "rst": "0110011",
    "halt": "0110011",
    "rvrs": "0110011"
}

OP_code_type_I = {
    "lw": "0000011",
    "addi": "0010011",
    "sltiu": "0010011",
    "jalr": "1100111"
}

OP_code_type_S = {
    "sw": "0100011"
}

OP_code_type_B = {
    "beq": "1100011",
    "bne": "1100011",
    "blt": "1100011",
    "bge": "1100011",
    "bltu": "1100011",
    "bgeu": "1100011"
}

OP_code_type_U = {
    "lui": "0110111",
    "auipc": "0010111"
}

OP_code_type_J = {
    "jal": "1101111"
}

#registers
reg_address = {
    "x0": "00000",
    "x1": "00001",
    "x2": "00010",
    "x3": "00011",
    "x4": "00100",
    "x5": "00101",
    "x6": "00110",
    "x7": "00111",
    "x8": "01000",
    "x9": "01001",
    "x10": "01010",
    "x11": "01011",
    "x12": "01100",
    "x13": "01101",
    "x14": "01110",
    "x15": "01111",
    "x16": "10000",
    "x17": "10001",
    "x18": "10010",
    "x19": "10011",
    "x20": "10100",
    "x21": "10101",
    "x22": "10110",
    "x23": "10111",
    "x24": "11000",
    "x25": "11001",
    "x26": "11010",
    "x27": "11011",
    "x28": "11100",
    "x29": "11101",
    "x30": "11110",
    "x31": "11111",
    "zero": "00000",
    "ra": "00001",
    "sp": "00010",
    "gp": "00011",
    "tp": "00100",
    "t0": "00101",
    "t1": "00110",
    "t2": "00111",
    "s0": "01000",
    "s1": "01001",
    "a0": "01010",
    "a1": "01011",
    "a2": "01100",
    "a3": "01101",
    "a4": "01110",
    "a5": "01111",
    "a6": "10000",
    "a7": "10001",
    "s2": "10010",
    "s3": "10011",
    "s4": "10100",
    "s5": "10101",
    "s6": "10110",
    "s7": "10111",
    "s8": "11000",
    "s9": "11001",
    "s10": "11010",
    "s11": "11011",
    "t3": "11100",
    "t4": "11101",
    "t5": "11110",
    "t6": "11111",
    "FLAGS": "111"
}


labels = OrderedDict()  
variables = OrderedDict()  

max_imm = 127
max_float = 0b11_111_100
min_float = 0b1
counter = 0b0_000_000 

instructions = []
machine_code = []  


def is_var(instruction: str) -> bool:
    instruction = instruction.split()
    if len(instruction) != 2:
        return False
    instruction[0].strip()
    if instruction[0] == "var":
        return True
    return False

def is_label(instruction: str) -> bool:
    instruction = instruction.split()
    instruction[0].strip()
    if instruction[0][-1] == ":":
        return True
    return False

def is_type_R(instruction: str) -> bool:
    instruction = instruction.split()
    if len(instruction) != 4:
        return False
    for j, i in enumerate(instruction):
        instruction[j] = i.strip()

    if instruction[0] in OP_code_type_R.keys():
        if instruction[1] in reg_address.keys() and instruction[2] in reg_address.keys() and instruction[3] in reg_address.keys():
            if instruction[1] == "FLAGS" or instruction[2] == "FLAGS" or instruction[3] == "FLAGS":
                print("ERROR: Illegal use of FLAGS register")
                exit()
            return True
        else:
            print("ERROR: Typos in register name")
            exit()
    return False

def is_type_I(instruction: str) -> bool:
    instruction = instruction.split()
    if len(instruction) != 4:
        return False
    for j, i in enumerate(instruction):
        instruction[j] = i.strip()

    if instruction[0] in OP_code_type_I.keys():
        if instruction[1] in reg_address.keys() and instruction[2] in reg_address.keys():
            if instruction[3] == "FLAGS":
                print("ERROR: Illegal use of FLAGS register")
                exit()
            return True
        else:
            print("ERROR: Typos in register name")
            exit()
    return False

def is_type_S(instruction: str) -> bool:
    instruction = instruction.split()
    if len(instruction) != 3:
        return False
    for j, i in enumerate(instruction):
        instruction[j] = i.strip()

    if instruction[0] in OP_code_type_S.keys():
        if instruction[1] in reg_address.keys() and instruction[2] in reg_address.keys():
            if instruction[1] == "FLAGS" or instruction[2] == "FLAGS":
                print("ERROR: Illegal use of FLAGS register")
                exit()
            return True
        else:
            print("ERROR: Typos in register name")
            exit()
    return False



def is_type_B(instruction: str) -> bool:
    instruction = instruction.split()
    if len(instruction) != 4:
        return False
    for j, i in enumerate(instruction):
        instruction[j] = i.strip()

    if instruction[0] in OP_code_type_B.keys():
        if instruction[1] in reg_address.keys() and instruction[2] in reg_address.keys():
            if instruction[3] == "FLAGS":
                print("ERROR: Illegal use of FLAGS register")
                exit()
            return True
        else:
            print("ERROR: Typos in register name")
            exit()
    return False

def is_type_U(instruction: str) -> bool:
    instruction = instruction.split()
    if len(instruction) != 3:
        return False
    for j, i in enumerate(instruction):
        instruction[j] = i.strip()

    if instruction[0] in OP_code_type_U.keys():
        if instruction[1] in reg_address.keys():
            if instruction[2] == "FLAGS":
                print("ERROR: Illegal use of FLAGS register")
                exit()
            return True
        else:
            print("ERROR: Typos in register name")
            exit()
    return False

def is_type_J(instruction: str) -> bool:
    instruction = instruction.split()
    if len(instruction) != 3:
        return False
    for j, i in enumerate(instruction):
        instruction[j] = i.strip()

    if instruction[0] in OP_code_type_J.keys():
        if instruction[1] in reg_address.keys():
            if instruction[2] == "FLAGS":
                print("ERROR: Illegal use of FLAGS register")
                exit()
            return True
        else:
            print("ERROR: Typos in register name")
            exit()
    return False


def handle_variable(instruction: str):  
    instruction = instruction.split()
    for i in instruction:
        i.strip()
    variables[instruction[1]] = None


def address_variables():  
    tmp_counter = counter
    for i in variables:
        tmp = bin(tmp_counter)[2:]
        while len(tmp) < 7:
            tmp = "0" + tmp
        variables[i] = tmp
        tmp_counter += 1



def handle_label(instruction: str) -> None:
    instruction = instruction.split()
    for j, i in enumerate(instruction):
        instruction[j] = i.strip()
    tmp = bin(counter)[2:]
    while len(tmp) < 12:
        tmp = "0" + tmp
    labels[instruction[0][:-1]] = tmp



def make_instructions():
    for i in instructions:
        mcode = ""
        if i["type"] == "R":
            mcode += OP_code_type_R[i["inst"]]
            rd = i["rd"].strip(',')  
            if rd not in reg_address:
                print(f"ERROR: Register '{rd}' not found")
                exit()
            mcode += reg_address[rd]
            if i["inst"] == "add":
                mcode += "000"
            elif i["inst"] == "sub":
                mcode += "000"
            elif i["inst"] == "sll":
                mcode += "001"
            elif i["inst"] == "slt":
                mcode += "010"
            elif i["inst"] == "sltu":
                mcode += "011"
            elif i["inst"] == "xor":
                mcode += "100"
            elif i["inst"] == "srl":
                mcode += "101"
            elif i["inst"] == "or":
                mcode += "110"
            elif i["inst"] == "and":
                mcode += "111"

            rs1 = i["rs1"].strip(',') 
            if rs1 not in reg_address:
                print(f"ERROR: Register '{rs1}' not found")
                exit()
            mcode += reg_address[rs1]

            rs2 = i["rs2"].strip(',')  
            if rs2 not in reg_address:
                print(f"ERROR: Register '{rs2}' not found")
                exit()
            mcode += reg_address[rs2]

            if i["inst"] == "sub":
                mcode += " 0100000"
            else:
                mcode += "0000000"



        if i["type"] == "I":
            mcode += OP_code_type_I[i["inst"]]
            rd = i["rd"].strip(',')  
            if rd not in reg_address:
                print(f"ERROR: Register '{rd}' not found")
                exit()
            mcode += reg_address[rd]
            if i["inst"] == "lw":
                mcode += "010"
            elif i["inst"] == "addi":
                mcode += "000"
            elif i["inst"] == "sltiu":
                mcode += "011"
            elif i["inst"] == "jalr":
                mcode += "000"
            rs1 = i["rs1"].strip(',') 
            if rs1 not in reg_address:
                print(f"ERROR: Register '{rs1}' not found")
                exit()
            mcode += i["imm"]




        elif i["type"] == "S":
            mcode += OP_code_type_S[i["inst"]]
            mcode += i["imm"][:5]
            if i["inst"] == "sw":
                mcode += "010"        

            rs1 = i["rs1"].strip(',') 
            if rs1 not in reg_address:
                print(f"ERROR: Register '{rs1}' not found")
                exit()

            rs2 = i["rs2"].strip(',') 
            if rs2 not in reg_address:
                print(f"ERROR: Register '{rs2}' not found")
                exit()

            mcode += reg_address[rs1]
            mcode += reg_address[rs2]
            mcode += i["imm"][5:]






        elif i["type"] == "B":
            mcode += OP_code_type_B[i["inst"]]

            mcode += i["imm"][0]  
            mcode += i["imm"][1:7]

            if i["inst"] == "beq":
                mcode += "000"
            elif i["inst"] == "bne":
                mcode += "001"
            elif i["inst"] == "blt":
                mcode += "100"
            elif i["inst"] == "bge":
                mcode += "101"
            elif i["inst"] == "bltu":
                mcode += "110"
            elif i["inst"] == "bgeu":
                mcode += "111"      
            mcode += "0"
            
            rd = i["rd"].strip(',')  
            if rd not in reg_address:
                print(f"ERROR: Register '{rd}' not found")
                exit()
            rs1 = i["rs1"].strip(',') 
            if rs1 not in reg_address:
                print(f"ERROR: Register '{rs1}' not found")
                exit()
            mcode += reg_address[rs1]

            mcode += i["imm"][7]
            mcode += i["imm"][-4:] 
            mcode += variables[i["mem_addr"]]





        elif i["type"] == "U":
            mcode += OP_code_type_U[i["inst"]]
            rd = i["rd"].strip(',')  
            if rd not in reg_address:
                print(f"ERROR: Register '{rd}' not found")
                exit()
            mcode += i["imm"]
            mcode += labels[i["mem_addr"]]






        elif i["type"] == "J":
            mcode += OP_code_type_J[i["inst"]]
            rd = i["rd"].strip(',')  
            if rd not in reg_address:
                print(f"ERROR: Register '{rd}' not found")
                exit()
            mcode += i["imm"][0] 
            mcode += i["imm"][1:10]  
            mcode += i["imm"][10]  
            mcode += i["imm"][11:19] 
        machine_code.append(mcode+'\n')




def handle_instruction(instruction):
    inst_parts = instruction.strip().split()  
    operands = inst_parts[1:]

    inst_dict = {}
    opcode = ""

    if inst_parts[0] == "add":
        opcode = "0110011"
        inst_type = "R"
        inst_dict["type"] = inst_type
        inst_dict["inst"] = "add"
        inst_dict["rd"] = operands[0]
        inst_dict["rs1"] = operands[1]
        inst_dict["rs2"] = operands[2]
    elif inst_parts[0] == "sub":
        opcode = "0110011"
        inst_type = "R"
        inst_dict["type"] = inst_type
        inst_dict["inst"] = "sub"
        inst_dict["rd"] = operands[0]
        inst_dict["rs1"] = operands[1]
        inst_dict["rs2"] = operands[2]
    elif inst_parts[0] == "sll":
        opcode = "0110011"
        inst_type = "R"
        inst_dict["type"] = inst_type
        inst_dict["inst"] = "sll"
        inst_dict["rd"] = operands[0]
        inst_dict["rs1"] = operands[1]
        inst_dict["rs2"] = operands[2]
    elif inst_parts[0] == "slt":
        opcode = "0110011"
        inst_type = "R"
        inst_dict["type"] = inst_type
        inst_dict["inst"] = "slt"
        inst_dict["rd"] = operands[0]
        inst_dict["rs1"] = operands[1]
        inst_dict["rs2"] = operands[2]
    elif inst_parts[0] == "sltu":
        opcode = "0110011"
        inst_type = "R"
        inst_dict["type"] = inst_type
        inst_dict["inst"] = "sltu"
        inst_dict["rd"] = operands[0]
        inst_dict["rs1"] = operands[1]
        inst_dict["rs2"] = operands[2]
    elif inst_parts[0] == "xor":
        opcode = "0110011"
        inst_type = "R"
        inst_dict["type"] = inst_type
        inst_dict["inst"] = "xor"
        inst_dict["rd"] = operands[0]
        inst_dict["rs1"] = operands[1]
        inst_dict["rs2"] = operands[2]
    elif inst_parts[0] == "srl":
        opcode = "0110011"
        inst_type = "R"
        inst_dict["type"] = inst_type
        inst_dict["inst"] = "srl"
        inst_dict["rd"] = operands[0]
        inst_dict["rs1"] = operands[1]
        inst_dict["rs2"] = operands[2]
    elif inst_parts[0] == "or":
        opcode = "0110011"
        inst_type = "R"
        inst_dict["type"] = inst_type
        inst_dict["inst"] = "or"
        inst_dict["rd"] = operands[0]
        inst_dict["rs1"] = operands[1]
        inst_dict["rs2"] = operands[2]
    elif inst_parts[0] == "and":
        opcode = "0110011"
        inst_type = "R"
        inst_dict["type"] = inst_type
        inst_dict["inst"] = "and"
        inst_dict["rd"] = operands[0]
        inst_dict["rs1"] = operands[1]
        inst_dict["rs2"] = operands[2]
    elif inst_parts[0] == "lw":
        opcode = "0000011"
        inst_type = "I"
        inst_dict["type"] = inst_type
        inst_dict["inst"] = "lw"
        inst_dict["rd"] = operands[0]
        inst_dict["rs1"] = operands[1]
        inst_dict["imm"] = operands[2]
    elif inst_parts[0] == "addi":
        opcode = "0010011"
        inst_type = "I"
        inst_dict["type"] = inst_type
        inst_dict["inst"] = "addi"
        inst_dict["rd"] = operands[0]
        inst_dict["rs1"] = operands[1]
        inst_dict["imm"] = operands[2]
    elif inst_parts[0] == "sltiu":
        opcode = "0010011"
        inst_type = "I"
        inst_dict["type"] = inst_type
        inst_dict["inst"] = "sltiu"
        inst_dict["rd"] = operands[0]
        inst_dict["rs1"] = operands[1]
        inst_dict["imm"] = operands[2]
    elif inst_parts[0] == "jalr":
        opcode = "1100111"
        inst_type = "I"
        inst_dict["type"] = inst_type
        inst_dict["inst"] = "jalr"
        inst_dict["rd"] = operands[0]
        inst_dict["rs1"] = operands[1]
        inst_dict["imm"] = operands[2]
    elif inst_parts[0] == "sw":
        opcode = "0100011"
        inst_type = "S"
        inst_dict["type"] = inst_type
        inst_dict["inst"] = "sw"
        inst_dict["rs2"] = operands[0]
        inst_dict["rs1"] = operands[1]
        inst_dict["imm"] = operands[2]
    elif inst_parts[0] == "beq":
        opcode = "1100011"
        inst_type = "B"
        inst_dict["type"] = inst_type
        inst_dict["inst"] = "beq"
        inst_dict["rs1"] = operands[0]
        inst_dict["rs2"] = operands[1]
        inst_dict["imm"] = operands[2]
    elif inst_parts[0] == "bne":
        opcode = "1100011"
        inst_type = "B"
        inst_dict["type"] = inst_type
        inst_dict["inst"] = "bne"
        inst_dict["rs1"] = operands[0]
        inst_dict["rs2"] = operands[1]
        inst_dict["imm"] = operands[2]
    elif inst_parts[0] == "bge":
        opcode = "1100011"
        inst_type = "B"
        inst_dict["type"] = inst_type
        inst_dict["inst"] = "bge"
        inst_dict["rs1"] = operands[0]
        inst_dict["rs2"] = operands[1]
        inst_dict["imm"] = operands[2]
    elif inst_parts[0] == "bgeu":
        opcode = "1100011"
        inst_type = "B"
        inst_dict["type"] = inst_type
        inst_dict["inst"] = "bgeu"
        inst_dict["rs1"] = operands[0]
        inst_dict["rs2"] = operands[1]
        inst_dict["imm"] = operands[2]
    elif inst_parts[0] == "blt":
        opcode = "1100011"
        inst_type = "B"
        inst_dict["type"] = inst_type
        inst_dict["inst"] = "blt"
        inst_dict["rs1"] = operands[0]
        inst_dict["rs2"] = operands[1]
        inst_dict["imm"] = operands[2]
    elif inst_parts[0] == "bltu":
        opcode = "1100011"
        inst_type = "B"
        inst_dict["type"] = inst_type
        inst_dict["inst"] = "bltu"
        inst_dict["rs1"] = operands[0]
        inst_dict["rs2"] = operands[1]
        inst_dict["imm"] = operands[2]
    elif inst_parts[0] == "auipc":
        opcode = "0010111"
        inst_type = "U"
        inst_dict["type"] = inst_type
        inst_dict["inst"] = "auipc"
        inst_dict["rd"] = operands[0]
        inst_dict["imm"] = operands[1]
    elif inst_parts[0] == "lui":
        opcode = "0110111"
        inst_type = "U"
        inst_dict["type"] = inst_type
        inst_dict["inst"] = "lui"
        inst_dict["rd"] = operands[0]
        inst_dict["imm"] = operands[1]
    elif inst_parts[0] == "jal":
        opcode = "1101111"
        inst_type = "J"
        inst_dict["type"] = inst_type
        inst_dict["inst"] = "jal"
        inst_dict["rd"] = operands[0]
        inst_dict["imm"] = operands[1]
    else:
        print("ERROR: Typos in instruction name")
        exit()

    instructions.append(inst_dict)



def strip_label(instruction: str) -> str:
    instruction = instruction.split()
    for i in instruction:
        i.strip()
    new_instruction = ""
    for i in instruction[1:]:
        new_instruction += " " + i
    return new_instruction.strip()

def main(input_file_path):
    global counter
    global max_imm
    global max_float
    global min_float
    global variables
    global labels
    global instructions
    global machine_code

    with open(input_file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line == "":
                continue
            if is_label(line):
                handle_label(line)
                continue
            if is_var(line):
                handle_variable(line)
                continue
            if line.startswith("#"):
                continue
            handle_instruction(line)
            counter += 1
    address_variables()
    make_instructions()
    for code in machine_code:
        print(code, end='')

if __name__ == "__main__":
    input_file_path = r"D:\code\DSA\Assignment2\input.txt"
    main(input_file_path)



