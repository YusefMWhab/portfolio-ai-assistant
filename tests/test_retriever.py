import asyncio

from app.ai.rag.retriever import Retriever



async def main():

    retriever = Retriever()


    results = await retriever.search(
        query="what is your current position",
        category="experience"
    )
    print(len(results))

    for result in results:

        print(result.payload["category"])
        print(result.payload["title"])
        print(result.payload["content"][:150])
        print()



asyncio.run(main())