# symbol table for Jack compiler


class SymbolTable:
    
    def __init__(self):
        self.class_table = {}  # {'name': [type, kind, #]}
        self.subroutine_table = {}
        
        self.class_static_index = 0
        self.class_field_index = 0
        self.subroutine_arg_index = 0
        self.subroutine_var_index = 0
    
    def start_subroutine(self):
        '''Start a new subroutine scope and resets the subroutine table'''
        self.subroutine_table.clear()
        self.subroutine_arg_index = 0
        self.subroutine_var_index = 0
    
    def define(self, name, jack_type, kind):
        '''collect entry: define a new identifier of the given name, type, and 
        kind;assign it a running index: static, filed: class scope;
        var arg: subroutine scope'''
        if kind == 'static':
            self.class_table[name] = (jack_type, kind, self.class_static_index)
            self.class_static_index += 1 
        elif kind == 'field':
            self.class_table[name] = (jack_type, kind, self.class_field_index)
            self.class_field_index += 1
        elif kind == 'arg':
            self.subroutine_table[name] = (jack_type, kind, self.subroutine_arg_index)
            self.subroutine_arg_index += 1
        elif kind == 'local':
            self.subroutine_table[name] = (jack_type, kind, self.subroutine_var_index)
            self.subroutine_var_index += 1 
        
    
    def var_count(self, kind):
        '''Return the number of variable given the type'''
        count = 0
        
        for key, value in self.class_table.items():
            if kind == value[1]:
                count += 1
        for key, value in self.subroutine_table.items():
            if kind == value[1]:
                count += 1
        
        return count 
        
    
    def kind_of(self, name):
        '''Return the kind of variable given the current scope'''
        if name in self.class_table:
            return self.class_table[name][1]
        if name in self.subroutine_table:
            return self.subroutine_table[name][1]
        
        return "NONE"
    
    def type_of(self, name):
        '''Return the type'''
        if name in self.class_table:
            return self.class_table[name][0]
        if name in self.subroutine_table:
            return self.subroutine_table[name][0]
    
    def index_of(self, name):
        '''Return the index of variable'''
        if name in self.class_table:
            return self.class_table[name][2]
        if name in self.subroutine_table:
            return self.subroutine_table[name][2]
    
    