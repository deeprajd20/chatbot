import os
from dotenv import load_dotenv
load_dotenv()
from uuid import uuid4
from src.utils import get_time
from groq import Groq
os.makedirs('session_chats')

API_KEY = os.getenv("API_KEY")



def usermessage(message,role = "user"):
    return {}

class ElementAI():

    def __init__(self,existing_session_id=None):
        self.api_key = API_KEY
        self.existing_session_id = existing_session_id

        self.client = Groq(api_key = self.api_key)
        if self.existing_session_id:
            pass
        else:
            self.chat_history = [{
                            "role": "system",
                            "content": "You are a helpful and concise AI assistant."
                        }]
        self.session_id = uuid4()

    def get_response(self,query):
        self.chat_history.append({
                        "role":"user",
                        "content":f"{query}"
                    })
        response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=self.chat_history
            )
        
        return response.choices[0].message.content
    
    def cleanup_session(self):
        import json
        with open(f"session_chats/{self.session_id}.json", "w", encoding="utf-8") as f:
            json.dump(self.chat_history, f, indent=4, ensure_ascii=False)
        print(f'\n To Restore this conversation use session ID : {self.session_id}')
            
    