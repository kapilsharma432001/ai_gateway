from litellm import acompletion
from app.config import settings

# LiteLLM is stateless, we just pass the key and the model string, we don't need to create a client object

async def get_llm_response(message: str, model: str = "gpt-4o-mini"):
    """
    Sends a message to the specified LLM and returns the text response.
    """

    try:
        response = await acompletion(
            model = model,
            messages = [{"role": "user", "content": message}],
            api_key = settings.openai_api_key,
        )

        # capture the cost data
        usage = response.usage

        return {
            "content": response.choices[0].message.content,
            "usage": {
                "prompt_tokens": usage.prompt_tokens,
                "completion_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens,
            }
        }
    
    except Exception as e:
        return f"Error communicating with LLM: {str(e)}"