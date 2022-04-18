## Project 8: Virtual Machine II 

### Directory Structure

```
Nand2Tetris
├── projects
│    ├── 08
│    │   ├── VMTranslator.py
│    │   ├── FunctionCalls
│    │   │     ├──FibonacciElement
│    │   │     ├── --- 
│    │   └── ProgramFlow
│    │         ├──BasicLoop
│    │         ├── ---
|    .
└── tools
```

### Prompt Command call

At projects/08/ directory: 

```bash
# prompt> call simple function -b: booting (default = 'no') -s: simple function (default = 'no')
# user@macbook 08$
python VMTranslator.py ./FunctionCalls/SimpleFunction/SimpleFunction.vm -b no -s yes

# prompt> call function with booting 
# user@macbook 08$
python VMTranslator.py ./FunctionCalls/NestedCall/ -b no -s no   

# prompt> call function with booting 
# user@macbook 08$
python VMTranslator.py ./FunctionCalls/FibonacciElement/ -b yes -s no  

# prompt> call function with booting 
# user@macbook 08$
python VMTranslator.py ./FunctionCalls/StaticsTest/ -b yes -s no    
```
