import asyncio

from app.ai.agent import PortfolioAgent
from tests.evaluation.questions import TEST_QUESTIONS


async def main():

    agent = PortfolioAgent()

    for index, question in enumerate(TEST_QUESTIONS, 1):

        print("=" * 80)
        print(f"{index}. {question}")
        print()

        answer = await agent.generate_answer(question)

        print(answer)
        print()


asyncio.run(main())