import asyncio

from app.ai.agent import PortfolioAgent


async def main():

    agent = PortfolioAgent()

    while True:

        question = input("\nYou: ")

        if question.lower() in ["exit", "quit"]:
            break

        answer = await agent.generate_answer(question)

        print("\nAI:")
        print(answer)


if __name__ == "__main__":
    asyncio.run(main())