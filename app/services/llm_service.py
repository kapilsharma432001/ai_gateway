from litellm import acompletion
import os

# LiteLLM is stateless, we just pass the key and the model string, we don't need to create a client object

async def get_llm_response(message: str, model: str = "gpt-4o-mini"):
    """
    Sends a message to the specified LLM and returns the text response.
    """

    try:
        response = await acompletion(
            model = model,
            messages = [{"role": "user", "content": message}],
            api_key = os.getenv("OPENAI_API_KEY")
        )

        # Extract just the text content from the response
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error communicating with LLM: {str(e)}"