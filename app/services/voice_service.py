from fastapi import UploadFile

from app.ai.models.response_models import VoiceResponse
from app.ai.stt import SpeechToText
from app.services.chat_service import ChatService
from app.ai.tts import TextToSpeech
from app.ai.conversation.manager import ConversationManager
from fastapi import HTTPException

import logging
logger = logging.getLogger(__name__)


class VoiceService:

    def __init__(self):
        
        self.conversation = ConversationManager()

        self.stt = SpeechToText()

        self.chat = ChatService(conversation=self.conversation)

        self.tts = TextToSpeech()

    async def process_voice(self, audio: UploadFile, session_id: str | None):
        logger.info("Getting session & session limit")
        session = self.conversation.get_or_create(session_id)
        limit_reached = self.conversation.is_limit_reached(session.session_id)    

        if limit_reached:
            logger.warning("Session limit reached")
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "session_limit_reached",
                    "message": "We've reached the question limit for this conversation. Refresh the page to start a new chat."
                }
            )

        # =====================
        # Read Audio
        # ====================
        logger.info("Starting reading audio")
        audio_bytes = await audio.read()
        if not audio_bytes:
            logger.warning("Read audio failed")
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "empty_audio",
                     "message": "I couldn't hear anything. Please try recording your question again."
                }
            )  

        # =====================
        # STT
        # =====================
        try:
            logger.info("Starting STT")
            stt_result = await self.stt.transcribe(audio_bytes=audio_bytes, mime_type=audio.content_type)
            transcript = stt_result.transcript
            language = stt_result.language
        except Exception:
            logger.exception("STT failed")
            raise HTTPException(
                status_code=502,
                detail={
                    "error": "speech_recognition_failed",
                    "message": "Sorry, I couldn't understand your voice. Could you try saying that again?"
                }
            )

        # =====================
        # Session
        # =====================
        
        self.conversation.set_language(
            session.session_id,
            language
        )

        # =====================
        # LLM
        # =====================
        try:
            logger.info("Starting LLM & Retrieve pipline")
            answer = await self.chat.ask(transcript, session_id=session.session_id)
        except Exception:
            logger.exception("LLM & Retrieve pipline failed")
            raise HTTPException(
                status_code=502,
                detail={
                    "error": "llm_failed",
                    "message": "Sorry, I ran into a problem while generating my response. Please try again in a moment."
                }
            )

        # =====================
        # Get remaining quota
        # =====================
        remaining_quota = self.conversation.get_session_quota(session_id=session.session_id)
        
        # =====================
        # Final result ( Text answers & Session ID & Transcription)
        # =====================
        return VoiceResponse(
            session_id=session.session_id,
            transcription=transcript,
            answer=answer,
            remaining_questions=remaining_quota
        )
    
    # =====================
    # TTS & Audio Generation
    # =====================
    def stream_audio(self, session_id: str | None):
        
        if not session_id:
            return
        
        answer = self.conversation.get_last_assistant_message(session_id)
        language = self.conversation.get_language(session_id)


        if not answer:
            return

        try:
            logger.info("Starting TTS")
            tts_result = self.tts.generateStream(answer, language)

        except Exception:
            logger.exception("TTS failed")
            raise HTTPException(
                status_code=502,
                detail={
                    "error": "text_to_speach_failed",
                    "message": "I couldn't generate the voice response, but you can still read my answer above."
                }
            )

        return tts_result
    
    # =====================
    # End Session
    # =====================
    def end_session(self, session_id: str | None):
        self.conversation.end_session(session_id)
