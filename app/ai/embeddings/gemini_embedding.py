from google import genai

from app.core.config import settings


class GeminiEmbedding:

    def __init__(self):

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = settings.GEMINI_EMBEDDING_MODEL


    async def embed_text(
        self,
        text: str
    ) -> list[float]:

        response = self.client.models.embed_content(
            model=self.model,
            contents=text
        )

        return response.embeddings[0].values