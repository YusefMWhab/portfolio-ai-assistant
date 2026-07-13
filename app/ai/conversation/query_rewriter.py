from app.ai.providers.gemini_provider import GeminiProvider


class SearchQueryRewriter:

    def __init__(self):

        self.llm = GeminiProvider()

    async def rewrite(
        self,
        question: str,
        history,
        current_topic: str | None
    ) -> str:

        history_text = ""

        for message in history:

            history_text += (
                f"{message.role}: {message.content}\n"
            )

        prompt = f"""
You are a Search Query Rewriter.

Your job is to convert EVERY user question into a single standalone English search query optimized for semantic retrieval.

The rewritten query should maximize retrieval accuracy while preserving the user's intent.

Current topic:
{current_topic}

Conversation history:
{history_text}

Current question:
{question}

Rules:

1. Return ONLY ONE search query.

2. If the user asks multiple questions, keep ONLY the FIRST question.

Example:
Question:
What technologies did you use and what challenges did you face?

Output:
What technologies were used in the NarrIQ project?

3. Always return the query in English.

4. If the original question is in Arabic, translate it to natural English.

5. If the user refers to:
- it
- this
- that
- the project
- the company
or omits the entity,
replace it with the Current Topic.

6. If Current Topic is available, the rewritten query MUST explicitly contain it.

7. Preserve the user's intent.

8. Do NOT answer the question.

9. Do NOT explain anything.

10. Return ONLY the rewritten query as plain text.

Examples

Topic:
NarrIQ

Question:
ايه التقنيات اللي استخدمتها فيه؟

Output:
What technologies were used in the NarrIQ project?

Topic:
NarrIQ

Question:
Could you give me a short brief?

Output:
Give me a brief overview of the NarrIQ project.

Topic:
NarrIQ

Question:
What is it designed for?

Output:
What is the NarrIQ project designed for?

Topic:
DataWhisperer

Question:
Could you explain it and what technologies did you use?

Output:
Could you explain the DataWhisperer project?

Rewrite the following question.

Question:
{question}
"""

        return await self.llm.generate_text(prompt)