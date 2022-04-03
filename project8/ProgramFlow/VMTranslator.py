import argparse

file_parser = argparse.ArgumentParser(description="VMTranslator: translate VM code\
                                 to assembly code")
file_parser.add_argument('filename')
args = file_parser.parse_args()
folder_path = args.filename

slash_idx = folder_path.rfind('/')
destination_file = folder_path[slash_idx+1:]
file_name = destination_file
file_path = folder_path + '/' + destination_file + '.vm'


def _clean_line(code_file):
    cleaned_code = []
    with open(code_file, 'r') as f:
        for line in f:
            if line != '\n':
                line = line.strip()
                if line[:2] != "//":
                    # delete inline comments 
                    comment_index = line.find('//')
                    if comment_index != -1:
                        line = line[:comment_index]
                    line = line.strip()
                    cleaned_code.append(line)
    
    return cleaned_code


def link_file(folder_path):
    linked_file = []
    slash_idx = folder_path.rfind('/')
    destination_file = folder_path[slash_idx+1:]
    sys_vm = folder_path + '/Sys.vm'
    neat_code = _clean_line(sys_vm)
    for line in neat_code:
        if 'call' in line:
            linked_file.append(line)
            space_idx = line.find(' ')
            space_ridx = line.rfind(' ')
            dot_idx = line.find('.')
            file_name = line[space_idx+1:dot_idx]
            file = folder_path + '/' + file_name + '.vm'
            neat_code2 = _clean_line(file)
            function_name = line[space_idx+1:space_ridx]
            for line2 in neat_code2:
                if line2[:-2] == 'function ' + function_name:
                    function_idx = neat_code2.index(line2)
                    while neat_code2[function_idx] != 'return':
                        linked_file.append(neat_code2[function_idx])
                        function_idx += 1
                    linked_file.append(neat_code2[function_idx])
        else:
            linked_file.append(line)
            
    # write the file
    final_file = folder_path + '/' + destination_file + '.vm'
    f = open(final_file, 'w')
    for x in linked_file:
        f.write(x+'\n')
    f.close()
    
    
     
        


class VMTranslator:
    """
    All functions start with Sys.vm
    function Sys.init 0
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
        self.return_label = []
        
        # Bootstrap initializaton
        # self.assembly.append('// Bootstrap Initialization')
        # self.assembly.append('@256')
        # self.assembly.append('D=A')
        # self.assembly.append('@SP')
        # self.assembly.append('M=D')
        # self.assembly.append('@-1')
        # self.assembly.append('D=A')
        # self.assembly.append('@LCL')
        # self.assembly.append('M=D')
        # self.assembly.append('@-2')
        # self.assembly.append('D=A')
        # self.assembly.append('@ARG')
        # self.assembly.append('M=D')
        # self.assembly.append('@-3')
        # self.assembly.append('D=A')
        # self.assembly.append('@THIS')
        # self.assembly.append('M=D')
        # self.assembly.append('@-1')
        # self.assembly.append('D=A')
        # self.assembly.append('@THAT')
        # self.assembly.append('M=D')
            
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
                        line = line.strip()
                        if line == 'function Sys.init 0':
                            self.__sys_init(line)
                        elif self.__command_type(line) == 'c_push':
                            self.__map_memory(line)
                        elif self.__command_type(line) == 'c_pop':
                            self.__map_memory(line)
                        elif self.__command_type(line) == 'branching':
                            self.__map_branching(line)
                        elif self.__command_type(line) == 'calling':
                            self.__call(line)
                        elif 'function' == line[:8]:
                            self.__single_function(line)
                        elif line == 'return':
                            self.__return(line, self.return_label.pop())
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
        if 'label' in line:
            return 'branching'
        if 'goto' in line:
            return 'branching'
        if 'if-goto' in line:
            return 'branching'
        if line in arithmetic_logic_commands:
            return 'c_arithmetic'
        if 'call' in line:
            return 'calling'
        
    
    def __map_memory(self, line):
        memory_dict = {
            'local': 'LCL',
            'argument': 'ARG',
            'this': 'THIS',
            'that': 'THAT',
            'temp': 'TEMP'
        }
        # be called only if the command type is c_push, c_pop
        line = line.strip()
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
        
    def __map_branching(self, line):
        if 'label' in line:
            label_idx = line.find(' ')
            symbol_name = line[label_idx+1:]
            self.assembly.append('//' + line)
            self.assembly.append(f'({symbol_name})')
        if 'goto' in line[:4]:
            label_idx = line.find(' ')
            symbol_name = line[label_idx+1:]
            self.assembly.append('//' + line)
            self.assembly.append(f'@{symbol_name}')
            self.assembly.append('0;JMP')
        if 'if-goto' in line:
            label_idx = line.find(' ')
            symbol_name = line[label_idx+1:]
            self.assembly.append('//' + line)
            self.assembly.append('@SP')
            self.assembly.append('AM=M-1')
            self.assembly.append('D=M')
            self.assembly.append(f'@{symbol_name}')
            self.assembly.append('D;JNE')
     
    def __single_function(self, line):
        line = line.strip()
        name_idx = line.find(' ')
        var_idx = line.rfind(' ')
        function_name = line[name_idx+1:var_idx]
        function_name = function_name.upper()
        num_local_var = int(line[var_idx+1:])
        self.assembly.append('// FUNCTION: ' + line)
        self.assembly.append(f'({function_name})')
        for i in range(num_local_var):
            self.assembly.append('@0')
            self.assembly.append('D=A')
            self.assembly.append('@SP')
            self.assembly.append('AM=M+1')
            self.assembly.append('A=A-1')
            self.assembly.append('M=D')
            
    def __return(self, line, return_label):
        self.assembly.append('// RETURN: ' + line)
        self.assembly.append('@LCL')
        self.assembly.append('D=M')
        self.assembly.append('@R13')
        self.assembly.append('M=D')
        self.assembly.append('@5')
        self.assembly.append('D=A')
        self.assembly.append('@R13')
        self.assembly.append('A=M-D')
        self.assembly.append('D=M')
        self.assembly.append('@R14')
        self.assembly.append('M=D')
        self.assembly.append('@SP')
        self.assembly.append('AM=M-1')
        self.assembly.append('D=M')
        self.assembly.append('@ARG')
        self.assembly.append('A=M')
        self.assembly.append('M=D')
        self.assembly.append('@ARG')
        self.assembly.append('D=M+1')
        self.assembly.append('@SP')
        self.assembly.append('M=D')
        self.assembly.append('@R13')
        self.assembly.append('A=M-1')
        self.assembly.append('D=M')
        self.assembly.append('@THAT')
        self.assembly.append('M=D')
        self.assembly.append('@2')
        self.assembly.append('D=A')
        self.assembly.append('@R13')
        self.assembly.append('A=M-D')
        self.assembly.append('D=M')
        self.assembly.append('@THIS')
        self.assembly.append('M=D')
        self.assembly.append('@3')
        self.assembly.append('D=A')
        self.assembly.append('@R13')
        self.assembly.append('A=M-D')
        self.assembly.append('D=M')
        self.assembly.append('@ARG')
        self.assembly.append('M=D')
        self.assembly.append('@4')
        self.assembly.append('D=A')
        self.assembly.append('@R13')
        self.assembly.append('A=M-D')
        self.assembly.append('D=M')
        self.assembly.append('@LCL')
        self.assembly.append('M=D')
        self.assembly.append(f'@{return_label[1:-1]}')
        self.assembly.append('0;JMP')
        
    def __sys_init(self, line):
        self.assembly.append('// ' + line)
        self.assembly.append('@SP')
        self.assembly.append('D=M')
        self.assembly.append('@SP')
        self.assembly.append('AM=M+1')
        self.assembly.append('A=A-1')
        self.assembly.append('M=D')
        self.assembly.append('@LCL')
        self.assembly.append('D=M')
        self.assembly.append('@SP')
        self.assembly.append('AM=M+1')
        self.assembly.append('A=A-1')
        self.assembly.append('M=D')
        self.assembly.append('@ARG')
        self.assembly.append('D=M')
        self.assembly.append('@SP')
        self.assembly.append('AM=M+1')
        self.assembly.append('A=A-1')
        self.assembly.append('M=D')
        self.assembly.append('@THIS')
        self.assembly.append('D=M')
        self.assembly.append('@SP')
        self.assembly.append('AM=M+1')
        self.assembly.append('A=A-1')
        self.assembly.append('M=D')
        self.assembly.append('@THAT')
        self.assembly.append('D=M')
        self.assembly.append('@SP')
        self.assembly.append('AM=M+1')
        self.assembly.append('A=A-1')
        self.assembly.append('M=D')
        self.assembly.append('@256')
        self.assembly.append('D=A')
        self.assembly.append('@ARG')
        self.assembly.append('M=D')
        self.assembly.append('@SP')
        self.assembly.append('D=M')
        self.assembly.append('@LCL')
        self.assembly.append('M=D')
    
    def __call(self, line):
        line = line.strip()
        name_idx = line.find(' ')
        arg_idx = line.rfind(' ')
        function_name = line[name_idx+1:arg_idx]
        function_name = function_name.upper()
        num_args = line[arg_idx+1:]
        self.assembly.append('// ' + line)
        self.assembly.append(f'@{num_args}')
        self.assembly.append('D=A')
        self.assembly.append('@num_args')
        self.assembly.append('M=D')
        self.assembly.append('@num_args')
        self.assembly.append('D=M')
        self.assembly.append('@SP')
        self.assembly.append('D=M-D')
        self.assembly.append('@ARG')
        self.assembly.append('M=D')
        self.assembly.append('@ARG')
        self.assembly.append('D=M')
        self.assembly.append('@SP')
        self.assembly.append('AM=M+1')
        self.assembly.append('A=A-1')
        self.assembly.append('M=D')
        self.assembly.append('@LCL')
        self.assembly.append('D=M')
        self.assembly.append('@SP')
        self.assembly.append('AM=M+1')
        self.assembly.append('A=A-1')
        self.assembly.append('M=D')
        self.assembly.append('@ARG')
        self.assembly.append('D=M')
        self.assembly.append('@SP')
        self.assembly.append('AM=M+1')
        self.assembly.append('A=A-1')
        self.assembly.append('M=D')
        self.assembly.append('@THIS')
        self.assembly.append('D=M')
        self.assembly.append('@SP')
        self.assembly.append('AM=M+1')
        self.assembly.append('A=A-1')
        self.assembly.append('M=D')
        self.assembly.append('@THAT')
        self.assembly.append('D=M')
        self.assembly.append('@SP')
        self.assembly.append('AM=M+1')
        self.assembly.append('A=A-1')
        self.assembly.append('M=D')
        self.assembly.append('@SP')
        self.assembly.append('D=M')
        self.assembly.append('@LCL')
        self.assembly.append('M=D')
        self.assembly.append(f'@{function_name}')
        self.assembly.append('0;JMP')
        return_label = f'({function_name}'+'$RETURN)'
        self.assembly.append(return_label)
        self.return_label.append(return_label)     
    
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
    # link_file(folder_path)
    vmt = VMTranslator(file_path)
    vmt.parser()
    vmt.write(file_path)
