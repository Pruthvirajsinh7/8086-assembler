import sys

#Open Output File
stdoutOrigin = sys.stdout
sys.stdout = open("OutputTest.txt" , "w")

address = {'AL' : 1, 'AH' : 2, 'BL' : 3, 'BH' : 4, 'CL' : 5, 'CH' : 6, 'DL' : 7, 'DH' : 8 }
oprations = {'MOV': 1,'ADD': '2','SUB': 3,'INC': 4,'DEC': 5,'AND': 6,'OR': 7,'XOR': 8,'NOT': 9,'NEG': 10,'PUSH': 11,'POP': 12,'XCHG': 13,'NOP':14,'HLT':15}
regValues= {'AL' : 0, 'AH' : 0, 'BL' : 0, 'BH' : 0, 'CL' : 0, 'CH' : 0, 'DL' : 0, 'DH' : 0 }

#Flag Registers

flagReg = [0,0,1,0,0,0,0,0,0]

#Memory

memory = [0]*16

#Parity Calculating Function 

def parity(s):
    count = 0
    output = 1
    for i in s:
        if(i=="1"):
            count = count +1
    if (count%2):
        output = 0
    return output

#Stack Segment 

stackSegment = []

def decode(data):
    
    opcode = 0
    rd = 0
    rs = 0
    rs2 = 0
    imm = 0
    dm =0
    type = 0
    
    
    data = data.strip()
    inst = data.split()
    
    args = []
    
    out = ''
    flag = 0
    
    for i in range(len(inst)):
        if (inst[i] != ""):
            if (inst[i] != "\n"):
                args.append(inst[i])
    
    
    # For Length 1
    
    if(len(args) == 1):
        opcode = oprations[args[0]]
        type = 0
        
        if(args[0] == 'HLT'):
            flag = 1
            out = "Program Terminated!\n"
    
    
    #For Length 2 
        
    elif (len(args) == 2):
        opcode = oprations[args[0]]
        if (args[0] != "PUSH"):
            rd = address [args[1]]
            ini = regValues[args[1]]
            
        type = 0
        
        #INC
        
        if(args[0] == 'INC'):
            out = args [1]
            regValues[args[1]] = regValues[args[1]] + 1
            value = regValues[args[1]]
            out = out + " = " + format(regValues[args[1]] , '02x') + "H"
            
            #Updating Flag Registers
            
            flagReg[7] = parity(format(regValues[args[1]] , '08b'))
            flagReg[0] = int((format(regValues[args[1]] , '08b')[0]!=format(ini , '08b')[0]))
            flagReg[4] = int(regValues[args[1]] < 0)
            flagReg[5] = int(regValues[args[1]] == 0)
        
        #DEC
        
        if(args[0] == "DEC"):
            out = args [1]
            regValues[args[1]] = regValues[args[1]] - 1
            value = regValues[args[1]]
            out = out + " = " + format(regValues[args[1]] , '02x')[-2] + format(regValues[args[1]] , '02x')[-1] + "H"
            
            #Updating Flag Registers
            
            flagReg[7] = parity(format(regValues[args[1]] , '08b'))
            flagReg[0] = int((format(regValues[args[1]] , '08b')[0]!=format(ini , '08b')[0]))
            flagReg[4] = int(format(regValues[args[1]] , '08b')[0] == '1')
            flagReg[5] = int(regValues[args[1]] == 0)
            
        #NOT
        
        if(args[0] == "NOT"):
            
            out = args[1] + " = "
            temp = format(regValues[args[1]] , '08b')
            temp = temp[::-1]
            
            regValues[args[1]] = 0
            
            for i in range(len(temp)):
                if(temp[i] == "0"):
                    regValues[args[1]] = regValues[args[1]] + 2**i
            out += format(regValues[args[1]] , "02x") + "H"
            
            #Updating Flag Registers
            
            flagReg[8] = 0
            flagReg[7] = parity(format(regValues[args[1]], '08b'))
            flagReg[0] = 0
            flagReg[4] = int(format(regValues[args[1]] , '08b')[0] == '1')
            flagReg[5] = int(regValues[args[1]] == 0)
            
        
        #NEG 
        
        if(args[0] == "NEG"):
            
            out = args[1] + " = "
            temp = format(regValues[args[1]] , '08b')
            temp = temp[::-1]
            
            regValues[args[1]] = 0
            ini = regValues[args[1]]
            
            for i in range(len(temp)):
                if(temp[i] == "0"):
                    regValues[args[1]] = regValues[args[1]] + 2**i
            
            regValues[args[1]] +=1
            out += format(regValues[args[1]] , '02x')[-2] + format(regValues[args[1]] , '02x')[-1] + "H"
            
            #Updating Flag Registers
            
            flagReg[7] = parity(format(regValues[args[1]], '08b'))
            flagReg[0] = int((format(regValues[args[1]], '08b')[0] != format(ini , '08b')[0]))
            flagReg[4] = int(format(regValues[args[1]] , '08b')[0] == '1')
            flagReg[5] = int(regValues[args[1]] == 0)
            
            
        #PUSH
        
        if(args[0]=="PUSH"): 
            a = int(args[1][:-1],16)
            stackSegment.append(a)

        #POP
        
        if(args[0]=="POP"): 
            b = stackSegment.pop()
            regValues[args[1]] = b
            out = args[1] + " = " + format(regValues[args[1]],"02x") +"H"
            
    
    #For Length 3 
        
    elif (len(args) == 3):
        opcode = oprations[args[0]]
        if(args[1][0] == '['):
            if(args[2][0] != '['):
                rd = address[args[2]]
        else:
            rd = address[args[1]]
        
        if(args[2] in address):
            rs = address[args[2]]
            type = 0
        else:
            if(args[2][0] == '['):
                if(args[2][-2] == 'H'):
                    dm = args[2][1:-2]
                else :
                    dm = args[2][1:-1]
                type = 3
            else:
                if(args[2][-1] == 'H'):
                    imm = args [2][:-1]
                    a = int(imm , 16)
                else:
                    imm = args [2]
                    a = int(imm , 16)
                type = 2
        
        #MOV
        
        if(args[0] == "MOV"):
            if(args[1][0] == '['):
                out = args[2] + " = "
                if(args[2][0] != '['):
                    memory[int(args[1][-3] , 16)] = regValues[args[2]]
                    out += format(regValues[args[2]] , "02x") + "H"
                else:
                    out = "Error"
            else:
                out = args[1] + ' = '
                if (args[2] in address):
                    regValues[args[1]] = regValues[args[2]]
                    out += format(regValues[args[1]] , "02x") +"H"
                else:
                    regValues[args[1]] = a
                    
                    out += format(regValues[args[1]] , "02X") + "H"
                    
        #AND
        
        if(args[0] == "AND"):
            if(args[1][0] == '['):
                out = args[2] + " = "
                if(args[2][0] != '['):
                    memory[int(args[1][-2] , 16)] = memory[int(args[1][-2] , 16)] & regValues[args[2]]
                    out += format(regValues[args[2]] , "02x") + "H"
                else:
                    out = "Error"
            else:
                out = args[1] + ' = '
                if (args[2] in address):
                    regValues[args[1]] = regValues[args[1]] & regValues[args[2]]
                    out += format(regValues[args[1]] , "02x") +"H"
                else:
                    if(args[2][0] == '['):
                        regValues[args[1]] = regValues[args[1]] & memory[int(args[2][-3] , 16)]
                        out += format((regValues[args[1]] , "02x")) + "H"
                    else:
                        regValues[args[1]] = regValues[args[1]] & a
                        out += format(regValues[args[1]] , "02x") + "H"
            #Updationg Flag Registers
            
            flagReg[8] = 0
            flagReg[7] = parity(format(regValues[args[1]] , '08b'))
            flagReg[0] = 0
            flagReg[4] = int(format(regValues[args[1]] , '08b')[0] == '1')
            flagReg[5] = int(regValues[args[1]] == 0)
        
        # OR
        
        if(args[0] == "OR"):
            if(args[1][0] == '['):
                out = args[2] + " = "
                if(args[2][0] != '['):
                    memory[int(args[2][-3] , 16)] = memory[int(args[2][-3] , 16)] | regValues[args[2]]
                    out += format(regValues[args[2]] , "02x") + "H"
                else:
                    out = "Error"
            else:
                out = args[1] + ' = '
                if (args[2] in address):
                    regValues[args[1]] = regValues[args[1]] | regValues[args[2]]
                    out += format(regValues[args[1]] , "02x") +"H"
                else:
                    if(args[2][0] == '['):
                        regValues[args[1]] = regValues[args[1]] | memory[int(args[2][-3] , 16)]
                        out += format((regValues[args[1]] , "02x")) + "H"
                    else:
                        regValues[args[1]] = regValues[args[1]] | a
                        out += format(regValues[args[1]] , "02x") + "H"
            #Updationg Flag Registers
            
            flagReg[8] = 0
            flagReg[7] = parity(format(regValues[args[1]] , '08b'))
            flagReg[0] = 0
            flagReg[4] = int(format(regValues[args[1]] , '08b')[0] == '1')
            flagReg[5] = int(regValues[args[1]] == 0)
        
        # XOR
        
        if(args[0] == "XOR"):
            if(args[1][0] == '['):
                out = args[2] + " = "
                if(args[2][0] != '['):
                    memory[int(args[2][-3] , 16)] = memory[int(args[2][-3] , 16)] ^ regValues[args[2]]
                    out += format(regValues[args[2]] , "02x") + "H"
                else:
                    out = "Error"
            else:
                out = args[1] + ' = '
                if (args[2] in address):
                    regValues[args[1]] = regValues[args[1]] ^ regValues[args[2]]
                    out += format(regValues[args[1]] , "02x") +"H"
                else:
                    if(args[2][0] == '['):
                        regValues[args[1]] = regValues[args[1]] ^ memory[int(args[2][-3] , 16)]
                        out += format((regValues[args[1]] , "02x")) + "H"
                    else:
                        regValues[args[1]] = regValues[args[1]] ^ a
                        out += format(regValues[args[1]] , "02x") + "H"
            #Updationg Flag Registers
            
            flagReg[8] = 0
            flagReg[7] = parity(format(regValues[args[1]] , '08b'))
            flagReg[0] = 0
            flagReg[4] = int(regValues[args[1]] < 0 )
            flagReg[5] = int(regValues[args[1]] == 0)
            
        #XCHG
        
        if(args[0] == "XCHG"):
            out = args[1] +" = "
            a = regValues[args[1]]
            regValues[args[1]] = regValues[args[2]]
            regValues[args[2]] = a
            
            out += format(regValues[args[1]] , "02x") + "H"
            out += " " + args[2] + " = "
            out += format(regValues[args[2]] , "02x") + "H"
            
        # ADD
        
        if(args[0] == "ADD"):
            out = args[1] +" = "
            if(args[1][0] != '['):
                if(args[2] in address):
                    regValues[args[1]] += regValues[args[2]]
                    out += format(regValues[args[1]] , "02x") + "H"
                
                else:
                    if(args[2][0] == '['):
                        regValues[args[1]] = regValues[args[1]] + memory[int(args[2][-3] , 16)]
                        out += format(regValues[args[1]] , "02x") + "H"
            else:
                out = "Error"
            
            #Updationg Flag Registers
            
            flagReg[7] = parity(format(regValues[args[1]] , '08b'))
            flagReg[0] = 0
            flagReg[4] = int(format((regValues[args[1]] , '08b')) [0] == '1')
            flagReg[5] = int(regValues[args[1]] == 0)
        
        # SUB
        
        if(args[0] == "SUB"):
            out = args[1] +" = "
            if(args[1][0] != '['):
                if(args[2] in address):
                    regValues[args[1]] -= regValues[args[2]]
                    out += format(regValues[args[1]] , "02x") + "H"
                
                else:
                    if(args[2][0] == '['):
                        regValues[args[1]] = regValues[args[1]] - memory[int(args[2][-3] , 16)]
                        out += format(regValues[args[1]] , "02x") + "H"
            else:
                out = "Error"
            
            #Updationg Flag Registers
            
            flagReg[7] = parity(format(regValues[args[1]] , '08b'))
            flagReg[0] = 0
            flagReg[4] = int(format((regValues[args[1]] , '08b')) [0] == '1')
            flagReg[5] = int(regValues[args[1]] == 0)
            
    
    
    
    def convertHexadecimal(opcode , type , rd , rs , rs2 , imm , dm ):
        opstr = format(int(opcode) , '04b')
        typestr = format(type , '02b')
        rdstr = format(rd , '04b')
        rsstr = format(rs , '04b')
        Instruction = opstr + typestr + rdstr + rsstr
        if(type == 1):
            rs2str = format(rs2 , '04b')
            Instruction += rs2str
            
        return format(int (Instruction , 2) , '04x')
    
    
    instruction = convertHexadecimal(opcode, type, rd, rs, rs2, imm, dm)
    if(type == 2):
        instruction += " " + imm + " "
    elif(type == 3 ):
        instruction += " " + dm
        
    print("{:<20} {:<30} {:<30}".format(instruction , data , out ),"\n")
    print("Flag Register: ")
    print("_"*42)
    print("         OF DF IF TF SF ZF   AF   PF   CF ")
    print("|X|X|X|X|{0} |{1} |{2} |{3} |{4} |{5} |X|{6} |X|{7} |X|{8} |".format(flagReg[0],flagReg[1],flagReg[2],flagReg[3],flagReg[4],flagReg[5],flagReg[6],flagReg[7],flagReg[8]))
    print("_"*42)
    print("-"*75)
    return flag

#Opening File
file = open('input.txt' , 'r')
#Read Line By Line
data = file.readlines() 
out = ""

print("{:<20} {:<30} {:<30}".format('opcode' , 'Mnemonic codes' , 'Output') ,"\n")
print("-"*75)

for i in range(len(data)):
    if(data[i] != ""):
        a = decode(data[i].upper())
        if(a):
            break