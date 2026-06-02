"""
teacher_model.py - Data model representing the teachers table.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Teacher:
    """Represents a row in the `teachers` table."""
    id: Optional[int]
    name: str
    subject: str

    @staticmethod
    def from_row(row: tuple) -> "Teacher":
        """Construct a Teacher from a DB tuple (id, name, subject)."""
        return Teacher(id=row[0], name=row[1], subject=row[2])

    def __repr__(self) -> str:
        return f"Teacher(id={self.id}, name='{self.name}', subject='{self.subject}')"
