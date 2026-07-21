"""Provider factory for instantiating the appropriate AI provider."""

from app.ai.providers.base import BaseProvider
from app.ai.providers.openai_provider import OpenAIProvider
from app.ai.providers.gemini import GeminiProvider
from app.core.config import settings


def create_provider() -> BaseProvider:
    """Create and return the appropriate AI provider based on configuration.

    Returns:
        BaseProvider: Initialized provider instance.

    Raises:
        ValueError: If LLM_PROVIDER is not recognized.
    """
    provider_name = settings.LLM_PROVIDER.lower()

    if provider_name == "openai":
        return OpenAIProvider(
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_BASE_URL,
            model=settings.LLM_MODEL,
            timeout=settings.LLM_TIMEOUT,
        )
    elif provider_name == "gemini":
        return GeminiProvider(api_key=settings.GEMINI_API_KEY)
    else:
        raise ValueError(f"Unknown LLM provider: {provider_name}")
