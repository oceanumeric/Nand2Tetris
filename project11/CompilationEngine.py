# A Compilation Engine for Jack Language 
"""
Compile Jack Source code into XML file 

Jack Grammar:

statements: statement*
statement: let_statement | if_statement | while_statement
let_statement: 'let' var_name '=' expression ';'
if_statement: 'if' '(' expression ')' '{' statements '}'
while_statement: 'while' '(' expression ')' '{' statements '}'
expression: term (op term)? 
term: var_name | constant
var_name: sting
constant: a non-negative integer 
op: '+, -, * /' 
"""

from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VM_Writer
import sys
import os 


class CompilationEngine:
    
    def __init__(self, file_path):
        self.tokenizer = JackTokenizer(file_path) 
        if self.tokenizer.has_more_tokens():  # initialize the first move
            self.tokenizer.advance()
            
        # initialize the table and vm file
        self.symbol_table = SymbolTable()  # a dictonary {name: (type, kind, #)}
        
        # vm file 
        jack_idx = file_path.find('.jack')
        vm_file = file_path[:jack_idx] + '.vm'
        self.vm = VM_Writer(vm_file)
        
        # initializing label index
        self.label_idx = 0
        self.if_idx = 0 
        self.while_idx = 0
        
        # start to compile class 
        self.compile_class()
        
    def compile_class(self):
        '''At this stage, we only deal with keywords and symbols.
        like class Main() \{ subroutine parts \}'''
        self._get_keyword()  # class 
        self.class_name = self._get_identifier()   # class_name 
        self._get_symbol()  # {
            
        # variable declaration, 
        if self.tokenizer.key_word() in ['static', 'field']:
            self.compile_class_var_dec()  # write happends in this call
        
        # Class' subroutines declarations:
        while (self.tokenizer.key_word() in ['constructor', 'function',
                                             'method', 'void']):
            self.compile_subroutine()  # this is the key part !
        
        self._get_symbol()  # get symbol } 
    
    def compile_class_var_dec(self):
        '''variables does not need allocate memeory before the construction, 
        therefore at this stage we do not need to write any vm code. 
        However, we do need to collect those variables'''
        # there might be multiple lines of variable declaration 
        while (self._match_keyword('static') or self._match_keyword('field')):
      
            var_kind = self._get_keyword()  # 'static' or 'field'
            var_type = self._get_type()
            var_name = self._get_identifier()
            
            # symbol table collect the entry 
            self._define_var(var_name, var_type, var_kind)
            # multivarialbe like: static int x, y;
            while self.tokenizer.symbol() == ',':
                self._get_symbol()
                var_name = self._get_identifier()
                self._define_var(var_name, var_type, var_kind)
                
            self._get_symbol()  # ';'
            
    def compile_subroutine(self):
        self.symbol_table.start_subroutine()  # clear the subroutine table 
        
        subroutine_type = self._get_keyword()   # function/constructor/method 
        return_type = self._get_type()
        subroutine_name = self._get_identifier()
        
        # A method will receive a pointer as the first argument,
		# we reserve index 0 for it.
        if subroutine_type == 'method':
            self._define_var('this_ptr', 'int', 'arg')  # construct symbol table 
            
        self.compile_parameters()
        
        self._get_symbol()  # '{'
        
        # local variables 
        local_vars = 0 
        if self.tokenizer.key_word() == 'var':
            local_vars = self.compile_var_dec()  # it has a while loop 
            
        call_name = self.class_name + '.' + subroutine_name
        
        self.vm.write_function(call_name, local_vars)  # call the function 
        
        if subroutine_type == 'method':
            # it generates code that associates the 'this' memorzy segment
            # with the object on which method was called to operate
            # Argument 0 of a constructor is the this pointer.
			# The first thing the function does is move it to the pointer register.
            self.vm.write_push('argument', 0)
            self.vm.write_pop('pointer', 0)  # THIS = argument 0 
        elif subroutine_type == 'constructor':
            # constructor: allocate new type 
            self.vm.write_alloc(self.symbol_table.var_count('field'))
            # write_alloc will return a base address !!! 
            # Then we set the this pointer to the assigned space.
            self.vm.write_pop('pointer', 0)  # anchors THIS at the base address
            
        if not self._match_symbols('}'):
            self.compile_statements()
            
        self._get_symbol()  # '}'
        
        # write return
        if return_type == 'void':
            self.vm.write_push('constant', 0)
        self.vm.write_return()  
        
    def compile_parameters(self):
        self._get_symbol()  # '('
        
        while self.tokenizer.symbol() != ')':  # a while loop 
            var_type = self._get_keyword()  # keyword type like 'static' 
            var_name = self._get_identifier()
            self._define_var(var_name, var_type, 'arg')  # arguments 
            if self.tokenizer.symbol() == ',':
                self._get_symbol()
                
        self._get_symbol()  # '('
        
    def compile_var_dec(self):
        var_dec = 0 
        while self._match_keyword('var'):
            self._get_keyword()  # var 
            var_type = self._get_type()
            var_name = self._get_identifier()
            # put them into the table 
            self._define_var(var_name, var_type, "local")
            var_dec += 1
            while self.tokenizer.symbol() == ',':
                self._get_symbol()  # ','
                var_name = self._get_identifier()
                self._define_var(var_name, var_type, 'local')
                var_dec += 1 
            self._get_symbol()  # ;
            
        return var_dec 
            
    def compile_statements(self):
        '''check the end of block }'''
        while not self._match_symbols('}'):
            if self.tokenizer.key_word() == 'let':
                self.compile_let()
            elif self.tokenizer.key_word() == 'if':
                self.compile_if()
            elif self.tokenizer.key_word() == 'while':
                self.compile_while()
            elif self.tokenizer.key_word() == 'do':
                self.compile_do()
            elif self.tokenizer.key_word() == 'return':
                self.compile_return()
        
    def compile_let(self):
        '''let varName = expression '''
        
        self._get_keyword()  # let 
        var_name = self._get_identifier()  # varName
        array = False 
        # handle array a[5] or a[5+3]
        if self.tokenizer.symbol() == '[':
            array = True   # let array[expression1] = expression2
            self._write_push_var(var_name)  # push array_idx 
            self._get_symbol()  #[
            self.compile_expression()  # expression 
            self._get_symbol()  # ] 
            self.vm.write_arithmetic('+')  # add: base address + expression 
            
        self._get_symbol()  # = 
        self.compile_expression()  # 
        
        if array:
            self.vm.write_pop('temp', 0)  # temp 0 = the value of expression2
            self.vm.write_pop('pointer', 1)  # 'THAT' stores the base+idx 
            self.vm.write_push('temp', 0)  
            self.vm.write_pop('that', 0)  # array[base+idx] = expression2
        else:
            self._write_pop_var(var_name)
            
        self._get_symbol()  # ; 
        
    def compile_if(self):
        self.if_idx += 1 
        
        self._get_keyword()  # if 
        self._get_symbol()  # (
        self.compile_expression()
        self._get_symbol()  # )
        
        self.vm.write_arithmetic('~')
        
        false_label = f"if_false_{self.if_idx}"
        true_label = f"if_true_{self.if_idx}"
        end_if_label = f"end_if_{self.if_idx}"
        self.vm.write_if(false_label)
        
        self._get_symbol()  # { 
        self.vm.write_label(true_label)
        
        self.compile_statements()
        
        self.vm.write_goto(end_if_label)
        
        self._get_symbol()  # }
        
        self.vm.write_label(false_label)
        
        if self._match_keyword('else'):
            self._get_keyword()  # else 
            self._get_symbol()
            self.compile_statements()
            self._get_symbol()
            
        self.vm.write_label(end_if_label)
    
    def compile_while(self):
        self.while_idx += 1 
        
        while_begin_label = f"while_{self.while_idx}"
        while_end_label = f"while_end_{self.while_idx}"
        
        self.vm.write_label(while_begin_label)
        
        self._get_keyword()  # 'while'
        
        self._get_symbol()  # '('
        self.compile_expression()  # expression
        self._get_symbol()  # ')'
        
        # While guard. Negating it and making a goto in case its false:
        self.vm.write_arithmetic('~')
        self.vm.write_if(while_end_label)
        
        self._get_symbol()  # '{'
        self.compile_statements()  # statments 
        self._get_symbol()  # '}'
        
        self.vm.write_goto(while_begin_label)
        
        self.vm.write_label(while_end_label)
        
    def compile_do(self):
        
        self._get_keyword()  # do 
        # either subroutineCall() or varName.methodCall()
        var_name = self._get_identifier()  # varName
        self._write_subroutine_call(var_name,return_void=True) 
        self._get_symbol()  # ; 
        
    def compile_return(self):
 
        self._get_keyword()
        if not self._match_symbols(';'):
            self.compile_expression()
        self._get_symbol()  # ; 
        
    def compile_expression(self):
        '''term (op term?)'''
        self.compile_term() 
        # check operator
        while self._is_operator():
            command = self._get_symbol()
            self.compile_term()
            self.vm.write_arithmetic(command)
    
    def compile_term(self):
        # integerConstant | stringConstant | keywordConstant |
        # # varName | varName '[' expression ']' | subroutineCall |
        # # '(' expression ')' | unaryOp term
        token_type = self.tokenizer.token_type()
        
        if self._is_keyword_constant():
            kw = self._get_keyword()
            if kw == 'false' or kw == 'null':
                # use 0 to represent false and null
                self.vm.write_push('constant', 0)
            elif kw == 'true':
                self.vm.write_push('constant', 0)
                self.vm.write_arithmetic('~')
            elif kw == 'this':
                self.vm.write_push('pointer', 0)
            
        elif token_type == 'integerConstant':
            self.vm.write_push('constant', self._get_integer())
            
        elif token_type == 'stringConstant':
            string_value = self._get_strings()
            self.vm.write_sring(string_value)
        elif token_type == 'identifier':  # var_name[] var_name() subrountine_call
            var_name = self._get_identifier()  # varname
            var_kind = self.symbol_table.kind_of(var_name)
            # push it into the stack 
            self._write_push_var(var_name)
            # lood ahead 
            # is it an array ?
            if self._match_symbols('['):
                self._get_symbol()
                self.compile_expression()
                self.vm.write_arithmetic('+')
                # rebase 'that' pointer to var+index
                self.vm.write_pop('pointer', 1)  # TAHT = var+index 
                self.vm.write_push('that', 0)  # push it to stack 
                self._get_symbol()
            # subroutine call like foo() or sqrt((x*y)+3)
            elif self._match_symbols('('):
                # in subroutine_call, it has a compile_expression_list 
                # which will get symbol ( and )
                self._write_subroutine_call(var_name)
            elif self._match_symbols('.'):  # method call foo.sqrt()
                self._write_subroutine_call(var_name)
        elif self._match_symbols('('):
            self._get_symbol()
            self.compile_expression()
            self._get_symbol()
        elif self._is_unary_operator():
            symbol = self._get_symbol()
            self.compile_term()
            if symbol == '-':
                symbol = 'neg'
            self.vm.write_arithmetic(symbol)
    
    def compile_expression_list(self):
        
        self._get_symbol()  # (
        num_of_expression = 0 
        
        while not self._match_symbols(')'):
            self.compile_expression()
            num_of_expression += 1
            if self._match_symbols(','):
                self._get_symbol()
                
        self._get_symbol()   # ) 
        
        return num_of_expression
        
        
    # --- private methods ---
    def _get_keyword(self):
        '''Tokinze keyword and advance'''
        keyword = self.tokenizer.key_word()
        self.tokenizer.advance()
        return keyword
        
    def _get_symbol(self):
        '''Tokenize symbol and advance()''' 
        symbol = self.tokenizer.symbol()
        self.tokenizer.advance()
        return symbol 
        
    def _get_identifier(self):
        identifer = self.tokenizer.identifier()
        self.tokenizer.advance()
        return identifer
        
    def _get_integer(self):
        int_val = self.tokenizer.int_val()
        self.tokenizer.advance()
        return int_val
        
    def _get_strings(self):
        string_val = self.tokenizer.string_val()
        self.tokenizer.advance()
        return string_val
        
    def _get_type(self):
        if self._is_primitive_type():
            return self._get_keyword()
        else:
            return self._get_identifier()
        
    def _is_symbol(self):
        return self.tokenizer.token_type() == 'symbol'
    
    def _is_key_word(self):
        return self.tokenizer.token_type() == 'keyword'
    
    def _is_operator(self):
        return (self._is_symbol() and self.tokenizer.symbol() in 
                ['+', '-', '*', '/', '&', '|', '<', '>', '='])
        
    def _is_keyword_constant(self):
        return (self._is_key_word() and self.tokenizer.key_word()
                in ['true', 'false', 'null', 'this'])
        
    def _is_unary_operator(self):
        return (self._is_symbol() and self.tokenizer.key_word()
                in ['-', '~'])
        
    def _is_primitive_type(self):
        return (self._is_key_word() and self.tokenizer.key_word() in 
                ['int', 'char', 'boolean', 'void'])
        
    def _match_symbols(self, symbol):
        return (self._is_symbol() and self.tokenizer.symbol() == symbol)
    
    def _match_keyword(self, keyword):
        return (self._is_key_word() and self.tokenizer.key_word() == keyword)
    
    
    def _define_var(self, name, var_type, kind):
        # if not in the table
        if self.symbol_table.kind_of(name) == 'NONE':
            self.symbol_table.define(name, var_type, kind)
            
    def _write_push_var(self, var_name):
        var_kind = self.symbol_table.kind_of(var_name)
        if var_kind == 'NONE':
            return
        var_index = self.symbol_table.index_of(var_name)
        if var_kind == 'field':
            self.vm.write_push('this', var_index)
        elif var_kind == 'static':
            self.vm.write_push('static', var_index)
        elif var_kind == 'local':
            self.vm.write_push('local', var_index)
        elif var_kind == 'arg':
            self.vm.write_push('argument', var_index)
            
    def _write_pop_var(self, var_name):
        var_kind = self.symbol_table.kind_of(var_name)
        if var_kind == 'NONE':
            return
        var_index = self.symbol_table.index_of(var_name)
        if var_kind == 'field':
            self.vm.write_pop('this', var_index)
        elif var_kind == 'static':
            self.vm.write_pop('static', var_index)
        elif var_kind == 'local':
            self.vm.write_pop('local', var_index)
        elif var_kind == 'arg':
            self.vm.write_pop('argument', var_index)
        
    def _write_subroutine_call(self, name, return_void=False):
        call_name = "" 
        method_name = "" 
        push_pointer = False 
        
        if self._match_symbols('.'):
            self._get_symbol()  # . 
            method_name = self._get_identifier()
            
        if method_name == "":
            # Implicit class, equivalent to "self.method()".
			# Appending the current/local class name to the function,
			# and pushing the "this" pointer.
            push_pointer = True 
            self.vm.write_push('pointer', 0)
            call_name = f"{self.class_name}.{name}"
        else:
            kind = self.symbol_table.kind_of(name)
            if kind == "NONE":  # name is a class and call it directly 
                call_name = f"{name}.{method_name}"
            else: 
                # like draw.circle()  draw is class type 
                class_type = self.symbol_table.type_of(name)
                call_name = f"{class_type}.{method_name}"
                push_pointer = True 
                self._write_push_var(name)
                
        num_of_parameters = self.compile_expression_list()
        
        if push_pointer:
            num_of_parameters += 1 
            
        self.vm.write_call(call_name, num_of_parameters)
        
        if return_void:
            self.vm.write_pop('temp', 0)