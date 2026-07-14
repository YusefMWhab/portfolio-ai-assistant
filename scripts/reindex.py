import asyncio

from app.ai.rag.loader import KnowledgeLoader
from app.ai.rag.chunker import MarkdownChunker
from app.ai.providers.gemini_provider import GeminiProvider
from app.ai.rag.vector_store import QdrantVectorStore


async def main():

    loader = KnowledgeLoader()
    chunker = MarkdownChunker()
    gemini = GeminiProvider()
    vector_store = QdrantVectorStore()

    print("Loading documents...")
    documents = loader.load()

    print("Chunking...")
    chunks = chunker.chunk(documents)

    print(f"Chunks: {len(chunks)}")

    print("Generating embeddings...")
    vectors = []

    for chunk in chunks:
        vectors.append(
            await gemini.embed_text(chunk.content)
        )

    print("Recreating collection...")

    vector_store.reset_collection(
        len(vectors[0])
    )

    print("Uploading...")

    vector_store.add_chunks(
        chunks,
        vectors
    )

    print("Done!")


asyncio.run(main())