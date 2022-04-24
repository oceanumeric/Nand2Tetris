from CompilationEngine import CompilationEngine
import os 
import sys 


def main():
    if len(sys.argv) < 2:
        print("ERROR: Missing argument [file_path]")
        return -1
    
    file_path = sys.argv[1]
       
    if '.jack' in file_path:
        # if a single jack file
        CompilationEngine(file_path)  # compile 
    else:
        # a folder 
        for file_name in os.listdir(file_path):
            if '.jack' in file_name:
                # call JackTokenizer 
                file = file_path+file_name
                CompilationEngine(file)
                
                
if __name__ == "__main__":
    main()