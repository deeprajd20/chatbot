import os
from dotenv import load_dotenv
load_dotenv()
from groq import Groq
API_KEY = os.getenv("API_KEY")


class ElementAI():

    def __init__(self):
        self.api_key = API_KEY
        self.client = Groq()

    def get_response(self,query):
        completion = self.client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
            {
                "role": "user",
                "content": f"{query}"
            }
            ],
            temperature=1,
            max_completion_tokens=2048,
            top_p=1,
            reasoning_effort="medium",
            stream=True,
            stop=None
        )
        return  completion 
    