from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from src.config_llm import ElementAI


app = FastAPI()

templates = Jinja2Templates(directory="src/templates")

a = ElementAI()


class InputChatMessage(BaseModel):
    message: str


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/chat")
async def chat(data: InputChatMessage):

    response = await a.get_response(data.message)

    return {
        "response": response
    }