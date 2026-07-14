from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import StreamingResponse

from app.services.voice_service import VoiceService

router = APIRouter(
    prefix="/api/voice",
    tags=["Voice"]
)

voice_service = VoiceService()


@router.post("/AI-agent/chat")
async def voice_chat(
    audio: UploadFile = File(...),
    session_id: str | None = Form(None)
):
    return await voice_service.process_voice(
        audio,
        session_id
    )

@router.get("/AI-agent/audio-stream/{session_id}")
async def stream_audio(session_id: str):
    return StreamingResponse(
        voice_service.stream_audio(session_id),
        media_type="application/x-ndjson",
    )

router.post("/AI-agent/end-session/{session_id}")
async def end_session(session_id: str):
    voice_service.end_session(session_id)
    return {"status": "ended"}