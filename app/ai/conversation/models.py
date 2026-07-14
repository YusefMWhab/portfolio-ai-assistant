from dataclasses import dataclass, field
from pydantic import Field
from datetime import datetime
from app.ai.conversation.enums import Language


MAX_QUESTIONS_PER_SESSION = 15

@dataclass
class ConversationMessage:

    role: str 

    content: str

    timestamp: datetime


@dataclass
class ConversationSession:

    session_id: str

    language: Language = Language.ENGLISH

    current_topic: str | None = None

    messages: list[ConversationMessage] = field(default_factory=list)

    question_count: int = 0

    def register_question(self):
        self.question_count += 1

    def has_reached_limit(self) -> bool:
        return self.question_count >= MAX_QUESTIONS_PER_SESSION

    def remaining_questions(self) -> int:
        return max(0, MAX_QUESTIONS_PER_SESSION - self.question_count)

