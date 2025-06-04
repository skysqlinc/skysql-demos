import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional
import uuid
import sys
import os
sys.path.append(os.path.dirname(__file__))
from db_chat_agent import db_chat_agent, list_db_agents

app = FastAPI()

# Allow CORS for all origins (for demo; restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store (for demo)
sessions: Dict[str, list] = {}

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str

class ChatResponse(BaseModel):
    session_id: str
    response: str
    sql: Optional[str] = None

@app.get("/agents")
def get_agents():
    return {"agents": list_db_agents()}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    # Session management
    session_id = req.session_id or str(uuid.uuid4())
    if session_id not in sessions:
        sessions[session_id] = []
    sessions[session_id].append({"user": req.message})
    # Call the agent
    agent_response = db_chat_agent.chat(req.message)
    # Extract string response and SQL if present
    if hasattr(agent_response, "response"):
        response_text = agent_response.response
        sql_text = getattr(agent_response, "sql", None)
    elif isinstance(agent_response, dict):
        response_text = agent_response.get("response") or str(agent_response)
        sql_text = agent_response.get("sql")
    else:
        # Try to parse SQL from string if formatted
        response_text = str(agent_response)
        sql_text = None
        if '```sql' in response_text:
            parts = response_text.split('```sql')
            if len(parts) > 1:
                sql_block = parts[1].split('```')[0].strip()
                sql_text = sql_block
    sessions[session_id].append({"agent": response_text, "sql": sql_text})
    return ChatResponse(session_id=session_id, response=response_text, sql=sql_text)

if __name__ == "__main__":
    uvicorn.run("db_chat_api:app", host="0.0.0.0", port=8000, reload=True) 