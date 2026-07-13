from markdown_it import MarkdownIt

from app.ai.models.document_models import Document
from app.ai.models.chunk_models import Chunk


class MarkdownChunker:

    def __init__(self):
        self.md = MarkdownIt()


    def chunk(
        self,
        documents: list[Document]
    ) -> list[Chunk]:

        chunks = []

        for document in documents:
            chunks.extend(
                self._chunk_document(document)
            )

        return chunks


    def _chunk_document(
        self,
        document: Document
    ) -> list[Chunk]:

        tokens = self.md.parse(document.content)

        chunks = []

        current_section = "Introduction"
        current_content = []

        chunk_index = 0


        for token in tokens:

            if token.type == "heading_open":

                if current_content:

                    chunks.append(
                        self._create_chunk(
                            document,
                            current_section,
                            "\n".join(current_content),
                            chunk_index
                        )
                    )

                    chunk_index += 1
                    current_content = []


            elif token.type == "inline":

                text = token.content.strip()

                if text:

                    if current_section == "Introduction":
                        current_section = text

                    else:
                        current_content.append(text)


        if current_content:

            chunks.append(
                self._create_chunk(
                    document,
                    current_section,
                    "\n".join(current_content),
                    chunk_index
                )
            )


        return chunks



    def _create_chunk(
        self,
        document,
        section,
        content,
        index
    ):

        return Chunk(

            id=f"{document.id}_{index}",

            document_id=document.id,

            title=document.title,

            section=section,

            category=document.category,

            source=document.source,

            content=content

        )