from app.ai.conversation.session import SessionManager
from app.ai.conversation.history import ConversationHistory
from app.ai.conversation.language import LanguageManager
from app.ai.conversation.topicManager import TopicTracker
from app.ai.conversation.enums import Language

class ConversationManager:

    def __init__(self):

        self.sessions = SessionManager()

        self.history = ConversationHistory()

        self.language = LanguageManager()

        self.topic = TopicTracker()


    def get_or_create(
        self,
        session_id: str | None
    ):

        if session_id:

            session = self.sessions.get(session_id)

            if session:
                return session

        return self.sessions.create()


    def add_user_message(
        self,
        session_id: str,
        message: str
    ):

        session = self.sessions.get(session_id)

        if session is None:
            return

        self.history.add_user_message(
            session,
            message
        )


    def add_assistant_message(
        self,
        session_id: str,
        message: str
    ):

        session = self.sessions.get(session_id)

        if session is None:
            return

        self.history.add_assistant_message(
            session,
            message
        )


    def get_history(
        self,
        session_id: str,
        limit: int = 10
    ):

        session = self.sessions.get(session_id)

        if session is None:
            return []

        return self.history.last_messages(
            session,
            limit
        )
    
    def set_language(
        self,
        session_id: str,
        language: Language
    ):
        session = self.sessions.get(session_id)

        if session is None:
            return

        self.language.set(
            session,
            language
        )
        

    def get_language(
        self,
        session_id: str
    ):

        session = self.sessions.get(session_id)

        if session is None:
            return None

        return self.language.get(session)


    def update_topic(
        self,
        session_id: str,
        results
    ):

        session = self.sessions.get(session_id)

        if session is None:
            return

        self.topic.update(
            session,
            results
        )


    def current_topic(
        self,
        session_id: str
    ):

        session = self.sessions.get(session_id)

        if session is None:
            return None

        return self.topic.current(session)


    def clear_topic(
        self,
        session_id: str
    ):

        session = self.sessions.get(session_id)

        if session is None:
            return

        self.topic.clear(session)

