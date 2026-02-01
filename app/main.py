from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from app.services.llm_service import get_llm_response

load_dotenv()

app = FastAPI(title = "AI Gateway", version = "0.1.0")

class ChatRequest(BaseModel):
    prompt: str
    model: str = "gpt-4o-mini"


# Endpoint
@app.post("/v1/chat")
async def chat(request: ChatRequest):
    """
    Accepts a prompt, talks to the LLM, and returns the response.
    """

    if not request.prompt:
        raise HTTPException(status_code = 400, detail = "Prompt is required.")
    response_text = await get_llm_response(request.prompt, request.model)
    return {"response": response_text, "model_used": request.model}

@app.get("/health")
async def health_check():
    return {"status": "ok"}