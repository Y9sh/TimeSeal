from core.file_man import FileManager
import json

class PromptManager(FileManager):
    def __init__(self):
        pass
        
    def get_prompt(self,path,contents,format):
        template = self.read_file_silently(path)
        content = self.read_file_silently(contents)
        formats = self.read_file_silently(format)
        return f'{template}{content}{formats}'
    
    # for debug
    def get_json(self,contents):
        return json.loads(self.read_file_silently(contents))