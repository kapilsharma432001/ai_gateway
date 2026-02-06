import litellm
import logging
import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from app.services.llm_service import get_llm_response
from app.schemas import ChatRequest


# Configure a simple logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai_gateway")

# load_dotenv()

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

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    This function intercepts all incoming request.
    1. Log start time.
    2. Process request.
    3. Calculate duration.
    4. Log the result.
    """
    start_time = time.time()

    # "call_next" passes the request to your chat endpoint
    response = await call_next(request)
    process_time = (time.time()- start_time) * 1000 # convert to milliseconds
    formatted_process_time = '{0:.2f}'.format(process_time)

    # Log the result
    logger.info(
        f"Path: {request.url.path}"
        f" | Method: {request.method}"
        f" | Status Code: {response.status_code}"
        f" | Process Time: {formatted_process_time} ms"
    )
    # Add a custom header so the client sees how long it took
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Endpoint
@app.post("/v1/chat")
async def chat(request: ChatRequest):
    """
    Accepts a prompt, talks to the LLM, and returns the response.
    """
    try:
        if not request.prompt:
            raise HTTPException(status_code = 400, detail = "Prompt is required.")
        response_text = await get_llm_response(request.prompt, request.model)
        return {"response": response_text["content"], 
                "usage": response_text["usage"],
                "model_used": request.model
                }
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok"}