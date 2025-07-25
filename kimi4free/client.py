import requests
import random
import time
import json

class KimiClient:
    def __init__(self):
        self.device_id = str(int(time.time() * 1000)) + str(random.randint(100000000, 999999999))
        self.session_id = str(int(time.time() * 1000)) + str(random.randint(100000000, 999999999))
        self.auth_token = None
        
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "origin": "https://www.kimi.com",
            "referer": "https://www.kimi.com/",
            "r-timezone": "Europe/Paris",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "x-language": "zh-CN",
            "x-msh-device-id": self.device_id,
            "x-msh-platform": "web",
            "x-msh-session-id": self.session_id,
            "x-traffic-id": self.device_id
        }
    
    def authenticate(self):
        response = requests.post("https://www.kimi.com/api/device/register", json={}, headers=self.headers)
        self.auth_token = response.cookies.get("kimi-auth")
        return self.auth_token
    
    def create_chat(self):
        if not self.auth_token:
            self.authenticate()
            
        headers = {
            **self.headers,
            "authorization": f"Bearer {self.auth_token}",
            "cookie": f"kimi-auth={self.auth_token}"
        }
        
        payload = {
            "born_from": "home",
            "is_example": False,
            "kimiplus_id": "kimi",
            "name": "未命名会话",
            "source": "web",
            "tags": []
        }
        
        response = requests.post("https://www.kimi.com/api/chat", json=payload, headers=headers)
        return response.json()["id"]
    
    def send_message(self, chat_id, message, stream=False, model="k2", use_search=True, 
                     use_deep_research=True, use_semantic_memory=False, kimiplus_id="kimi"):
        if refs is None:
            refs = []

        if scene_labels is None:
            scene_labels = []
            
        headers = {
            **self.headers,
            "authorization": f"Bearer {self.auth_token}",
            "cookie": f"kimi-auth={self.auth_token}",
            "accept": "text/event-stream"
        }
        
        payload = {
            "kimiplus_id": kimiplus_id,
            "extend": {"sidebar": True},
            "model": model,
            "use_search": use_search,
            "messages": [{"role": "user", "content": message}],
            "refs": [],
            "scene_labels": [],
            "use_semantic_memory": use_semantic_memory,
            "use_deep_research": use_deep_research
        }
        
        response = requests.post(
            f"https://www.kimi.com/api/chat/{chat_id}/completion/stream",
            json=payload,
            headers=headers,
            stream=True
        )
        
        full_response = ""
        for line in response.iter_lines(decode_unicode=True):
            if line and line.startswith("data: "):
                try:
                    data = json.loads(line[6:])
                    if data.get("event") == "cmpl":
                        text = data.get("text", "")
                        if text:
                            full_response += text
                            if stream:
                                print(text, end="", flush=True)
                except:
                    continue
        
        return full_response
    
    def chat(self, message, stream=False, **kwargs):
        chat_id = self.create_chat()
        return self.send_message(chat_id, message, stream, **kwargs)
