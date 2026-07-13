from app.ai.rag.loader import KnowledgeLoader
from app.ai.rag.chunker import MarkdownChunker


loader = KnowledgeLoader()

documents = loader.load()


chunker = MarkdownChunker()

chunks = chunker.chunk(documents)


for chunk in chunks:

    print("=" * 50)

    print("ID:", chunk.id)

    print("TITLE:", chunk.title)

    print("SECTION:", chunk.section)

    print("CONTENT:")
    print(chunk.content[:300])