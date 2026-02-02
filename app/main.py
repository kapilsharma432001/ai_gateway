import litellm
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from app.services.llm_service import get_llm_response
from app.schemas import ChatRequest

load_dotenv()

app = FastAPI(title = "AI Gateway", version = "0.1.0")

# Global exception handler
# This wrapper catches any error from from LiteLLM across the entire app
@app.exception_handler(litellm.APIConnectionError)
async def service_unavailable_handler(request: Request, exc: litellm.APIConnectionError):
    return JSONResponse(
        status_code = 503,
        content = {"error": "LLM Provider is unavailable. Please try again later."}
    )

# if user is sending too many requests, we catch that here
@app.exception_handler(litellm.RateLimitError)
async def rate_limit_handler(request: Request, exc: litellm.RateLimitError):
    return JSONResponse(
        status_code = 429,
        content = {"error": "LLM Proider rate limit exceeded", "detail": "we are sending too many requests to OpenAI"}
    )

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