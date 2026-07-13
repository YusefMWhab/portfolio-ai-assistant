from app.ai.rag.loader import KnowledgeLoader
from app.ai.rag.chunker import MarkdownChunker
from app.ai.embeddings.gemini_embedding import GeminiEmbedding
from app.ai.rag.vector_store import QdrantVectorStore


class KnowledgeIndexer:


    def __init__(self):

        self.loader = KnowledgeLoader()

        self.chunker = MarkdownChunker()

        self.embedding = GeminiEmbedding()

        self.vector_store = QdrantVectorStore()



    async def build(self):

        print("Loading documents...")

        documents = self.loader.load()


        print("Creating chunks...")

        chunks = self.chunker.chunk(documents)


        print(
            f"Created {len(chunks)} chunks"
        )


        vectors = []


        print("Generating embeddings...")


        for chunk in chunks:

            vector = await self.embedding.embed_text(
                chunk.content
            )

            vectors.append(vector)



        print("Creating collection...")


        self.vector_store.create_collection(
            vector_size=len(vectors[0])
        )


        print("Saving to Qdrant...")


        self.vector_store.add_chunks(
            chunks,
            vectors
        )


        print("Knowledge Base Ready 🚀")