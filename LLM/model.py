# here where the local model called, core using LMStudio
import requests
import json

u_input = input("Enter:")
response = requests.post("http://localhost:1234/api/v1/chat",headers={
    "Authorization":f"Bearer sk-lm-pErwOJGp:JAiz0nfUXHU1rF2O4cTY",
    "Content-Type":"application/json"
},json ={
    "model":"liquid/lfm2-1.2b",
    "input":u_input
})
print(json.dumps(response.json()))
