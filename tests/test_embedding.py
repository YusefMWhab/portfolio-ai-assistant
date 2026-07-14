import asyncio

from app.ai.providers.gemini_provider import GeminiProvider


async def main():

    gemini = GeminiProvider()

    vector = await gemini.embed_text(
        "NarrIQ is an AI powered SaaS platform"
    )

    print(len(vector))

    print(vector[:10])


asyncio.run(main())