from app.ai.providers.gemini_provider import GeminiProvider
from app.ai.rag.vector_store import QdrantVectorStore


class Retriever:

    def __init__(self):

        self.gemini = GeminiProvider()
        self.vector_store = QdrantVectorStore()

    async def search(
        self,
        query: str,
        limit: int = 10,
        category: str | None = None
    ):

        query_vector = await self.gemini.embed_text(query)

        results = self.vector_store.search(
            vector=query_vector,
            limit=limit,
            category=category
        )

        return results