class ContextBuilder:


    def build(self, results):

        contexts = []

        for result in results:

            content = result.payload["content"]

            title = result.payload["title"]

            contexts.append(
                f"""
Document: {title}

{content}
"""
            )


        return "\n\n".join(contexts)