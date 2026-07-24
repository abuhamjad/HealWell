import asyncio
from openai import AsyncOpenAI

from app.core.config import settings


async def main():
    client = AsyncOpenAI(
        api_key=settings.LLM_API_KEY,
        base_url=settings.LLM_BASE_URL,
        timeout=settings.LLM_TIMEOUT,
    )

    response = await client.chat.completions.create(
        model=settings.LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": "Reply with exactly: Groq connection successful!"
            }
        ],
    )

    print(response.choices[0].message.content)


asyncio.run(main())