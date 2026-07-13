from dataclasses import dataclass, field
from pydantic import Field
from datetime import datetime
from app.ai.conversation.enums import Language

@dataclass
class ConversationMessage:

    role: str          # user | assistant | system

    content: str

    timestamp: datetime


@dataclass
class ConversationSession:

    session_id: str

    language: Language = Language.ENGLISH

    tone: str = "professional"

    current_topic: str | None = None

    messages: list[ConversationMessage] = field(default_factory=list)


