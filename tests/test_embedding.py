import asyncio

from app.ai.embeddings.gemini_embedding import GeminiEmbedding


async def main():

    embedding = GeminiEmbedding()

    vector = await embedding.embed_text(
        "NarrIQ is an AI powered SaaS platform"
    )

    print(len(vector))

    print(vector[:10])


asyncio.run(main())