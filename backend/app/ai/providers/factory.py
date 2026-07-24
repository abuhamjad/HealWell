import logging
from app.ai.providers.base import BaseProvider
from app.ai.providers.openai_provider import OpenAIProvider
from app.ai.providers.gemini import GeminiProvider
from app.ai.providers.mock_provider import MockProvider
from app.core.config import settings

logger = logging.getLogger(__name__)


def create_provider() -> BaseProvider:
    """Create and return the appropriate AI provider based on configuration.

    Automatically falls back to MockProvider if API keys are missing or provider setup fails.
    """
    provider_name = settings.LLM_PROVIDER.lower()

    if provider_name == "openai":
        if not settings.LLM_API_KEY:
            logger.info("No LLM_API_KEY set; defaulting to MockProvider")
            return MockProvider()
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

