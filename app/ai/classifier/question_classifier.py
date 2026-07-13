from app.ai.prompts.classifier_prompt import QUESTION_CLASSIFIER_PROMPT
from app.ai.providers.gemini_provider import GeminiProvider


class QuestionClassifier:

    def __init__(self):
        self.llm = GeminiProvider()

    async def classify(
        self,
        question: str
    ) -> str:

        prompt = f"""
{QUESTION_CLASSIFIER_PROMPT}

Question:

{question}
"""

        category = await self.llm.generate_text(prompt)

        return category.strip().lower()