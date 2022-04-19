## Project 10: Compiler I - Syntax Analysis

```python
# Input: a stream of chars
# output: meaningful tokens: keyword, symbol, identifier, int_const, string_const

"""
Process: combine and classify
  * combine chars
  * classify those combinations into different groups 

How could we combine chars? What are criteria of combining chars:
  - "string_const", combine by peek(1) == "
  - symbols like (, combine by peek(1) in symbols
  - comments: combine by peek(2) in ['//', '/*'] 
  - keywords: space-[strings]-space/symbol 
  - identifier: space-[strings]-space
  - int_const: space-[strings]-space 
  
One could notice that keywords, identifier and int_const can be combined in the same way. Therefore we could construct the following code 
"""

### It is all about iterator

The iterator of `has_more_tokens()` has to run at the same speed with `advance()`

```python
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
```

### The Jack Grammar

#### Token types
There are five types of lexical elements in the Jack language:
 - keyword: ‘class’ | ‘constructor’ | ‘function’ | ‘method’ | ‘field’ | ‘static’ | ‘var’ | ‘int’ | ‘char’ | ‘boolean’ | ‘void’ | ‘true’ | ‘false’ | ‘null’ | ‘this’ | ‘let’ | ‘do’ | ‘if’ | ‘else’ | ‘while’ | ‘return’
 - symbol: ‘{‘ | ‘}’ | ‘(‘ | ‘)’ | ‘[‘ | ‘]’ | ‘,’ | ‘;’ | '+' | '-' | '*' | '/' | '&' | '|' | '>' | '<' | '=' | ‘~’ 
 - integerConstant: a decimal number in the range 0 .. 32767
 - stringConstant '"' sequence of ASCII characters not including double quote or newline '"' 
 - identifier: sequence of letters, digits, and underscore (“_”) not starting with a digit 

#### Program structure

A  program is a collection of classes, each appearing in a separate file. The compilation unit is a class, and is given by the following context free syntax:
 - class: 'class' className '{' classVarDec* subroutineDec* '}' 
 - classVarDec: ('static' | 'field' ) type varName (',' varName)* ';' 
 - type: 'int' | 'char' | 'boolean' | className 
 - subroutineDec: ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody
 - parameterList: ( (type varName) (',' type varName)*)?
 - subroutineBody: '{' varDec* statements '}' 
 - varDec: 'var' type varName (',' varName)* ';' 
 - className: identifier
 - subroutineName: identifier 
 - varName: identifier 

#### Statements structure

statements: statement* 
- statement: whileStatement | ifStatement | letStatement | returnStatement | doStatement
- whileStatement: 'while' '(' expression ')' '{' statements '}' 
- ifStatement: 'if' '(' expression ')' '{' statements '}' ( 'else' '{' statements '}' )?
- returnStatement 'return' expression? ';' 
- letStatement: 'let' varName ('[' expression ']')? '=' expression ';' 
- doStatement: 'do' subroutineCall ';' 

### Expressions

Expression: term (op term)* 
 - term: integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp term
 - subroutineCall: subroutineName '(' expressionList ')' | ( className | varName) '.' 
 - subroutineName '(' expressionList ')' 
 - expressionList: (expression (',' expression)* )?
 - op: '+' | '-' | '*' | '/' | '&' | '|' | '>' | '<' | '=' 
 - unaryOp: '-' | '~' 
 - keywordConstant: 'true' | 'false' | 'null' | 'this' 
