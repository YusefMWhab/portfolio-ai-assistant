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

3. Always return the query in English.

4. If the original question is in Arabic, translate it to natural English.

5. Resolve pronouns only.

If the user says:
- it
- this
- that
- the company

replace them with Current Topic.

6. If the user's question is generic (for example: "all projects", "your skills", "your education", "tell me about yourself"), NEVER inject the current topic.

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

Examples:

User:
What are all projects did you work on?

Correct:
What projects has Youssef Mohamed worked on?

Wrong:
Portfolio AI Assistant projects

Topic:
Portfolio AI Assistant

Question:
Tell me about your education.

Output:
Tell me about Youssef Mohamed's education.

Question:
{question}
"""

        return await self.llm.generate_text(prompt)