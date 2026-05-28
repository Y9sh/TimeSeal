# here where the local model called, core using LMStudio
# using LLM to generate metadata for old notes 
import requests
import json
from core.file_manager import FileManager

class LocalModel(FileManager):

    def __init__(self):
        self.api_key = 'apikey'
        self.path = ''

    def get_prompts(self,state_prmpt):
        if state_prmpt == 'summary':
            self.path ="LLM/summary_prmpt.md" 
        else:
            self.path = "LLM/metadata__prmpt.md"
            
    def prompt_build_up(self):
        self.read_file_silently(self.path)
        
    def get_responses(self):
        response = requests.post("http://localhost:1234/api/v1/chat",headers={
        "Authorization":f"Bearer {self.api_key}",
        "Content-Type":"application/json"
        },json ={
        "model":"liquid/lfm2-1.2b",
        "input":self.prompt_build_up
        })
        return(json.dumps(response.json()))
