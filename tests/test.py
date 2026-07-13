from fastapi import APIRouter

from app.ai.providers.gemini_provider import GeminiProvider

router = APIRouter(
    prefix="/api/test",
    tags=["Test"]
)

gemini = GeminiProvider()


@router.get("/gemini")
async def test():

    answer = await gemini.generate_text(
        "Say hello in one sentence."
    )

    return {
        "answer": answer
    }