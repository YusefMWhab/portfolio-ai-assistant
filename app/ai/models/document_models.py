from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Document:
    id: str
    title: str
    category: str
    source: Path
    content: str