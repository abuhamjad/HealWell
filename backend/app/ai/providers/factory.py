import logging
from app.ai.providers.base import BaseProvider
from app.ai.providers.openai_provider import OpenAIProvider
from app.ai.providers.groq_provider import GroqProvider
from app.ai.providers.gemini import GeminiProvider
from app.ai.providers.mock_provider import MockProvider
from app.core.config import settings

logger = logging.getLogger(__name__)


def create_provider() -> BaseProvider:
    """Create and return the appropriate AI provider based on configuration.

    Supports Groq, OpenAI, Gemini, and automatically falls back to MockProvider
    if API keys are missing or provider setup fails.
    """
    provider_name = settings.LLM_PROVIDER.lower()

    if provider_name in ["groq", "openai"]:
        if not settings.LLM_API_KEY:
            logger.info("No LLM_API_KEY set; defaulting to MockProvider")
            return MockProvider()
        
        # If base_url contains groq or provider is explicitly groq, return GroqProvider
        base_url = settings.LLM_BASE_URL or ""
        if provider_name == "groq" or "groq.com" in base_url or "gpt-oss" in (settings.LLM_MODEL or ""):
            logger.info("Initializing GroqProvider")
            return GroqProvider(
                api_key=settings.LLM_API_KEY,
                base_url=settings.LLM_BASE_URL,
                model=settings.LLM_MODEL,
                timeout=settings.LLM_TIMEOUT,
            )
        return OpenAIProvider(
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_BASE_URL,
            model=settings.LLM_MODEL,
            timeout=settings.LLM_TIMEOUT,
        )
    elif provider_name == "gemini":
        gemini_key = getattr(settings, "GEMINI_API_KEY", None)
        if not gemini_key:
            logger.info("No GEMINI_API_KEY set; defaulting to MockProvider")
            return MockProvider()
        return GeminiProvider(api_key=gemini_key)
    elif provider_name == "mock":
        return MockProvider()
    else:
        logger.warning(f"Unknown LLM provider: {provider_name}; defaulting to MockProvider")
        return MockProvider()


