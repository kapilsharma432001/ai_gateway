from pydantic import BaseModel, Field, field_validator

class ChatRequest(BaseModel):
    prompt: str = Field(..., desccription = "The user's input prompt for the LLM.", 
                        min_length=1, max_length=5000) # max_length 5000 is a guardrail, that is there to prevent huge payloads
    model: str = Field("gpt-4o-mini", description = "The LLM model to use")
    temperature: float = Field(0.7, ge=0.0, le=2.0, description="Creativity level (0.0 to 2.0)")
    
    @field_validator('model')
    @classmethod
    def validate_model(cls, m: str):
        allowed_models = {"gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo", "gpt-4", "claude-3-opus", "gemini-pro"}
        if m not in allowed_models:
            raise ValueError(f"Model '{m}' is not supported. Choose from {allowed_models}.")
        return m