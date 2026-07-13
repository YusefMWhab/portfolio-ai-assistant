from dataclasses import dataclass
from app.ai.conversation.enums import Language


@dataclass
class STTResult:
    transcript: str
    language: Language