from google import genai
from google.genai import types

from app.core.config import settings


class GeminiProvider:

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    async def generate_text(self, prompt: str) -> str:

        response = self.client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt
        )

        return response.text.strip()
    
    async def transcribe_audio(
        self,
        audio_bytes: bytes,
        mime_type: str
    ) -> str:

        response = self.client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=[
                types.Part.from_bytes(
                    data=audio_bytes,
                    mime_type=mime_type
                ),
                """
Transcribe this audio.

Return ONLY a JSON object in this format:

{
  "transcript": "...",
  "language": "ar"
}

Rules:
- language must be "ar" for Arabic.
- language must be "en" for English.
- Do not include markdown.
- Do not wrap the JSON in ``` blocks.
"""
            ]
        )

        return response.text
    
    async def text_to_speech(self, text: str) -> bytes:

        config = types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name="Puck"
                    )
                )
            )
        )

        response = await self.client.aio.models.generate_content(
            model=settings.GEMINI_MODEL_TTS, 
            contents=text,
            config=config
        )

        try:
            audio_part = response.candidates[0].content.parts[0]
            if audio_part.inline_data:
                return audio_part.inline_data.data
            else:
                raise ValueError("Gemini did not return inline audio data.")
        except (IndexError, AttributeError) as e:
            raise RuntimeError(f"Failed to extract audio from Gemini response: {str(e)}")