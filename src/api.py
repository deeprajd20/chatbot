from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import json
from src.config_llm import ElementAI
from src.config import SESSION_CHATS_DIR, TEMPLATES_DIR


app = FastAPI()

templates = Jinja2Templates(directory=TEMPLATES_DIR)



class InputChatMessage(BaseModel):
    message: str
    session_id: str | None = None


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/chat")
async def chat(data: InputChatMessage):

    a = ElementAI(
        existing_session_id=data.session_id
    )

    response = await a.get_response(data.message)
    a.cleanup_session()

    return {"response": response}


@app.get("/sessions")
async def get_sessions_list():

    sessions = []

    for file in SESSION_CHATS_DIR.glob("*.json"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                messages = json.load(f)

            first_user_message = next(
                (
                    message["content"]
                    for message in messages
                    if message.get("role") == "user"
                ),
                "New Chat",
            )

            title = first_user_message.strip()

            if len(title) > 35:
                title = title[:35] + "..."

            sessions.append({"session_id": file.stem, "title": title})

        except Exception as e:
            print(f"Could not read {file}: {e}")

    sessions.sort(
        key=lambda x: (SESSION_CHATS_DIR / f"{x['session_id']}.json").stat().st_mtime,
        reverse=True,
    )

    return {"sessions": sessions}


@app.get("/sessions/{session_id}")
async def get_session(session_id):
    session_file = SESSION_CHATS_DIR / f"{session_id}.json"
    if not session_file.exists():
        raise HTTPException(404, "Session File Not found")

    try:
        with open(session_file, "r", encoding="utf-8") as f:
            messages = json.load(f)

        return {"session_id": session_id, "messages": messages}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
