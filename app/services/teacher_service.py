"""
teacher_service.py - Teacher CRUD business logic.
"""
from typing import List, Optional
from app.utils.db import get_connection
from app.utils.logger import get_logger
from app.models.teacher_model import Teacher

logger = get_logger(__name__)


class TeacherService:
    """Handles all teacher-related database operations."""

    @staticmethod
    def _validate(name: str, subject: str) -> None:
        if not name.strip():
            raise ValueError("Teacher name cannot be empty.")
        if not subject.strip():
            raise ValueError("Subject cannot be empty.")

    def add_teacher(self, name: str, subject: str) -> None:
        """Insert a new teacher record."""
        self._validate(name, subject)
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO teachers (name, subject) VALUES (%s, %s)",
                (name.strip(), subject.strip()),
            )
            conn.commit()
            logger.info("Teacher added: name='%s', subject='%s'", name, subject)
        finally:
            cursor.close()
            conn.close()

    def get_all_teachers(self) -> List[Teacher]:
        """Return all teachers ordered by name."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, subject FROM teachers ORDER BY name")
            return [Teacher.from_row(row) for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()

    def get_teacher_by_id(self, teacher_id: int) -> Optional[Teacher]:
        """Return a single teacher or None if not found."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, subject FROM teachers WHERE id = %s",
                (teacher_id,),
            )
            row = cursor.fetchone()
            return Teacher.from_row(row) if row else None
        finally:
            cursor.close()
            conn.close()

    def update_teacher(self, teacher_id: int, name: str, subject: str) -> None:
        """Update an existing teacher record."""
        self._validate(name, subject)
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE teachers SET name=%s, subject=%s WHERE id=%s",
                (name.strip(), subject.strip(), teacher_id),
            )
            conn.commit()
            logger.info("Teacher updated: id=%s", teacher_id)
        finally:
            cursor.close()
            conn.close()

    def delete_teacher(self, teacher_id: int) -> None:
        """Delete a teacher record."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM teachers WHERE id = %s", (teacher_id,))
            conn.commit()
            logger.info("Teacher deleted: id=%s", teacher_id)
        finally:
            cursor.close()
            conn.close()

    def get_total_count(self) -> int:
        """Return total number of teachers."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM teachers")
            return cursor.fetchone()[0]
        finally:
            cursor.close()
            conn.close()
