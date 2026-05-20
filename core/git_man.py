import subprocess

class GitManager():
    
    def __init__(self):
        self.cmd = subprocess.run
        
        
    def git_init(self,arg,working_dir):
        try:
            self.cmd(["git",arg],check=True,cwd=working_dir)
        except subprocess.CalledProcessError as err:
            print("wrong commands", type(err).__name__)
        
    def git_add(self,arg,working_dir):
        try:
            self.cmd(["git","add",arg],check=True,cwd=working_dir)
        except subprocess.CalledProcessError as err:
            print("wrong commands", type(err).__name__)
            
    
    def git_commit(self,arg1,comments,working_dir):
        try:
            self.cmd(["git","commit",arg1,comments],check=True,cwd=working_dir)
        except subprocess.CalledProcessError as err:
            print("wrong commands", type(err).__name__)
    
    
    def git_status(self,arg1,working_dir):
        try:
            output = self.cmd(["git","status",arg1],check=True,text=True,capture_output=True,cwd=working_dir).stdout
            return output
        except subprocess.CalledProcessError as err:
            print("wrong commands", type(err).__name__)
            
