"""
student_service.py - Student CRUD business logic.
"""
from typing import List, Optional
from app.utils.db import get_connection
from app.utils.logger import get_logger
from app.models.student_model import Student

logger = get_logger(__name__)


class StudentService:
    """Handles all student-related database operations."""

    # ── Validation helper ─────────────────────────────────────────────────────
    @staticmethod
    def _validate(name: str, class_name: str, age: str) -> int:
        """Validate and return parsed age; raises ValueError on bad input."""
        if not name.strip():
            raise ValueError("Student name cannot be empty.")
        if not class_name.strip():
            raise ValueError("Class cannot be empty.")
        try:
            age_int = int(age)
        except (ValueError, TypeError):
            raise ValueError("Age must be a valid integer.")
        if age_int <= 0 or age_int > 100:
            raise ValueError("Age must be between 1 and 100.")
        return age_int

    # ── Create ────────────────────────────────────────────────────────────────
    def add_student(self, name: str, class_name: str, age: str) -> None:
        """Insert a new student record."""
        age_int = self._validate(name, class_name, age)
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO students (name, class, age) VALUES (%s, %s, %s)",
                (name.strip(), class_name.strip(), age_int),
            )
            conn.commit()
            logger.info("Student added: name='%s', class='%s'", name, class_name)
        finally:
            cursor.close()
            conn.close()

    # ── Read ──────────────────────────────────────────────────────────────────
    def get_all_students(self) -> List[Student]:
        """Return all students ordered by name."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, class, age FROM students ORDER BY name")
            return [Student.from_row(row) for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()

    def get_student_by_id(self, student_id: int) -> Optional[Student]:
        """Return a single student or None if not found."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, class, age FROM students WHERE id = %s",
                (student_id,),
            )
            row = cursor.fetchone()
            return Student.from_row(row) if row else None
        finally:
            cursor.close()
            conn.close()

    # ── Update ────────────────────────────────────────────────────────────────
    def update_student(self, student_id: int, name: str,
                       class_name: str, age: str) -> None:
        """Update an existing student record."""
        age_int = self._validate(name, class_name, age)
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE students SET name=%s, class=%s, age=%s WHERE id=%s",
                (name.strip(), class_name.strip(), age_int, student_id),
            )
            conn.commit()
            logger.info("Student updated: id=%s", student_id)
        finally:
            cursor.close()
            conn.close()

    # ── Delete ────────────────────────────────────────────────────────────────
    def delete_student(self, student_id: int) -> None:
        """Delete a student and cascade to attendance/fees."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
            conn.commit()
            logger.info("Student deleted: id=%s", student_id)
        finally:
            cursor.close()
            conn.close()

    def get_total_count(self) -> int:
        """Return total number of students."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM students")
            return cursor.fetchone()[0]
        finally:
            cursor.close()
            conn.close()
