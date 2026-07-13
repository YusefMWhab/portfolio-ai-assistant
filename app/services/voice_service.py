from fastapi import UploadFile

from app.ai.models.response_models import VoiceResponse
from app.ai.stt import SpeechToText
from app.services.chat_service import ChatService
from app.ai.tts import TextToSpeech
from app.ai.conversation.manager import ConversationManager

import logging
from time import perf_counter
import os
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("logs/performance.log", encoding="utf-8"),
        logging.StreamHandler()   # يخليها تظهر في التيرمينال كمان
    ]
)

logger = logging.getLogger("performance")

class VoiceService:

    def __init__(self):
        
        self.conversation = ConversationManager()
        

        self.stt = SpeechToText()

        self.chat = ChatService(conversation=self.conversation)

        self.tts = TextToSpeech()

    async def process_voice(self, audio: UploadFile, session_id: str | None):

        total_start = perf_counter()

        # =====================
        # Read Audio
        # ====================
        start = perf_counter()
        audio_bytes = await audio.read()
        logger.info(f"[READ AUDIO] {(perf_counter() - start):.3f}s")

        # =====================
        # STT
        # =====================
        start = perf_counter()
        stt_result = await self.stt.transcribe(audio_bytes=audio_bytes, mime_type=audio.content_type)
        transcript = stt_result.transcript
        language = stt_result.language
        stt_time = perf_counter() - start

        logger.info(
            f"[STT] {stt_time:.3f}s | "
            f"Lang={language} | "
            f'Text="{transcript}"'
        )

        # =====================
        # Session
        # =====================
        session = self.conversation.get_or_create(session_id)
        self.conversation.set_language(
            session.session_id,
            language
        )

        # =====================
        # LLM
        # =====================
        start = perf_counter()
        answer = await self.chat.ask(transcript, session_id=session.session_id)
        llm_time = perf_counter() - start
        logger.info(
            f"[LLM] {llm_time:.3f}s | "
        )

        # =====================
        # TTS
        # =====================
        start = perf_counter()
        audio_response_base64_str = await self.tts.generateAudio(answer, language)
        tts_time = perf_counter() - start

        logger.info(
            f"[TTS] {tts_time:.2f}s | "
            f"chars={len(answer)} | "
        )
        
        # 7. Return the final results
        return VoiceResponse(
            session_id=session.session_id,
            transcription=transcript,
            answer=answer,
            audio_base64=audio_response_base64_str
        )