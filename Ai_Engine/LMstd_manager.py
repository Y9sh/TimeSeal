from core.cli import CLI
import subprocess

class LManager(CLI):
    
    def __init__(self):
        super().__init__()
        self.list_model = []
        self.loaded_model = []

        
    def model_parser(self,json_text,outer,inner):
    # parsing model from choose_model output
    # outer and innner == str the value in dict
        if inner == 'key':
            for n in range(len(json_text[outer])):
                self.append_list_model(json_text[outer][n][inner])
        elif inner == 'loaded_instances':
            for n in range(len(json_text[outer])):
                self.get_loaded_models(json_text[outer][n][inner])
        else:
            print('Added additional needed here later..')
            
    def LM_server(self,action):
        # action = should be (start/stop)
        try:
            test = self.cmd(["lms","server",action], capture_output=True, text=True, check=True)
            return test.stderr
        except subprocess.CalledProcessError as err:
            print("wrong commands", type(err).__name__)
            
    def append_list_model(self,model):
        self.list_model.append(model)
    
    def get_loaded_models(self,loaded):
        if loaded != []:
            self.loaded_model.append(loaded[0]['id'])