"""
attendance_service.py - Attendance business logic.
"""
from datetime import date
from typing import List, Tuple
from app.utils.db import get_connection
from app.utils.logger import get_logger

logger = get_logger(__name__)

VALID_STATUSES = {"Present", "Absent", "Late"}


class AttendanceService:
    """Handles attendance marking and querying."""

    def mark_attendance(self, student_id: int,
                        att_date: str, status: str) -> None:
        """
        Insert or update an attendance record.

        Args:
            student_id: ID of the student.
            att_date:   ISO date string (YYYY-MM-DD).
            status:     One of 'Present', 'Absent', 'Late'.
        """
        if not att_date:
            raise ValueError("Date cannot be empty.")
        if status not in VALID_STATUSES:
            raise ValueError(f"Status must be one of: {VALID_STATUSES}")

        conn = get_connection()
        try:
            cursor = conn.cursor()
            # Upsert: replace existing record for same student + date
            cursor.execute(
                """INSERT INTO attendance (student_id, date, status)
                   VALUES (%s, %s, %s)
                   ON DUPLICATE KEY UPDATE status = VALUES(status)""",
                (student_id, att_date, status),
            )
            conn.commit()
            logger.info(
                "Attendance marked: student_id=%s, date=%s, status=%s",
                student_id, att_date, status,
            )
        finally:
            cursor.close()
            conn.close()

    def get_all_attendance(self) -> List[Tuple]:
        """
        Return all attendance records joined with student names.

        Returns:
            List of (attendance_id, student_name, date, status) tuples.
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.id, s.name, a.date, a.status
                FROM attendance a
                JOIN students s ON a.student_id = s.id
                ORDER BY a.date DESC, s.name
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_attendance_by_student(self, student_id: int) -> List[Tuple]:
        """Return attendance records for a specific student."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, student_id, date, status FROM attendance "
                "WHERE student_id = %s ORDER BY date DESC",
                (student_id,),
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_today_summary(self) -> dict:
        """Return today's present/absent/late counts."""
        today = date.today().isoformat()
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT status, COUNT(*) FROM attendance "
                "WHERE date = %s GROUP BY status",
                (today,),
            )
            result = {row[0]: row[1] for row in cursor.fetchall()}
            return result
        finally:
            cursor.close()
            conn.close()
