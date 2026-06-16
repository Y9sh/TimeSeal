# here where the local model called, core using LMStudio
# api called
# using LLM to generate metadata and summary for old notes 
import requests
import json
import os
from dotenv import load_dotenv
from Ai_Engine.prompt_manager import PromptManager
from core.file_man import FileManager
load_dotenv()

class LocalModel(PromptManager):

    def __init__(self):
        self.api_key = os.getenv("LM_KEY")
        self.templates = 'Ai_Engine/prompts/prompt.md'
        self.formats = 'Ai_Engine/prompts/format.md'
        self.load = ''
        self.unload = ''
        
    def list_model(self):
        # list of downloaded model
        try:
            model = requests.get("http://localhost:1234/api/v1/models",headers={
            "Authorization":f"Bearer {self.api_key}"})
            #eturn(json.dumps(models.json()))
            return model.json()
        except Exception as e:
            print(e)
    
    def load_model(self):
        try:
            load = requests.post("http://localhost:1234/api/v1/models/load",headers={
            "Authorization":f"Bearer {self.api_key}",
            "Content-Type":"application/json"
            },json = {
                "model": self.load
            })
            self.unload = self.load
            print(self.unload)
            self.load = ''
        except Exception as e:
            print(e)
    
    def unload_model(self):
        if self.unload == '':
            self.unload = self.load
            
        try:
            unloads = requests.post(
                "http://localhost:1234/api/v1/models/unload",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={"instance_id": self.unload}
            )
        except Exception as e:
            print(e)
    
    
    def get_responses(self,content,model):
        file_man = FileManager()
        print("Model:",model)
        try:
            response = requests.post("http://localhost:1234/api/v1/chat",headers={
            "Authorization":f"Bearer {self.api_key}",
            "Content-Type":"application/json"
            },json ={
                # later in UI, will trigger which models will be used
                "model":model.strip(),
                "input":self.get_prompt(self.templates,content,self.formats),
                "store":False
                })
            file_man.write_json('Ai_Engine/logs/log.json',response.json(),'a')
            return response.json()['output'][0]['content']
            #return(json.dumps(response.json()))
        except Exception as e:
            print(e)

        