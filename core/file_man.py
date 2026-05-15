from PySide6.QtCore import QDate
from pathlib import Path
import datefinder
import datetime

class FileManager():
    
    def __init__(self):
        super().__init__() 
        self.file_path_base = Path(f"./notes/{QDate.currentDate().toString("yyyy-MM-dd")}.md")
        self.current_file_date = QDate.currentDate().toString("yyyy-MM-dd")
        self.current_path = ""
    
    def get_date(self,path):
        date_file = list(datefinder.find_dates(path))[0].date()
        return date_file
        
    
    def check_for_existed_file(self,text):
        if self.file_path_base.exists():
            print("File already exists")
            if self.current_path == "":
                self.current_path = self.file_path_base
                self.write_file(self.current_path,text)
            elif self.current_path != "":
                print("This is the current path",self.current_path)
                self.write_file(self.current_path,text)
            else:
                print("Something wrong with the logic")
        else:
            print("Non-exist..need to create new file")
            self.write_file(self.file_path_base,text)
                            
    def read_file(self,path):
        with open(path, 'r') as rw_file:
            return rw_file.read()

    def write_file(self,file_path,text):
        with open(file_path,'w') as e_file:
            e_file.write(text)
    
    def read_file_silently(self):
        with open(self.file_path_base, 'r') as r_file:
            return r_file.read()