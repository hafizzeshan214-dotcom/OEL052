"""
student_model.py - Data model representing the students table.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Student:
    """Represents a row in the `students` table."""
    id: Optional[int]
    name: str
    class_name: str   # 'class' is a Python keyword, so we use class_name
    age: int

    @staticmethod
    def from_row(row: tuple) -> "Student":
        """Construct a Student from a DB tuple (id, name, class, age)."""
        return Student(id=row[0], name=row[1], class_name=row[2], age=row[3])

    def __repr__(self) -> str:
        return (f"Student(id={self.id}, name='{self.name}', "
                f"class='{self.class_name}', age={self.age})")
