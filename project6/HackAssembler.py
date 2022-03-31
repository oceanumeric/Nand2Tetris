import argparse

# command line propmt parser 
parser = argparse.ArgumentParser(description="Translate Assembly to Binary Code")
parser.add_argument('filename')
args = parser.parse_args()
file_path = args.filename


# a class to parse line
class Parser:
    symbols_map = {
            'R0': 0,
            'R1': 1,
            'R2': 2,
            'R3': 3,
            'R4': 4,
            'R5': 5,
            'R6': 6,
            'R7': 7, 
            'R8': 8,
            'R9': 9,
            'R10': 10,
            'R11': 11,
            'R12': 12,
            'R13': 13,
            'R14': 14,
            'R15': 15,
            'SCREEN': 16384,
            'KBD': 24576,
            'SP': 0,
            'LCL': 1,
            'ARG': 2,
            'THIS': 3,
            'THAT': 4
            
        }
    comp_map = {'0': '0101010', 
                 '1': '0111111', 
                 '-1': '0111010', 
                 'D': '0001100', 
                 'A': '0110000', 
                 'M': '1110000', '!D': '0001101', '!A': '0110001', 
                 '!M': '1110001', '-D': '0001111', '-A': '0110011', 
                 '-M': '1110011', 'D+1': '0011111', 'A+1': '0110111',
                 'M+1': '1110111', 'D-1': '0001110', 'A-1': '0110010', 
                 'M-1': '1110010', 'D+A': '0000010', 'D+M': '1000010', 
                 'D-A': '0010011', 'D-M': '1010011', 'A-D': '0000111', 
                 'M-D': '1000111', 'D&A': '0000000', 'D&M': '1000000', 
                 'D|A': '0010101', 'D|M': '1010101'}
    dest_map = {'null': '000',
                 'M': '001', 
                 'D': '010',
                 'MD': '011',
                 'A': '100',
                 'AM': '101',
                  'AD': '110',
                  'AMD': '111'}
    jump_map = {'null': '000',
                'JGT': '001',
                 'JEQ': '010',
                 'JGE': '011',
                 'JLT': '100',
                 'JNE': '101',
                 'JLE': '110',
                 'JMP': '111'}
    variable_count = 16
  
    def __init__(self, file_path):
        self.file = open(file_path, 'r')
        self.lines = []
        self.instructions = {}
        self.symbols = {}
        self.binary = []
                    
    def translate(self):
        for line in self.file.readlines():
            line = Parser.advance(line)
            if line is not None:
                self.lines.append(line)
        count = 0
        label_count = 0
        for line in self.lines:
            line = line.strip()
            if line.find('(') == -1:
                self.instructions[str(count)] = line
                count += 1
            else:
                self.instructions['label'+str(label_count)] = line[1:-1]
                label_count += 1
        # first parsing: extract labels 
        key_list = list(self.instructions.keys())
        value_list = list(self.instructions.values())
        for idx, value in enumerate(key_list):
            if 'label' in value:
                # check whether following ones are label or not
                tmp = idx 
                while 'label' in key_list[tmp]:
                    tmp += 1
                if value_list[idx] not in Parser.symbols_map:
                    Parser.symbols_map[value_list[idx]] = key_list[tmp]
        
        # second parsing
        for line in self.lines:
            Parser.instruction_extract(self, line)
    
    def advance(line):
        if line != '\n':
                # skip the blank line 
                line = line.strip()
                if line[:2] != "//":
                    # delete inline comments 
                    comment_index = line.find('//')
                    if comment_index != -1:
                        line = line[:comment_index]
                    return line
                
    def instruction_extract(self, line):
        # A-instruction
        if line[0] == "@":
            symbol = line[1:]
            if symbol in Parser.symbols_map:
                value = Parser.symbols_map.get(symbol)
                value = int(value)
                self.binary.append('0'+'{0:015b}'.format(value))
            else:
                try:
                    value = int(symbol)
                    self.binary.append('0'+'{0:015b}'.format(value))
                except:
                    Parser.symbols_map[symbol] = Parser.variable_count
                    self.binary.append('0'+'{0:015b}'.format(Parser.variable_count))
                    Parser.variable_count += 1 
        elif line[0] == '(':
            pass
        else:
            # C instruction
            semicolon = line.find(';')
            # jump case 
            if semicolon != -1:
                jump = line[semicolon+1:].strip()
                equal = line.find('=')
                if equal != -1:
                    dest = line[:equal].strip()
                    comp = line[equal:].strip()
                    self.binary.append(
                        '111'+
                        Parser.dest_map[dest]+
                        Parser.comp_map[comp]+
                        Parser.jump_map[jump]
                        )
                else:
                    comp = line[:semicolon].strip()
                    self.binary.append(
                        '111'+
                        Parser.comp_map[comp]+
                                       '000'+
                        Parser.jump_map[jump])
            else:
                equal = line.find('=')
                dest = line[:equal].strip()
                comp = line[equal+1:].strip()
                self.binary.append(
                    '111'+
                    Parser.comp_map[comp]+
                        Parser.dest_map[dest]+
                        '000')
                
    def write(self, file_path):
        slash_index = file_path.rfind('/')
        name_index = file_path[slash_index+1:].find('asm')
        name = file_path[slash_index+1:][:name_index]
        path = file_path[:slash_index]+'/'+name+'hack'
        f = open(path, 'w')
        for x in self.binary:
            f.write(x+'\n')
        f.close()
        
        
        
    
if __name__ == "__main__":
    # stream each line
    parsing = Parser(file_path)
    parsing.translate()
    parsing.write(file_path)
    
        
        
        

            
