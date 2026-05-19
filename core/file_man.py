from PySide6.QtCore import QDate
from pathlib import Path
import datefinder
import os
import tempfile

class FileManager():
    
    def __init__(self):
        super().__init__() 
        self.today_sessions = Path(f"./notes/{QDate.currentDate().toString("yyyy-MM-dd")}.md")
        self.current_file_date = QDate.currentDate().toString("yyyy-MM-dd")
    
    def check_git(self):
        if not os.path.exists("notes/.git"):
            # logic to git
            print("Here create 1st snapshot for the notes")
        else:
            print("Already existed")
 
    def check_dir_notes(self):
        if not os.path.exists("notes/"):
            os.mkdir("notes/")
            print("Directory create")
        else:
            print("Directory existed")
            
    def check_existed(self,tdy_session):
        if not os.path.exists(tdy_session):
            return 'NO'
        else:
            return 'YES'
        
    def get_date(self,path):
        date_file = list(datefinder.find_dates(path))[0].date()
        return date_file
        
    def save_decisions(self,current_pth,tdy_session):
        if str(current_pth) in str(tdy_session):
            return self.today_sessions
        else:
            return current_pth
        
    def where_to_save(self,text,action,current_pth):
        path = self.save_decisions(current_pth,self.today_sessions)
        print("curr path:",path)
        if path == self.today_sessions:
            self.write_file(path,text,action)
        else:
            self.safety_old_write(path,text)
        

    
    def safety_old_write(self,file_path,text):
        dir_name = os.path.dirname(file_path)
    
        content = self.read_file(file_path)
        full_content = f"{content}\n# -- Reflection: {self.current_file_date} --{text}"
        
        with tempfile.NamedTemporaryFile(dir=dir_name,mode='w+t',delete=False) as temp:
            print("Using safety")
            temp.write(full_content)
            temp.flush()
            f_temp = temp.name
        # swap old file content with temp file
        os.replace(f_temp,file_path)
            
        
    def read_file(self,path):
        with open(path, 'r') as rw_file:
            return rw_file.read()

    def write_file(self,file_path,text,action):
        with open(file_path,action) as e_file:
            e_file.write(text)
    
    def read_file_silently(self,path):
        with open(path, 'r') as r_file:
            return r_file.read()
        