from app.ai.agent import PortfolioAgent
from app.ai.conversation.manager import ConversationManager


class ChatService:

    def __init__(self, conversation: ConversationManager):
        self.agent = PortfolioAgent(conversation)
        

    async def ask(
        self,
        question: str,
        session_id: str
    ) -> str:

        return await self.agent.generate_answer(question, session_id=session_id)