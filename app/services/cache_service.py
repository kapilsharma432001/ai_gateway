from redisvl.extensions.llmcache import SemanticCache
from app.config import settings

# We will use OpenAI embedding model to turn text into vectors
class AICache:
    def __init__(self):
        self.cache = SemanticCache(
            name = "llm_cache",
            redis_url = settings.redis_url,
            distance_threshold = 0.1, # How close the meaning must be 0 to 1
        )
    
    async def check_cache(self, prompt: str):
        pass

    async def update_cache(self, prompt: str, response: str):
        pass

# Initialize the cache (singleton pattern)
ai_cache = AICache()
