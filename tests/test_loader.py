from app.ai.rag.loader import KnowledgeLoader


loader = KnowledgeLoader()

documents = loader.load()

for doc in documents:

    print("=" * 50)

    print(doc.id)

    print(doc.category)

    print(doc.title)

    print(doc.source)

    print(doc.content[:100])