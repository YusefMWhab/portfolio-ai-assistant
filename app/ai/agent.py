from app.ai.providers.gemini_provider import GeminiProvider
from app.ai.rag.retriever import Retriever
from app.ai.classifier.question_classifier import QuestionClassifier
from app.ai.rag.context_builder import ContextBuilder
from app.ai.prompts.prompt_builder import PromptBuilder
from app.ai.conversation.query_rewriter import SearchQueryRewriter
from app.ai.conversation.manager import ConversationManager


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

        print("Original:", original_question)
        print("Rewritten:", question)
        print("Category:", category)
        print("Session:", session_id)
        print("Topic before:", self.conversation.current_topic(session_id))
        print("Language:", language)

        # Retrieve
        results = await self.retriever.search(
            query=question,
            category=category
        )

        self.conversation.update_topic(
            session_id,
            results
        )

        print("Session:", session_id)
        print("Topic after:", self.conversation.current_topic(session_id))
        
        # Build Context
        context = self.context_builder.build(results)

        # Prompt
        prompt = self.prompt_builder.build(
            question=question,
            context=context,
            language=language
        )
        answer = await self.llm.generate_text(prompt)

        self.conversation.add_assistant_message(session_id=session_id, message=answer)

        

        return answer