from pathlib import Path

from app.ai.models.document_models import Document


class KnowledgeLoader:

    def __init__(self):
        self.root = Path("knowledge")

    def load(self) -> list[Document]:

        documents = []

        for file in self.root.rglob("*.md"):

            relative = file.relative_to(self.root)

            if relative.parent == Path("."):
                category = file.stem.lower()
            else:
                category = relative.parent.name.lower()

            document = Document(
                id=file.stem,
                title=file.stem.replace("_", " ").title(),
                category=category,
                source=file,
                content=file.read_text(encoding="utf-8")
            )

            documents.append(document)

        return documents