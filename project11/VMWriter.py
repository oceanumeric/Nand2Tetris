# VM writer for Jack compiler


class VM_Writer:
    
    def __init__(self, vm_file):
        self.vm_file = open(vm_file, 'w')
        
    def __del__(self):
        self.vm_file.close()
        
    def write_push(self, segment, index):
        self.vm_file.write(f"push {segment} {index}\n")
        
    def write_pop(self, segment, index):
        self.vm_file.write(f"pop {segment} {index}\n")
        
    def write_arithmetic(self, command):
        if command == '+':
            self.vm_file.write("add")
        elif command == '-':
            self.vm_file.write("sub")
        elif command == '*':
            self.vm_file.write("call Math.multiply 2")
        elif command == '/':
            self.vm_file.write("call Math.divide 2")
        elif command == '&':
            self.vm_file.write("and")
        elif command == '|':
            self.vm_file.write("or")
        elif command == '<':
            self.vm_file.write("lt")
        elif command == '>':
            self.vm_file.write("gt")
        elif command == '=':
            self.vm_file.write("eq")
        elif command == '~':
            self.vm_file.write("not")
        elif command == 'neg': # Unary
            self.vm_file.write("neg")
            
        self.vm_file.write('\n')
        
    def write_label(self, label):
        self.vm_file.write(f"label {label}\n")
        
    def write_goto(self, label):
        self.vm_file.write(f"goto {label}\n")
        
    def write_if(self, label):
        self.vm_file.write(f"if-goto {label}\n")
        
    def write_call(self, name, n_args):
        self.vm_file.write(f"call {name} {n_args}\n")
        
    def write_function(self, name, n_locals):
        self.vm_file.write(f"function {name} {n_locals}\n")
        
    def write_return(self):
        self.vm_file.write("return\n")
    
    def write_alloc(self, size):
        self.write_push("constant", size)
        self.vm_file.write("call Memory.alloc 1\n")

    def write_sring(self, string):
        self.write_push("constant", len(string))
        self.write_call("String.new", 1)
        for char in string:
            unicode_rep = ord(char)  # return an integer representing the Unicode character
            self.write_push("constant", unicode_rep)
            self.write_call("String.appendChar", 2)
        
    
        