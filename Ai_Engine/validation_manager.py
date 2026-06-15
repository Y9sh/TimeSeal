import re

class ValidManager:
    def __init__(self):
        self.time = r'^\s*(\d{2}:\d{2})'
        
    def time_validate(self,content):
        return re.findall(self.time,content)
    
    def check_times(self,base_time,time_count):
        if time_count == base_time :
            return True
        else:
            return False
    
    def time_count(self,path):
        count = 0
        with open(path,'r') as read_con:
            for time in read_con:
                times = self.time_validate(time)
                if times != []:
                    count+=1
        return count
    
    def check_time_exist(self,count):
        if count == 0:
            return False
            