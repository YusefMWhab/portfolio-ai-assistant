import uuid

from app.ai.conversation.models import ConversationSession


class SessionManager:

    def __init__(self):

        self.sessions = {}        


    def create(self) -> ConversationSession:

        session = ConversationSession(
            session_id=str(uuid.uuid4())
        )

        self.sessions[session.session_id] = session

        return session


    def get(
        self,
        session_id: str
    ) -> ConversationSession | None:

        return self.sessions.get(session_id)


    def delete(
        self,
        session_id: str
    ):

        self.sessions.pop(session_id, None)
        print(f"End Session: {session_id}")
