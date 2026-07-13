from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from pathlib import Path

from app.services.voice_service import VoiceService
from app.ai.models.response_models import VoiceResponse

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

""" @router.get("/audio/{audio_id}")
async def get_audio(audio_id: str):
    audio_path = Path("static/audio/demo.m4a")

    return FileResponse(
        path=audio_path,
        media_type="audio/mp4",
        filename="demo.m4a"
    ) """