import requests
import random
import time
import json

class KimiClient:
    def __init__(self, debug=False):
        self.device_id = str(int(time.time() * 1000)) + str(random.randint(100000000, 999999999))
        self.session_id = str(int(time.time() * 1000)) + str(random.randint(100000000, 999999999))
        self.auth_token = None
        self.debug = debug

        self.headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "origin": "https://www.kimi.com",
            "referer": "https://www.kimi.com/",
            "r-timezone": "Europe/Paris",
            "user-agent": self.session_id,
            "x-language": "zh-CN",
            "x-msh-device-id": self.device_id,
            "x-msh-platform": "web",
            "x-msh-session-id": self.session_id,
            "x-traffic-id": self.device_id
        }
        if self.debug:
            print(f"[DEBUG] Initialized KimiClient with device_id={self.device_id} and session_id={self.session_id}")

    def authenticate(self):
        if self.debug:
            print("[DEBUG] Authenticating...")

        response = requests.post("https://www.kimi.com/api/device/register", json={}, headers=self.headers)
        
        if self.debug:
            print(f"[DEBUG] Auth response status: {response.status_code}")
            print(f"[DEBUG] Response cookies: {response.cookies}")

        if response.status_code != 200:
            raise Exception(f"Authentication failed: {response.text}")

        self.auth_token = response.cookies.get("kimi-auth")

        if self.debug:
            print(f"[DEBUG] Retrieved auth_token: {self.auth_token}")

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

        if self.debug:
            print(f"[DEBUG] Creating chat with payload: {json.dumps(payload)}")

        response = requests.post("https://www.kimi.com/api/chat", json=payload, headers=headers)

        if self.debug:
            print(f"[DEBUG] Create chat status: {response.status_code}")
            print(f"[DEBUG] Chat creation response: {response.text}")

        if response.status_code != 200:
            raise Exception(f"Create chat failed: {response.text}")

        return response.json()["id"]

    def send_message(self, chat_id, message, stream=False, model="k2", use_search=True,
                     use_deep_research=True, use_semantic_memory=False, kimiplus_id="kimi"):

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
            "history": [],
            "scene_labels": [],
            "use_semantic_memory": use_semantic_memory,
            "use_deep_research": use_deep_research
        }

        if self.debug:
            print(f"[DEBUG] Sending message to chat_id={chat_id}")
            print(f"[DEBUG] Payload: {json.dumps(payload)}")

        try:
            response = requests.post(
                f"https://www.kimi.com/api/chat/{chat_id}/completion/stream",
                json=payload,
                headers=headers,
                stream=True
            )

            if self.debug:
                print(f"[DEBUG] Send message response status: {response.status_code}")

            full_response = ""
            for line in response.iter_lines(decode_unicode=True):
                if line and line.startswith("data: "):
                    try:
                        data = json.loads(line[6:])
                        if self.debug:
                            print(f"[DEBUG] SSE data: {data}")
                        if data.get("event") == "cmpl":
                            text = data.get("text", "")
                            if text:
                                full_response += text
                                if stream:
                                    print(text, end="", flush=True)
                    except Exception as e:
                        if self.debug:
                            print(f"[DEBUG] JSON decode error: {e}")
                        continue

            return full_response

        except Exception as e:
            print(f"[ERROR] Failed to send message: {e}")
            return ""

    def chat(self, message, stream=False, chat_id=None,
            model="k2", use_search=True, use_deep_research=True,
            use_semantic_memory=False, kimiplus_id="kimi"):
        
        if chat_id is None:
            chat_id = self.create_chat()
            if self.debug:
                print(f"[DEBUG] Created new chat_id: {chat_id}")
        
        return self.send_message(
            chat_id=chat_id,
            message=message,
            stream=stream,
            model=model,
            use_search=use_search,
            use_deep_research=use_deep_research,
            use_semantic_memory=use_semantic_memory,
            kimiplus_id=kimiplus_id
        )
