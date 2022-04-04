import argparse
import os 

file_parser = argparse.ArgumentParser(description="VMTranslator: translate VM code\
                                 to assembly code")
file_parser.add_argument('path')  # name, no need flag indicator
file_parser.add_argument('-b', type=str, default='yes')  # flag indicator -b something 
# -s: is simple function or not
file_parser.add_argument('-s', type=str, default='no',
                         help='Is a simple function or not')  
prompt_values = file_parser.parse_args()



# Two cases:
    # with booting: Stack Initialization, calling sys.init() and link files too
    # without booting: run a simple file directly 

"""
CODING STRUCTURE:
    Entry:
        prompt> command
        input: 
            python VMTranslator.py ./ProgramFlow/FibonacciSeries -b yes
            python VMTranslator.py ./ProgramFlow/FibonacciSeries/FibonacciSeries.vm -b no 
        output:
            folder_path, VM file, bool booting 
    
    Main:
        Input:
            folder_path, VM file, bool booting
        booting = no:
            translate VM file without booting
            return folder_path/VM_file.asm 
        booting = yes:
            translate VM file with booting
            return folder_path/folder.asm
        Output:
            translated assembly code 
    
    Main_Structure:
        load VM file
        clean VM file by deleting block comments and in-line comments
        parse each line and translate
            treat each function as a block:
                check function f_name
                translate until next 'function f_name'
                
                function f_name1:
                             
                function f_name2:
                
                function f_name3:
"""

class VMTranslator:
    # global variables to label eq, gt, and lt
    eqidx = 0
    gtidx = 0
    ltidx = 0
    retidx = 0
    def __init__(self, file_path, booting, simple):
        self.file_path = file_path
        self.booting = booting
        self.simple = simple
        self.assembly = []
        self.function_stack = []  # a stack to link all functions 
        self.file_name_label = []  # follows function in LIFO manner 
        
    def translate(self):
        if self.simple == 'yes':
            slach_idx = self.file_path.rfind('/')
            dot_idx= self.file_path.rfind('.')
            self.file_name_label = self.file_path[slach_idx+1:dot_idx]
            # file_path inclues vm file 
            # read and clea the file
            cleaned_code = self.__clean_code(self.file_path)
            # translate the file 
            # call __translate 
            self.__translate(cleaned_code, simple_branching=True)
            # write
            self.__write()
        else:
            # it must have a Sys.vm
            # # read and clean Sys.vm
            sys_vm = self.file_path + '/Sys.vm'
            cleaned_code= self.__clean_code(sys_vm)
            if self.booting == 'yes':
                # link all file first
                linked_file = self.__link_files()
                # read linked_file
                cleaned_code = []
                with open(linked_file, 'r') as f:
                    for line in f:
                        cleaned_code.append(line)
                # call bootstrapping function
                self.__booting()
                # translate 
                self.__translate(cleaned_code)
                # write
                self.__write()
            else:
                # No booting
                # No need to link all files
                # call __translate with default simple_branching 
                self.__translate(cleaned_code)
                # write
                self.__write()
    
    def __link_files(self):
        non_sys_files = []
        sys_vm = []
        slash_index = self.file_path[:-1].rfind('/')
        name = self.file_path[slash_index+1:][:-1]
        name = name + '.vm'
        for file in os.listdir(self.file_path+'/'):
            if file.endswith('.vm'):
                vm_file = self.file_path + file
                if 'Sys' in vm_file:
                    sys_vm = self.__clean_code(vm_file)
                elif name in vm_file:
                    # do not link the generated file 
                    pass 
                else:
                    non_sys_files.append(vm_file)
        for vm in non_sys_files:
            # read and clean
            cleaned_code = self.__clean_code(vm)
            sys_vm += cleaned_code
        
        slash_index = self.file_path[:-1].rfind('/')
        name = self.file_path[slash_index+1:][:-1]
        write_file = self.file_path + name +'.vm'
        f = open(write_file, 'w')
        for x in sys_vm:
            f.write(x+'\n')
        f.close()
        
        return write_file
            
    def __clean_code(self, file):
        cleaned_code = []
        with open(file, 'r') as f:
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
    
    def __booting(self):
        # SP = 256
        # Call Sys.init 
        self.assembly.append('// Booting')
        self.assembly.append('// call Sys.init')
        self.assembly.append('@256')
        self.assembly.append('D=A')
        self.assembly.append('@SP')
        self.assembly.append('M=D')
        self.assembly.append('@BOOTING_Return')
        self.assembly.append('D=A')
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
        self.assembly.append('@5')
        self.assembly.append('D=D-A')
        self.assembly.append('@n_args')
        self.assembly.append('D=D-A')
        self.assembly.append('@ARG')
        self.assembly.append('M=D')
        self.assembly.append('@SP')
        self.assembly.append('D=M')
        self.assembly.append('@LCL')
        self.assembly.append('M=D')
        self.assembly.append('@Sys.init')
        self.assembly.append('0;JMP')
        self.assembly.append('(BOOTING_Return)')
        
    def __translate(self, cleaned_code, simple_branching=False):
        # we have: push pop segment index 
        # arithemtic-logic commands: add sub neg eq gt lt and or not
        # label command, goto command, if-goto label
        # function, call, return 
        arithmetic_logic_commands = ['add', 'sub', 'neg',
                                     'eq', 'gt', 'lt',
                                     'add', 'or', 'not']
        for line in cleaned_code:
            line = line.strip()
            if 'push' in line:
                self.__map_memory(line)
            if 'pop' in line:
                self.__map_memory(line)
            if line in arithmetic_logic_commands:
                self.__map_arithmetic(line)
            if 'function' in line:
                self.__map_function(line)
            if 'call' in line:
                self.__map_call(line)
            if 'return' in line:
                self.__map_return(line)
            else:
                self.__map_branching(line, simple_branching)
        
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
                self.assembly.append('@'+self.file_name_label[-1]+number)
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
                self.assembly.append('@'+self.file_name_label[-1]+number)
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
                
    def __map_branching(self, line, simple=False):
        label_idx = line.find(' ')
        if simple:
            symbol_name = line[label_idx+1:]
        else:
            function_label = self.function_stack[-1]
            symbol_name = line[label_idx+1:]
            symbol_name = function_label + '$' + symbol_name
        if 'label' in line:
            self.assembly.append('//' + line)
            self.assembly.append(f'({symbol_name})')
        if 'goto' in line[:4]:
            self.assembly.append('//' + line)
            self.assembly.append(f'@{symbol_name}')
            self.assembly.append('0;JMP')
        if 'if-goto' in line:
            self.assembly.append('//' + line)
            self.assembly.append('@SP')
            self.assembly.append('AM=M-1')
            self.assembly.append('D=M')
            self.assembly.append(f'@{symbol_name}')
            self.assembly.append('D;JNE')
    
    def __map_function(self, line):
        name_idx = line.find(' ')
        var_idx = line.rfind(' ')
        function_name = line[name_idx+1:var_idx]
        num_local_var = int(line[var_idx+1:])
        self.function_stack.append(function_name)
        dot_idx = function_name.find('.')
        file_name = function_name[:dot_idx]
        if self.simple != 'yes':
            self.file_name_label.append(file_name)
        self.assembly.append('// FUNCTION: ' + line)
        self.assembly.append(f'({function_name})')
        for i in range(num_local_var):
            self.assembly.append('@0')
            self.assembly.append('D=A')
            self.assembly.append('@SP')
            self.assembly.append('AM=M+1')
            self.assembly.append('A=A-1')
            self.assembly.append('M=D')
    
    def __map_call(self, line):
        line = line.strip()
        name_idx = line.find(' ')
        arg_idx = line.rfind(' ')
        function_name = line[name_idx+1:arg_idx]
        num_args = line[arg_idx+1:]
        self.assembly.append('// CALL: ' + line)
        self.assembly.append('@'+function_name+'$ret.'+str(VMTranslator.retidx))
        self.assembly.append('D=A')
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
        self.assembly.append('@5')
        self.assembly.append('D=D-A')
        self.assembly.append(f'@{num_args}')
        self.assembly.append('D=D-A')
        self.assembly.append('@ARG')
        self.assembly.append('M=D')
        self.assembly.append('@SP')
        self.assembly.append('D=M')
        self.assembly.append('@LCL')
        self.assembly.append('M=D')
        self.assembly.append(f'@{function_name}')
        self.assembly.append('0;JMP')
        self.assembly.append('('+function_name+'$ret.'+str(VMTranslator.retidx)+')')
        VMTranslator.retidx += 1
    
    def __map_return(self, line):
        self.assembly.append('// RETURN: ' + line)
        self.assembly.append('@LCL')
        self.assembly.append('D=M')
        self.assembly.append('@frame')
        self.assembly.append('M=D')
        self.assembly.append('@frame')
        self.assembly.append('D=M')
        self.assembly.append('@5')
        self.assembly.append('D=D-A')
        self.assembly.append('A=D')
        self.assembly.append('D=M')
        self.assembly.append('@ret_address')
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
        self.assembly.append('@frame')
        self.assembly.append('A=M-1')
        self.assembly.append('D=M')
        self.assembly.append('@THAT')
        self.assembly.append('M=D')
        self.assembly.append('@2')
        self.assembly.append('D=A')
        self.assembly.append('@frame')
        self.assembly.append('A=M-D')
        self.assembly.append('D=M')
        self.assembly.append('@THIS')
        self.assembly.append('M=D')
        self.assembly.append('@3')
        self.assembly.append('D=A')
        self.assembly.append('@frame')
        self.assembly.append('A=M-D')
        self.assembly.append('D=M')
        self.assembly.append('@ARG')
        self.assembly.append('M=D')
        self.assembly.append('@4')
        self.assembly.append('D=A')
        self.assembly.append('@frame')
        self.assembly.append('A=M-D')
        self.assembly.append('D=M')
        self.assembly.append('@LCL')
        self.assembly.append('M=D')
        self.assembly.append('@ret_address')
        self.assembly.append('A=M')
        self.assembly.append('0;JMP')
    
    def __write(self):
        if self.simple == 'yes':
            self.assembly.append('(END)')
            self.assembly.append('@END')
            self.assembly.append('0;JMP')
            slash_index = self.file_path.rfind('/')
            name_index = self.file_path[slash_index+1:].find('vm')
            name = self.file_path[slash_index+1:][:name_index]
            path = self.file_path[:slash_index]+'/'+name+'asm'
            f = open(path, 'w')
            for x in self.assembly:
                f.write(x+'\n')
            f.close()
        else:
            slash_index = self.file_path[:-1].rfind('/')
            name = self.file_path[slash_index+1:][:-1]
            write_file = self.file_path + '/' + name +'.asm'
            f = open(write_file, 'w')
            for x in self.assembly:
                f.write(x+'\n')
            f.close()
        
if __name__ == "__main__":
    vmt = VMTranslator(prompt_values.path, prompt_values.b, prompt_values.s)
    vmt.translate()
