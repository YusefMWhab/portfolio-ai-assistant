from langdetect import detect

from app.ai.conversation.models import ConversationSession
from app.ai.conversation.enums import Language



class LanguageManager:

    def set(
        self,
        session: ConversationSession,
        language: Language
    ):
        session.language = language


    def get(
        self,
        session: ConversationSession
    ) -> Language:

        return session.language or Language.ENGLISH
