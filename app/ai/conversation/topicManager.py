class TopicTracker:

    def update(
        self,
        session,
        results
    ):

        if not results:
            return

        first = results[0]

        session.current_topic = first.payload["title"]


    def current(
        self,
        session
    ):

        return session.current_topic


    def clear(
        self,
        session
    ):

        session.current_topic = None