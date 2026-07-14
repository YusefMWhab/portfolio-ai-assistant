from pydantic import BaseModel

class ChatResponse(BaseModel):
    answer: str

class VoiceResponse(BaseModel):

    session_id: str

    transcription: str

    answer: str

    remaining_questions: int
