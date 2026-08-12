import os
from dotenv import load_dotenv

load_dotenv()
from uuid import uuid4
from src.utils import get_time
from groq import AsyncGroq
from src.config import SESSION_CHATS_DIR
import json

API_KEY = os.getenv("API_KEY")


class ElementAI:
    def __init__(self, existing_session_id=None):
        self.api_key = API_KEY
        self.existing_session_id = existing_session_id

        self.client = AsyncGroq(api_key=self.api_key)
        if self.existing_session_id:
            self.session_id = str(
                existing_session_id
            )
            with open(
                f"{SESSION_CHATS_DIR}/{self.session_id}.json",
                "r",
                encoding="utf-8",
            ) as f:
                messages_hist = json.load(f)
            self.chat_history = messages_hist

        else:
            self.session_id = str(
                uuid4()
            )
            self.chat_history = [
                {
                    "role": "system",
                    "content": "You are a helpful and concise AI assistant.",
                }
            ]
        

    async def get_response(self, query):
        self.chat_history.append({"role": "user", "content": f"{query}"})
        response = await self.client.chat.completions.create(
            model="llama-3.3-70b-versatile", messages=self.chat_history
        )
        content = response.choices[0].message.content
        self.chat_history.append({"role": "assistant", "content": f"{content}"})
        return content

    def cleanup_session(self):

        with open(
            f"{SESSION_CHATS_DIR}/{self.session_id}.json", "w", encoding="utf-8"
        ) as f:
            json.dump(self.chat_history, f, indent=4, ensure_ascii=False)
