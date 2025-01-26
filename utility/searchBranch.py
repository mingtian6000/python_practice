# to search specific file among diff git branches
import os, subprocess

def get_release_branches():
    branches = []
    try:
        #branches = subprocess.check_output(['git', 'branch', '-r']).decode('utf-8').split('\n')
        result = subprocess.run(['git', 'branch', '--list','--all','--format=%(refname:short)',
                                   '*release*'], capture_output=True,check=True ,text=True)
        branches = result.stdout.strip().split('\n')
        for branch in branches:
            print(branch)
        return branches
    except Exception as e:
        print("Error: ", e)
    return branches


file_folder_path='C:/Users/lenovo/Desktop/abc'
keyword = 'kafka.store.config'

try:
    os.chdir(file_folder_path) 
    branches = get_release_branches() # get all release branches
    for branch in branches: # iterate over each branch
        try: 
            subprocess.check_output(['git', 'checkout', branch]) 
            result = subprocess.run(['git', 'ls-files', '--', '*.py'], capture_output=True, check=True, text=True)
            files = result.stdout.strip().split('\n')
            for file in files: 
                if keyword in file:
                    print(f"Found in {file} in branch {branch}")
        except Exception as e: 
            print(f"Error checking out branch {branch}: {e}")
    subprocess.check_output(['git', 'checkout', 'main'])  # switch back to main branch
except Exception as e: 
    print(f"Error changing directory to {file_folder_path}: {e}")
    
    