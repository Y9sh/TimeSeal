from PySide6.QtCore import QDate
from pathlib import Path
import datefinder
import os
import json
import tempfile
from platformdirs import user_data_dir
from core.debugging import print_line
from core.git_man import GitManager 


class FileManager(GitManager):
    
    def __init__(self):
        super().__init__() 
        self.APP_NAME = 'TimeSeal'
        self.today_sessions = Path(f"{QDate.currentDate().toString("yyyy-MM-dd")}.md")
        self.directory_notes= os.path.dirname(self.today_sessions)
        self.current_file_date = QDate.currentDate().toString("yyyy-MM-dd")
        self.seal_today = ""
        self.seal_old = []
    
    def get_date(self,path):
        date_file = list(datefinder.find_dates(path))[0].date()
        return date_file
    
    def create_vaults(self):
        try:
            app_dir = Path(user_data_dir(self.APP_NAME))
            app_dir.mkdir(parents=True, exist_ok=True)
            notes_dir = app_dir / "notes_vault"
            notes_dir.mkdir(exist_ok= True)
            self.metadata_dir = app_dir / "metadata"
            self.metadata_dir.mkdir(exist_ok=True)
            self.metadata_today = Path(f"{self.metadata_dir}/{self.current_file_date}.json")
            self.notes_vault= notes_dir
            self.today_sessions = Path(f"{notes_dir}/{self.current_file_date}.md")
            print_line(self.today_sessions)
        except:
            print("Error")
        
    def check_metadata(self,path):
        date = self.get_date(path)
        print_line(Path(f"{self.metadata_dir}/{date}.json"))
        if os.path.exists(Path(f"{self.metadata_dir}/{date}.json")):
            print("Exists")
            return True
        else:
            print("Generated metadata")
            return False       
            
    def check_git(self):
        if not os.path.exists(f"{self.notes_vault}/.git"):
            
            self.git_init('init',self.notes_vault)
            self.git_add(str(self.notes_vault),self.notes_vault)
            self.git_commit('-m','Genesis Seal',self.notes_vault)
            print("Here create 1st snapshot for the notes")
        else:
            print_line(self.notes_vault)
            print_line(self.today_sessions)
            print("Already existed")
    
    def parse_git_status(self):
        output = self.git_status("--porcelain",self.notes_vault)
        for s in output.splitlines():
            if s.startswith(' '):
                if 'M' in s:
                    if self.current_file_date in s:
                        print("Current Sessions but Modified",s)
                        self.seal_today = self.get_date(s)
                    else:
                        print_line(s,"CHECK")
                        self.seal_old.append(f'{self.get_date(s)}')
                else:
                    print("No changes")
            else:
                if '?' in s:
                    print("Current Sessions",s)
                    self.seal_today = self.get_date(s)
        
    def commit(self):
        self.parse_git_status()
        print_line(self.notes_vault)
        print_line(self.seal_old)
        print_line(self.seal_today)
        self.git_add(str(self.notes_vault),self.notes_vault)
        self.git_commit('-m',f'Seal Timeline: {self.seal_today}\nReflections: {self.seal_old}',self.notes_vault)
        print("Commit-Successful")
                  
    def check_existed(self,tdy_session):
        if not os.path.exists(tdy_session):
            return 'NO'
        else:
            return 'YES'
        
    def save_decisions(self,current_pth,tdy_session):
        print_line(current_pth)
        if str(current_pth) in str(tdy_session):
            return self.today_sessions
        else:
            return current_pth
        
    def where_to_save(self,text,action,current_pth):
        path = self.save_decisions(current_pth,self.today_sessions)
        print_line(path)
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
            
    def write_prompt(self,path,text):
        with open(path,'w') as wr:
            wr.write(text)
        
    def read_file_silently(self,path):
        with open(path, 'r') as r_file:
            return r_file.read()
        
    def write_json(self,path,contents,action):
        with open(path,action, encoding='utf-8') as w_json:
            json.dump(contents,w_json,indent=4,sort_keys=True)
            
    def read_json(self,path,action):
        with open(path,action,encoding='utf-8') as r_json:
            return json.load(r_json)
