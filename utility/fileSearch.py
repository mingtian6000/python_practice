import os
import re

def find_with_keyword(directory, keyword, excluded_dir=None):
    if excluded_dir is None:
        excluded_dir = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in excluded_dir]
        for file in files:
            if file.endswith('.java'): # search only java files
                with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if keyword in content:
                        print(f"Found in {file} in {root}")
                        ## loop all and exit
                    
                            
directory = 'C:/Users/lenovo/Desktop/abc'
keyword = 'kafka.store.config'

excluded_dir = ['target', 'build', '.git','test', 'TEST']
find_with_keyword(directory, keyword, excluded_dir)                      