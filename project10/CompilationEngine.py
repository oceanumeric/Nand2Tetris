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
import sys
import os 


class CompilationEngine:
    
    def __init__(self, file_path):
        self.tokenizer = JackTokenizer(file_path) 
        if self.tokenizer.has_more_tokens():  # initialize the first move
            self.tokenizer.advance()
        self.indent_level = 0 
        jack_idx = file_path.find('.jack')
        xml_file = file_path[:jack_idx] + '.xml'
        self.xml = open(xml_file, 'w')
        self.compile_class()
        self.xml.close()
        
    def compile_class(self):
        self._start_with('class')
        
        self._write_keyword()  # class 
        self._write_identifier()  
        self._write_symbol()  # {
            
        # variable declaration
        if self.tokenizer.key_word() in ['static', 'field']:
            self.compile_class_var_dec()
        
        # Class' subroutines declarations:
        while (self.tokenizer.key_word() in ['constructor', 'function',
                                             'method', 'void']):
            self.compile_subroutine_dec()
        
        self._write_symbol()  # '}'
        
        self._end_with('class')
        
    def compile_class_var_dec(self):
        # there might be multiple lines of variable declaration 
        while (self._match_keyword('static') or self._match_keyword('field')):
            self._start_with('classVarDec')
            
            self._write_identifier()
            self._write_type()
            self._write_identifier()
            # multivarialbe like: static int x, y;
            while self.tokenizer.symbol() == ',':
                self._write_symbol()
                self._write_identifier()
            self._write_symbol()  # ';'
            
            self._end_with('classVarDec')
            
    def compile_subroutine_dec(self):
        self._start_with('subroutineDec')
        
        self._write_keyword()
        self._write_type()
        self._write_identifier()
        self.compile_parameters()
        
        self._start_with('subroutineBody')
        self._write_symbol()  # '{'
        
        if self.tokenizer.key_word() == 'var':
            self.compile_var_dec()  # it has a while loop 
            
        if not self._match_symbols('}'):
            self.compile_statements()
            
        self._write_symbol()  # '}'
        
        self._end_with('subroutineBody')
        
        self._end_with('subroutineDec')
        
    def compile_parameters(self):
        self._write_symbol()  # '('
        self._start_with('parameterList')
        
        while self.tokenizer.symbol() != ')':
            self._write_type()
            self._write_identifier()
            if self.tokenizer.symbol() == ',':
                self._write_symbol()
                
        self._end_with('parameterList')
        self._write_symbol()  # '('
        
    def compile_var_dec(self):
        while self._match_keyword('var'):
            self._start_with('varDec')
            
            self._write_keyword()
            self._write_type()
            self._write_identifier()
            while self.tokenizer.symbol() == ',':
                self._write_symbol()  # ','
                self._write_identifier()
            self._write_symbol()
            
            self._end_with('varDec')
            
    def compile_statements(self):
        '''check the end of block }'''
        self._start_with('statements')
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
        self._end_with('statements')
        
    def compile_let(self):
        '''let varName = expression '''
        self._start_with("letStatement")
        
        self._write_keyword()  # let
        
        self._write_identifier()  # varName
        
        # handle array a[5] or a[5+3]
        if self.tokenizer.symbol() == '[':
            self._write_symbol()  # '['
            self.compile_expression()
            self._write_symbol()  # ']'
            
        self._write_symbol()  # = 
        
        self.compile_expression()  # 
        self._write_symbol()  # ';'
        self._end_with('letStatement')   
        
    def compile_if(self):
        self._start_with('ifStatement')
        
        self._write_keyword()
        self._write_symbol()
        self.compile_expression()
        self._write_symbol()
        self._write_symbol()
        self.compile_statements()
        
        if self._match_symbols('else'):
            self._write_keyword()
            self._write_symbol()
            self.compile_statements()
            self._write_symbol()
            
        self._end_with('ifStatement')
    
    def compile_while(self):
        self._start_with("whileStatement")
        
        self._write_keyword()  # 'while'
        
        self._write_symbol()  # '('
        self.compile_expression()  # expression
        self._write_symbol()  # ')'
        
        self._write_symbol()  # '{'
        self.compile_statements()  # statments 
        self._write_symbol()  # '}'
        
        self._end_with('whileStatement')
        
    def compile_do(self):
        self._start_with('doStatement')
        
        self._write_keyword()  # do 
        # either subroutineCall() or varName.methodCall()
        self._write_identifier()  # varName
        if self._match_symbols('.'):
            self._write_symbol()  #.
            self._write_identifier()
        self._write_symbol()  # (
        self.compile_expression_list()
        self._write_symbol()  # ) 
        
        self._write_symbol()  # ';'
        
        self._end_with('doStatement')  
        
    def compile_return(self):
        self._start_with('returnStatement')
        
        self._write_keyword()
        if not self._match_symbols(';'):
            self.compile_expression()
        self._write_symbol()
        
        self._end_with('returnStatement')
            
        
    def compile_expression(self):
        '''term (op term?)'''
        self._start_with('expression')
        
        self.compile_term() 
        
        # check operator
        while self._is_operator():
            self._write_symbol()
            self.compile_term()
        
        self._end_with('expression')
        
    def compile_term(self):
        # integerConstant | stringConstant | keywordConstant |
        # # varName | varName '[' expression ']' | subroutineCall |
        # # '(' expression ')' | unaryOp term
        self._start_with('term')
        
        token_type = self.tokenizer.token_type()
        
        if self._is_keyword_constant():
            self._write_keyword()
            
        elif token_type == 'integerConstant':
            self._write_integer()
            
        elif token_type == 'stringConstant':
            self._write_strings()
        elif token_type == 'identifier':  # var_name[] var_name() subrountine_call
            self._write_identifier()  # varname
            # lood ahead 
            # is it an array ?
            if self._match_symbols('['):
                self._write_symbol()
                self.compile_expression()
                self._write_symbol()
            # subroutine call like foo() or sqrt((x*y)+3)
            elif self._match_symbols('('):
                self._write_symbol()
                self.compile_expression_list()  # can be empty
                self._write_symbol()
            elif self._match_symbols('.'):  # method call foo.sqrt()
                self._write_symbol()
                self._write_identifier()
                self._write_symbol()  # '('
                self.compile_expression_list()  # can be empty 
                self._write_symbol()  # ')'
        elif self._match_symbols('('):
            self._write_symbol()
            self.compile_expression()
        elif self._is_unary_operator():
            self._write_symbol()
            self.compile_term()
            
        self._end_with('term')
                
    
    def compile_expression_list(self):
        self._start_with('expressionList')
        
        while not self._match_symbols(')'):
            self.compile_expression()
            if self._match_symbols(','):
                self._write_symbol()
                
        self._end_with('expressionList')
        
        
    # --- private methods ---
    def _start_with(self, section):
        self._write_line('<' + section + '>')
        self._inc_indent()
        
    def _end_with(self, section):
        self._dec_indent()
        self._write_line("</" + section + ">")
        
    def _write_line(self, line):
        '''Utility function to write a line in xml'''
        space = ' ' * 2 * self.indent_level
        self.xml.write(space + line + '\n')
        
    def _inc_indent(self):
        '''Increase the indent'''
        self.indent_level += 1 
        
    def _dec_indent(self):
        '''Decrease the indent'''
        if self.indent_level > 0:
            self.indent_level -= 1 
        
    def _write_keyword(self):
        '''Tokinze keyword and write'''
        self._write_line("<keyword> " + self.tokenizer.key_word()+
                         " </keyword>")
        self.tokenizer.advance()
        
    def _write_symbol(self):
        '''Tokenize symbol and write and advance()'''
        self._write_line("<symbol> " + self.tokenizer.symbol()+
                         " </symbol>")
        self.tokenizer.advance()
        
    def _write_identifier(self):
        self._write_line("<identifier> " + self.tokenizer.identifier() +
                         " </identifier>")
        self.tokenizer.advance()
        
    def _write_integer(self):
        self._write_line("<integerConstant> " + str(self.tokenizer.int_val()) +
                         " </integerConstant>")
        self.tokenizer.advance()
        
    def _write_strings(self):
        self._write_line("<stringConstant> " + self.tokenizer.string_val() +
                         " </stringConstant>")
        self.tokenizer.advance()
        
    def _write_type(self):
        if self._is_primitive_type():
            self._write_keyword()
        else:
            self._write_identifier()
        
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
        
        
def main():
    if len(sys.argv) < 2:
        print("ERROR: Missing argument [file_path]")
        return -1
    
    file_path = sys.argv[1]
       
    if '.jack' in file_path:
        # if a single jack file
        ce = CompilationEngine(file_path)
    else:
        # a folder 
        for file_name in os.listdir(file_path):
            if '.jack' in file_name:
                # call JackTokenizer 
                file = file_path+file_name
                ce = CompilationEngine(file)
                
                
if __name__ == "__main__":
    main()
