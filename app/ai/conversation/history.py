from datetime import datetime

from app.ai.conversation.models import (
    ConversationMessage,
    ConversationSession
)


class ConversationHistory:

    def add_user_message(
        self,
        session: ConversationSession,
        content: str
    ):

        session.messages.append(

            ConversationMessage(
                role="user",
                content=content,
                timestamp=datetime.now()
            )

        )

    def add_assistant_message(
        self,
        session: ConversationSession,
        content: str
    ):

        session.messages.append(

            ConversationMessage(
                role="assistant",
                content=content,
                timestamp=datetime.now()
            )

        )

    def last_messages(
        self,
        session: ConversationSession,
        limit: int = 10
    ):

        return session.messages[-limit:]