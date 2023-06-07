from wudao.api_request import executeSSE, getToken, queryTaskResult
from random import randint
import time
import uuid

from typing import Union, List, Tuple, Optional, Dict

def randomTaskCode():
    return "%019d" % randint(0, 10**19)

class ChatGLMAPI:
    def __init__(self,api_key:str, public_key:str) -> None:
        self.api_key = api_key
        self.public_key = public_key
        self.ability_type = "chatGLM"
        self.engine_type = "chatGLM"
        self.temp_token = None

    def get_token_or_refresh(self):
        token_result = getToken(self.api_key, self.public_key)
        if token_result and token_result["code"] == 200:
            token = token_result["data"]
            self.temp_token = token
        else:
            raise Exception("Fail to get token from ChatGLMAPI. Check api_key/public_key")    
        return self.temp_token    
    
    def stream_chat(self,tokenizer,ins:str, his:List[Tuple[str,str]]=[],  
        max_length:int=4096, 
        top_p:float=0.7,
        temperature:float=0.9):  
        data = {
                    "top_p": top_p,
                    "temperature": temperature,                    
                    "risk": 0.15,                    
                    "requestTaskNo": randomTaskCode(),                                        
                    "prompt": ins,
                    "history": []                    
                }    
        token = self.temp_token if self.temp_token  else self.get_token_or_refresh()
        resp = executeSSE(self.ability_type, self.engine_type, token, data)                

        output_text = ""
        for event in resp.events():
            if event.data:
                output_text = event.data
            elif event.event == "error":
                token = self.get_token_or_refresh()
                break
                
        return [(output_text,"")]




