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

def advance(self):
    # get the next token from the input and make it the current token
    # advance in the level of TOKEN not CHAR !!! 
    if self._peek() == '"':
        self.current_token = self._pop_strings()
        print(self.current_token)
    elif self._peek(2) in ['//', '/*']:
        # skip the comments
        self._skip_comments()
    elif self._peek() == '\n':
        # skip the empty line
        self._pop()
    elif len(self._peek_word()) > 0:
        self.current_token = self._peek_word()
        self._pop(len(self._peek_word()))
        print(self.current_token)
    # elif self._peek() in self._symbols:
    #     self.current_token = self._pop()
    else:
        # space
        self._pop()
```
