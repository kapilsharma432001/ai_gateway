# High-Performance AI Gateway

A high-throughput middleware proxy for LLM providers (OpenAI, Anthropic, etc.) designed to reduce costs and latency.

## 🚀 Key Features
1.  **Universal Interface:** Standardized API calls via LiteLLM.
2.  **Semantic Caching:** Vector-based caching (RedisVL) to return cached answers for semantically similar queries (<50ms).
3.  **Distributed Rate Limiting:** Token Bucket algorithm implemented via Redis Lua scripts.
4.  **Resilience:** Automatic failover and retry logic.

## 🛠 Tech Stack
* **Core:** Python 3.11+, FastAPI, Uvicorn
* **LLM Ops:** LiteLLM
* **Data & Cache:** Redis (RedisVL for vectors)

## 📂 Architecture (Planned)
[Client] -> [FastAPI Gateway] -> [Redis Semantic Cache]
                      |
                      v
               [LLM Provider (OpenAI/Anthropic)]