from app.ai.providers.gemini_provider import GeminiProvider
from app.ai.rag.retriever import Retriever
from app.ai.classifier.question_classifier import QuestionClassifier
from app.ai.rag.context_builder import ContextBuilder
from app.ai.prompts.prompt_builder import PromptBuilder
from app.ai.conversation.query_rewriter import SearchQueryRewriter
from app.ai.conversation.manager import ConversationManager

import logging
logger = logging.getLogger(__name__)

class PortfolioAgent:

    def __init__(self, conversation: ConversationManager):

        self.llm = GeminiProvider()

        self.classifier = QuestionClassifier()

        self.retriever = Retriever()

        self.context_builder = ContextBuilder()

        self.prompt_builder = PromptBuilder()

        self.rewriter = SearchQueryRewriter()

        self.conversation = conversation
        


    async def generate_answer(
        self,
        question: str,
        session_id: str
    ) -> str:
        
        self.conversation.add_user_message(session_id=session_id, message=question)

        language = self.conversation.get_language(session_id=session_id)
        
        original_question = question
        
        history = self.conversation.get_history(session_id, limit=4)

        topic = self.conversation.current_topic(session_id)

        question = await self.rewriter.rewrite(
            question=question,
            history=history,
            current_topic=topic
        )
        

        category = await self.classifier.classify(question)

        logger.info(f"Original: {original_question}")
        logger.info(f"Rewritten: {question}")
        logger.info(f"Category: {category}")
        logger.info(f"Session: {session_id}")
        logger.info(f"Topic before: {self.conversation.current_topic(session_id)}")
        logger.info(f"Language: {language}")

        # Retrieve
        results = await self.retriever.search(
            query=question,
            category=category
        )

        self.conversation.update_topic(
            session_id,
            results
        )
        
        # Build Context
        context = self.context_builder.build(results)

        # Prompt
        prompt = self.prompt_builder.build(
            question=original_question,
            context=context,
            language=language
        )

        logger.info(f"Prompt: {prompt}")
        answer = await self.llm.generate_text(prompt)

        self.conversation.add_assistant_message(session_id=session_id, message=answer)

        return answer