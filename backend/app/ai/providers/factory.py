"""Provider factory for instantiating the AI provider."""

from app.ai.providers.base import BaseProvider
from app.ai.providers.openai_provider import OpenAIProvider
from app.core.config import settings


def create_provider() -> BaseProvider:
    """Create and return the OpenAI provider.

    Returns:
        BaseProvider: OpenAI provider instance.
    """
    return OpenAIProvider(
        api_key=settings.LLM_API_KEY,
        base_url=settings.LLM_BASE_URL,
        model=settings.LLM_MODEL,
        timeout=settings.LLM_TIMEOUT,
    )
