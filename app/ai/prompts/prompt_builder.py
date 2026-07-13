from app.ai.prompts.system_prompt import PORTFOLIO_SYSTEM_PROMPT
from app.ai.conversation.enums import Language

class PromptBuilder:

    def build(
        self,
        question: str,
        context: str,
        language
    ) -> str:

        if not context.strip():
            context = "No relevant portfolio information was retrieved."

        if language == Language.ARABIC:
            response_language = """
        ### Response Language
        The user is speaking Arabic.

        Always answer in fluent Egyptian Local friendly Arabic.

        Keep all technical terms (Python, FastAPI, Docker, RAG, etc.) in English when appropriate.

        Do not answer in English unless the user explicitly asks.
        """

        else:

            response_language = """
        ### Response Language
        The user is speaking English.

        Always answer in professional English.
        """
        return f"""
{PORTFOLIO_SYSTEM_PROMPT}

{response_language}

### Portfolio Context
{context}

### User Question
{question}

### Assistant Answer
"""