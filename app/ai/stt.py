from app.ai.models.stt_models import STTResult
from app.ai.conversation.enums import Language
from app.ai.providers.gemini_provider import GeminiProvider
import json

class SpeechToText:

    def __init__(self):

        self.gemini = GeminiProvider()

    async def transcribe(
        self,
        audio_bytes: bytes,
        mime_type: str
    ) -> str:


        raw  = await self.gemini.transcribe_audio(
            audio_bytes=audio_bytes,
            mime_type=mime_type
        )

        text = raw.strip()
        
        data = json.loads(text)

        return STTResult(
            transcript=data["transcript"],
            language=Language(data["language"])
        )