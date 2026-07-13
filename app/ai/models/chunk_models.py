from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Chunk:
    id: str
    document_id: str
    title: str
    section: str
    category: str
    source: Path
    content: str