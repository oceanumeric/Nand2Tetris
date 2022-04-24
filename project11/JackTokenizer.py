# JackTokenizer 
# based on the code by https://github.com/santigl
# improved in several ways:
# fixed bug for string like do Output.printString("THE // AVERAGE IS: "); 
# write the xml token files
# detecting white space like empty line, ' ', '\n', and '\t' is challenging 
import sys
import os 


# TOKEN_TYPES = ["KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"]

TOKEN_KEYWORDS = ["CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT", \
					"BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", \
					"LET", "DO", "IF", "ELSE", "WHILE", "RETURN", "TRUE", \
					"FALSE", "NULL", "THIS"]

SYMBOLS = ['(', ')', '[', ']', '{', '}', ',', ';', '=', '.', '+', '-', '*', \
		 '/', '&', '|', '~', '<', '>']

WHITE_SPACE = [' ', '\n', '\t']


class JackTokenizer:
    """
    A JackTokenizer based on function open() open.tell(), open.read() open.seek()
    
    Main functions:
        public:
            constructor
            has_more_tokens()
            advance()
            token_type()
            destructor()
        private:
            _peek(num_char=1)  
                as Jack language is LL(1)
                we only need _peek(2) for parsing a term such as x+y-arr[5]
            _skip_line()
                to skip empty line ' ' or '\n' or '\t'
    """
    # class attributes 
    # _token_types = frozenset(TOKEN_TYPES)
    _keywords = frozenset(TOKEN_KEYWORDS)
    _symbols = frozenset(SYMBOLS)
    _white_space = frozenset(WHITE_SPACE)
    
    def __init__(self, file_name):
        # input file stream and token 
        self.file = open(file_name, 'r')
        self.current_token = ""  # current token = None 
  
    def __del__(self):
        # destructor 
        self.file.close()
        
    def has_more_tokens(self):
        # ignore comments and white space 
        while self._peek() != "":
            # Skipping spaces and newlines:
            while self._peek() in self._white_space:
                self._pop()
                if self._peek() == "":
                    return False
            if self._peek() == '"':
                # it is token 
                return True
            else:
                # skip comments 
                cs = self._peek(2)
                while cs in ['//', '/*']:
                    self._skip_comments()
                    cs = self._peek(2)
            if self._peek() not in self._white_space:
                # must have some token 
                return True
            
        return False
            
    def advance(self):
        if self.has_more_tokens():
            if self._peek() != '"':
                self.current_token = self._peek_word()
                self._pop(len(self.current_token))
            else:
                self.current_token = self._pop_strings()
        
    def token_type(self):
        # need to be updated later: iterator is not on the same level with
        # has_more_tokens() and advance()
        token = self.current_token
        if token.upper() in self._keywords:
            return "keyword"
        if token in self._symbols:
            return "symbol"
        if '"' in token:
            return "stringConstant"
        if token.isdigit():
            return "integerConstant" 
        
        return "identifier"
    
    def key_word(self):
        '''To be called only if type is keyword'''
        return self.current_token
    
    def symbol(self):
        '''To be called only if type is symbol'''
        return self.current_token
    
    def identifier(self):
        return self.current_token
    
    def int_val(self):
        return int(self.current_token)
    
    def string_val(self):
        return self.current_token.replace('"', '')
    
    # -- private method --    
    def _peek(self, num_char=1):
        current_pos = self.file.tell()  # current position
        char = self.file.read(num_char)  # read num_char 
        self.file.seek(current_pos)
        return char 
    
    def _pop(self, num_char=1):
        # pop out num_char
        return self.file.read(num_char)
    
    def _peek_word(self):
        '''Read all chars until white space or a symbol'''
        word = ""
        current_pos = self.file.tell()
        current_char = self._pop()
        
        if current_char in self._symbols:
            word = current_char
        else:
            while (current_char != "") and (current_char not in self._white_space):
                word += current_char
                current_char = self._pop()  # update current_char 
                if current_char in self._symbols:
                    break 
                
        self.file.seek(current_pos)
        
        return word
    
    def _pop_strings(self):
        # to be called after self._peek() == '"'
        string_const = ""
        current_char = self._pop()  # current char = "
        string_const += current_char  # 
        while self._peek() != '"':
            string_const += self._pop()  # string_const = "++++
        string_const += self._pop()  # string_const = "++++"
        return string_const
    
    def _skip_comments(self):
        # to be called after self._peek(2) == '//' pr "/*"
        # it must be comment as it is only called after if .. in symbols
        if self._peek(2) == '//':
            self.file.readline()
        if self._peek(2) == '/*':
            self._pop(2)  # pop /*
            while self._peek(2) != '*/':
                self._pop()
            self._pop(2)  # pop */ 