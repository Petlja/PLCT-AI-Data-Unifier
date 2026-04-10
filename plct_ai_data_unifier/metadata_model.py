"""Pydantic models for the dataset structure metadata (structure.json).

These models define the schema for the structure.json files produced by
the data-unifier pipeline.  They are intentionally kept in their own
module so that downstream projects can import and validate / deserialise
these files without pulling in the rest of the pipeline.

Typical consumer usage::

    import json
    from plct_ai_data_unifier.metadata_model import UdBook

    with open("structure.json") as f:
        book = UdBook.model_validate_json(f.read())
"""

from __future__ import annotations

from pathlib import Path
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field


class PetljaActivityEnum(StrEnum):
    """Petlja activity types from course YAML metadata."""

    READING = "reading"
    QUIZ = "quiz"
    CODINGQUIZ = "codingquiz"
    VIDEO = "video"
    PDF = "pdf"


class PetljaLectureEnum(StrEnum):
    """Petlja didactic segment types (for example, index-like lecture nodes)."""

    LECTURE = "lecture"


class PlctSegmentEnum(StrEnum):
    """PLCT segment types placeholder until PLCT introduces a stable taxonomy."""
    LESSON = "lesson"
    ACTIVITY = "activity"


type UdSegmentSourceType = (
    PetljaActivityEnum | PetljaLectureEnum | PlctSegmentEnum | str
)


class UdSegment(BaseModel):
    """A single node in the content tree.

    Leaf segments carry a ``content_path``; branch segments only have
    nested ``sub_segments``.
    """

    segment_id: str
    title: str
    content_path: str | None = None
    sub_segments: list[UdSegment] = Field(default_factory=list)
    source_type: UdSegmentSourceType | None = None


class UdBook(BaseModel):
    """Top-level structure.json schema."""

    schema_version: int = 1
    book_id: str
    source_type: Literal["petljadoc", "plct"]
    title: str
    description: dict | None = None
    segments: list[UdSegment] = Field(default_factory=list)


    base_path: str | None = Field(default=None, exclude=True)

    @classmethod
    def load_dataset(cls, dataset_dir: str | Path) -> list[UdBook]:
        """Load all books from a dataset directory.

        Scans immediate subdirectories of ``dataset_dir`` for a
        ``structure.json`` file and returns a list of validated
        ``UdBook`` instances with ``base_path`` set to the
        subdirectory path.
        """
        dataset_path = Path(dataset_dir)
        books: list[UdBook] = []
        for child in sorted(dataset_path.iterdir()):
            structure_file = child / "structure.json"
            if child.is_dir() and structure_file.is_file():
                book = cls.model_validate_json(structure_file.read_text(encoding="utf-8"))
                book.base_path = child.as_posix()
                books.append(book)
        return books
