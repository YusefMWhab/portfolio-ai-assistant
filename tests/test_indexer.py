import asyncio

from app.ai.rag.indexer import KnowledgeIndexer



async def main():

    indexer = KnowledgeIndexer()

    await indexer.build()



asyncio.run(main())