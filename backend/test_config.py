from app.core.config import settings

print("Provider:", settings.LLM_PROVIDER)
print("Base URL:", settings.LLM_BASE_URL)
print("Model:", settings.LLM_MODEL)
print("API Key:", settings.LLM_API_KEY[:10] + "...")