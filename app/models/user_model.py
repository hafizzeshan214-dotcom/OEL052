"""
user_model.py - Data model representing the users table.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """Represents a row in the `users` table."""
    id: Optional[int]
    username: str
    password: str

    @staticmethod
    def from_row(row: tuple) -> "User":
        """Construct a User from a DB tuple (id, username, password)."""
        return User(id=row[0], username=row[1], password=row[2])

    def __repr__(self) -> str:
        return f"User(id={self.id}, username='{self.username}')"
