from app.ai.embeddings.gemini_embedding import GeminiEmbedding
from app.ai.rag.vector_store import QdrantVectorStore


class Retriever:

    def __init__(self):

        self.embedding = GeminiEmbedding()
        self.vector_store = QdrantVectorStore()

    async def search(
        self,
        query: str,
        limit: int = 5,
        category: str | None = None
    ):

        query_vector = await self.embedding.embed_text(query)

        results = self.vector_store.search(
            vector=query_vector,
            limit=limit,
            category=category
        )

        return results