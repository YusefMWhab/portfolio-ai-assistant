from pydantic import BaseModel

class ChatResponse(BaseModel):
    answer: str

class VoiceResponse(BaseModel):

    session_id: str

    transcription: str

    answer: str

    audio_base64: str
