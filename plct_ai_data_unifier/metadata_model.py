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

from typing import Literal, Optional, List

from pydantic import BaseModel, Field


class UdSegment(BaseModel):
    """A single node in the content tree.

    Leaf segments carry a ``content_path``; branch segments only have
    nested ``sub_segments``.
    """

    segment_id: str
    title: str
    content_path: Optional[str] = None
    sub_segments: List[UdSegment] = Field(default_factory=list)


class UdBook(BaseModel):
    """Top-level structure.json schema."""

    schema_version: int = 1
    book_id: str
    source_type: Literal["petljadoc", "plct"]
    title: str
    segments: List[UdSegment] = Field(default_factory=list)
