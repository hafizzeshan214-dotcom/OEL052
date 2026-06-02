"""
fee_service.py - Fee management business logic.
"""
from typing import List, Tuple
from app.utils.db import get_connection
from app.utils.logger import get_logger

logger = get_logger(__name__)


class FeeService:
    """Handles fee recording and querying."""

    @staticmethod
    def _validate(student_id: int, amount: str, fee_date: str) -> float:
        if not fee_date:
            raise ValueError("Date cannot be empty.")
        try:
            amount_float = float(amount)
        except (ValueError, TypeError):
            raise ValueError("Amount must be a valid number.")
        if amount_float <= 0:
            raise ValueError("Amount must be greater than zero.")
        return amount_float

    def add_fee(self, student_id: int, amount: str, fee_date: str) -> None:
        """Insert a new fee record."""
        amount_float = self._validate(student_id, amount, fee_date)
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO fees (student_id, amount, date) VALUES (%s, %s, %s)",
                (student_id, amount_float, fee_date),
            )
            conn.commit()
            logger.info(
                "Fee added: student_id=%s, amount=%.2f, date=%s",
                student_id, amount_float, fee_date,
            )
        finally:
            cursor.close()
            conn.close()

    def get_all_fees(self) -> List[Tuple]:
        """
        Return all fee records joined with student names.

        Returns:
            List of (fee_id, student_name, amount, date) tuples.
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT f.id, s.name, f.amount, f.date
                FROM fees f
                JOIN students s ON f.student_id = s.id
                ORDER BY f.date DESC
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_fees_by_student(self, student_id: int) -> List[Tuple]:
        """Return fee records for a specific student."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, student_id, amount, date FROM fees "
                "WHERE student_id = %s ORDER BY date DESC",
                (student_id,),
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_total_collected(self) -> float:
        """Return the total fees collected across all students."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM fees")
            return float(cursor.fetchone()[0])
        finally:
            cursor.close()
            conn.close()
