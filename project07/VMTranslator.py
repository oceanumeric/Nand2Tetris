import argparse

file_parser = argparse.ArgumentParser(description="VMTranslator: translate VM code\
                                 to assembly code")
file_parser.add_argument('filename')
args = file_parser.parse_args()
file_path = args.filename

slash_index = file_path.rfind('/')
name_index = file_path[slash_index+1:].find('vm')
file_name = file_path[slash_index+1:][:name_index]


class VMTranslator:
    """
    stack base address SP=256: @256, D=A, @SP, M=D has been initialized already
    Address register:
        SP - RAM[0] - pointer 256 (fixed)
        LCL - RAM[1] - pointer 
        ARG - RAM[2] - pointer
        THIS - RAM[3] - pointer
        THAT - RAM[4] - pointer
        TEMP - RAM[5-12]
        R13-R15 - RAM[13-15]
        Static Variables - RAM[16-255] (maximum number of static variable = 240)
    """
    eqidx = 0
    gtidx = 0
    ltidx = 0
    def __init__(self, vmfile):
        self.file = vmfile
        self.assembly = []
            
    def parser(self):
        with open (self.file, 'r') as f:
            for line in f:
                if line != '\n':
                    line = line.strip()
                    if line[:2] != "//":
                        # delete inline comments 
                        comment_index = line.find('//')
                        if comment_index != -1:
                            line = line[:comment_index]
                        if self.__command_type(line) == 'c_push':
                            self.__map_memory(line)
                        elif self.__command_type(line) == 'c_pop':
                            self.__map_memory(line)
                        else:
                            self.__map_arithmetic(line)
                            
    
    # private method
    def __command_type(self, line):
        arithmetic_logic_commands = ['add', 'sub', 'neg',
                                     'eq', 'gt', 'lt',
                                     'add', 'or', 'not']
        line = line.strip()
        if 'push' in line:
            return 'c_push'
        if 'pop' in line:
            return 'c_pop'
        if line in arithmetic_logic_commands:
            return 'c_arithmetic'
        
    
    def __map_memory(self, line):
        memory_dict = {
            'local': 'LCL',
            'argument': 'ARG',
            'this': 'THIS',
            'that': 'THAT',
            'temp': 'TEMP'
        }
        # be called only if the command type is c_push, c_pop
        first_space_idx = line.find(' ')
        last_space_idx = line.rfind(' ')
        command = line[:first_space_idx]
        segment = line[first_space_idx+1:last_space_idx]
        number = line[last_space_idx+1:]
        if segment == 'temp':
            number = int(number)
            number += 5
            number = str(number)
        if command == 'push':
            # move from memory to stack
            if segment == 'constant':
                self.assembly.append('//' + line)
                self.assembly.append(f'@{number}')
                self.assembly.append('D=A')
                self.assembly.append('@SP')
                self.assembly.append('AM=M+1')
                self.assembly.append('A=A-1')
                self.assembly.append('M=D')
            elif segment == 'temp':
                self.assembly.append('// ' + line)
                self.assembly.append(f'@{number}')
                self.assembly.append('D=M')
                self.assembly.append('@SP')
                self.assembly.append('AM=M+1')
                self.assembly.append('A=A-1')
                self.assembly.append('M=D')
            elif segment == 'pointer':
                pointer_map = {'0': 'THIS', '1': 'THAT'}
                self.assembly.append('// ' + line)
                self.assembly.append(f'@{pointer_map[number]}')
                self.assembly.append('D=M')
                self.assembly.append('@SP')
                self.assembly.append('AM=M+1')
                self.assembly.append('A=A-1')
                self.assembly.append('M=D')
            elif segment == 'static':
                self.assembly.append('// ' + line)
                self.assembly.append('@'+file_name+number)
                self.assembly.append('D=M')
                self.assembly.append('@SP')
                self.assembly.append('AM=M+1')
                self.assembly.append('A=A-1')
                self.assembly.append('M=D')
            else:
                self.assembly.append('// ' + line)
                self.assembly.append(f'@{memory_dict[segment]}')
                self.assembly.append('D=M')
                self.assembly.append(f'@{number}')
                self.assembly.append('A=A+D')
                self.assembly.append('D=M')
                self.assembly.append('@SP')
                self.assembly.append('AM=M+1')
                self.assembly.append('A=A-1')
                self.assembly.append('M=D')
        else:
            if segment == 'temp':
                # pop: move from stack to memory
                self.assembly.append('// ' + line)
                self.assembly.append('@SP')
                self.assembly.append('AM=M-1')
                self.assembly.append('D=M')
                self.assembly.append(f'@{number}')
                self.assembly.append('M=D')
            elif segment == 'pointer':
                pointer_map = {'0': 'THIS', '1': 'THAT'}
                self.assembly.append('// ' + line)
                self.assembly.append('@SP')
                self.assembly.append('AM=M-1')
                self.assembly.append('D=M')
                self.assembly.append(f'@{pointer_map[number]}')
                self.assembly.append('M=D')
            elif segment == 'static':
                self.assembly.append('// ' + line)
                self.assembly.append('@SP')
                self.assembly.append('AM=M-1')
                self.assembly.append('D=M')
                self.assembly.append('@'+file_name+number)
                self.assembly.append('M=D')
            else:
                # pop: move from stack to memory
                self.assembly.append('// ' + line)
                self.assembly.append(f'@{memory_dict[segment]}')
                self.assembly.append('D=M')
                self.assembly.append(f'@{number}')
                self.assembly.append('D=D+A')
                self.assembly.append('@R13')
                self.assembly.append('M=D')
                self.assembly.append('@SP')
                self.assembly.append('AM=M-1')
                self.assembly.append('D=M')
                self.assembly.append('@R13')
                self.assembly.append('A=M')
                self.assembly.append('M=D')
            
    def __map_arithmetic(self, line):
        if line == 'add':
            self.assembly.append('// ' + line)
            self.assembly.append('@SP')
            self.assembly.append('AM=M-1')
            self.assembly.append('D=M')
            self.assembly.append('A=A-1')
            self.assembly.append('M=M+D')
        elif line == 'sub':
            self.assembly.append('// ' + line)
            self.assembly.append('@SP')
            self.assembly.append('AM=M-1')
            self.assembly.append('D=M')
            self.assembly.append('A=A-1')
            self.assembly.append('M=M-D')
        elif line == 'neg':
            self.assembly.append('// ' + line)
            self.assembly.append('@SP')
            self.assembly.append('A=M-1')
            self.assembly.append('D=-M')
            self.assembly.append('M=D')
        elif line == 'eq':
            self.assembly.append('// compare whether ' + line)
            self.assembly.append('@SP')
            self.assembly.append('AM=M-1')
            self.assembly.append('D=M  ')
            self.assembly.append('A=A-1 ')
            self.assembly.append('M=M-D')
            self.assembly.append('@SP')
            self.assembly.append('A=M-1  ')
            self.assembly.append('D=M')
            self.assembly.append('@EQUAL'+str(VMTranslator.eqidx))
            self.assembly.append('D;JEQ')
            self.assembly.append('@SP')
            self.assembly.append('A=M-1')
            self.assembly.append('M=0')
            self.assembly.append('@EQEND'+str(VMTranslator.eqidx))
            self.assembly.append('0;JMP')
            self.assembly.append('(EQUAL'+str(VMTranslator.eqidx)+')')
            self.assembly.append('@SP')
            self.assembly.append('A=M-1')
            self.assembly.append('M=-1')
            self.assembly.append('(EQEND'+str(VMTranslator.eqidx)+')')
            VMTranslator.eqidx += 1 
        elif line == 'gt':
            self.assembly.append('// compare whether ' + line)
            self.assembly.append('@SP')
            self.assembly.append('AM=M-1')
            self.assembly.append('D=M')
            self.assembly.append('A=A-1 ')
            self.assembly.append('M=M-D  ')
            self.assembly.append('@SP')
            self.assembly.append('A=M-1')
            self.assembly.append('D=M')
            self.assembly.append('@GREATER'+str(VMTranslator.gtidx))
            self.assembly.append('D;JGT')
            self.assembly.append('@SP')
            self.assembly.append('A=M-1')
            self.assembly.append('M=0')
            self.assembly.append('@GTEND'+str(VMTranslator.gtidx))
            self.assembly.append('0;JMP')
            self.assembly.append('(GREATER'+str(VMTranslator.gtidx)+')')
            self.assembly.append('@SP')
            self.assembly.append('A=M-1')
            self.assembly.append('M=-1')
            self.assembly.append('(GTEND'+str(VMTranslator.gtidx)+')')
            VMTranslator.gtidx += 1 
        elif line == 'lt':
            self.assembly.append('// compare whether ' + line)
            self.assembly.append('@SP')
            self.assembly.append('AM=M-1')
            self.assembly.append('D=M')
            self.assembly.append('A=A-1 ')
            self.assembly.append('M=M-D')
            self.assembly.append('@SP')
            self.assembly.append('A=M-1')
            self.assembly.append('D=M')
            self.assembly.append('@LESS'+str(VMTranslator.ltidx))
            self.assembly.append('D;JLT')
            self.assembly.append('@SP')
            self.assembly.append('A=M-1')
            self.assembly.append('M=0')
            self.assembly.append('@LTEND'+str(VMTranslator.ltidx))
            self.assembly.append('0;JMP')
            self.assembly.append('(LESS'+str(VMTranslator.ltidx)+')')
            self.assembly.append('@SP')
            self.assembly.append('A=M-1')
            self.assembly.append('M=-1')
            self.assembly.append('(LTEND'+str(VMTranslator.ltidx)+')')
            VMTranslator.ltidx += 1
        elif line == 'and':
            self.assembly.append('// bitwise operation ' + line)
            self.assembly.append('@SP')
            self.assembly.append('AM=M-1')
            self.assembly.append('D=M ')
            self.assembly.append('A=A-1 ')
            self.assembly.append('M=D&M')
        elif line == 'or':
            self.assembly.append('// bitwise operation ' + line)
            self.assembly.append('@SP')
            self.assembly.append('AM=M-1')
            self.assembly.append('D=M')
            self.assembly.append('A=A-1 ')
            self.assembly.append('M=D|M')
        elif line == 'not':
            self.assembly.append('// bitwise operation ' + line)
            self.assembly.append('@SP')
            self.assembly.append('A=M-1')
            self.assembly.append('D=!M')
            self.assembly.append('M=D')
        else:
            pass
        
    def write(self, file_path):
        # add infinite loop 
        self.assembly.append('(END)')
        self.assembly.append('@END')
        self.assembly.append('0;JMP')
        slash_index = file_path.rfind('/')
        name_index = file_path[slash_index+1:].find('vm')
        name = file_path[slash_index+1:][:name_index]
        path = file_path[:slash_index]+'/'+name+'asm'
        f = open(path, 'w')
        for x in self.assembly:
            f.write(x+'\n')
        f.close()
        


if __name__ == "__main__":
    vmt = VMTranslator(file_path)
    vmt.parser()
    vmt.write(file_path)