"""
test_student.py - Unit tests for StudentService CRUD operations.

Run with:  pytest tests/test_student.py -v
"""
import pytest
from unittest.mock import patch, MagicMock, call
from app.services.student_service import StudentService
from app.models.student_model import Student


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def svc():
    return StudentService()


SAMPLE_ROWS = [
    (1, "Ali Hassan",   "10-A", 15),
    (2, "Sara Khan",    "9-B",  14),
    (3, "Usman Ahmed",  "11-C", 16),
]


# ── Validation tests ──────────────────────────────────────────────────────────

class TestValidation:

    def test_empty_name_raises(self, svc):
        with pytest.raises(ValueError, match="name"):
            svc.add_student("", "10-A", "15")

    def test_whitespace_name_raises(self, svc):
        with pytest.raises(ValueError, match="name"):
            svc.add_student("   ", "10-A", "15")

    def test_empty_class_raises(self, svc):
        with pytest.raises(ValueError, match="[Cc]lass"):
            svc.add_student("John Doe", "", "15")

    def test_non_numeric_age_raises(self, svc):
        with pytest.raises(ValueError, match="[Aa]ge"):
            svc.add_student("John Doe", "10-A", "abc")

    def test_negative_age_raises(self, svc):
        with pytest.raises(ValueError, match="[Aa]ge"):
            svc.add_student("John Doe", "10-A", "-5")

    def test_zero_age_raises(self, svc):
        with pytest.raises(ValueError, match="[Aa]ge"):
            svc.add_student("John Doe", "10-A", "0")

    def test_age_over_100_raises(self, svc):
        with pytest.raises(ValueError, match="[Aa]ge"):
            svc.add_student("John Doe", "10-A", "101")

    def test_valid_data_returns_age(self, svc):
        age = svc._validate("John Doe", "10-A", "15")
        assert age == 15


# ── CRUD tests ────────────────────────────────────────────────────────────────

class TestAddStudent:

    @patch("app.services.student_service.get_connection")
    def test_add_student_executes_insert(self, mock_conn, svc):
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor

        svc.add_student("John Doe", "10-A", "15")

        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args[0]
        assert "INSERT" in call_args[0]

    @patch("app.services.student_service.get_connection")
    def test_add_student_commits(self, mock_conn, svc):
        mock_cursor = MagicMock()
        conn_instance = mock_conn.return_value
        conn_instance.cursor.return_value = mock_cursor

        svc.add_student("Jane Doe", "9-B", "14")
        conn_instance.commit.assert_called_once()


class TestGetAllStudents:

    @patch("app.services.student_service.get_connection")
    def test_returns_list_of_students(self, mock_conn, svc):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = SAMPLE_ROWS
        mock_conn.return_value.cursor.return_value = mock_cursor

        result = svc.get_all_students()

        assert len(result) == 3
        assert all(isinstance(s, Student) for s in result)

    @patch("app.services.student_service.get_connection")
    def test_empty_table_returns_empty_list(self, mock_conn, svc):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_conn.return_value.cursor.return_value = mock_cursor

        result = svc.get_all_students()
        assert result == []

    @patch("app.services.student_service.get_connection")
    def test_student_fields_mapped_correctly(self, mock_conn, svc):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [(7, "Bilal Raza", "12-B", 17)]
        mock_conn.return_value.cursor.return_value = mock_cursor

        students = svc.get_all_students()
        s = students[0]
        assert s.id == 7
        assert s.name == "Bilal Raza"
        assert s.class_name == "12-B"
        assert s.age == 17


class TestUpdateStudent:

    @patch("app.services.student_service.get_connection")
    def test_update_executes_update_query(self, mock_conn, svc):
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor

        svc.update_student(1, "Ali Hassan", "10-A", "16")

        call_args = mock_cursor.execute.call_args[0]
        assert "UPDATE" in call_args[0]

    def test_update_with_invalid_age_raises(self, svc):
        with pytest.raises(ValueError):
            svc.update_student(1, "Ali Hassan", "10-A", "xyz")


class TestDeleteStudent:

    @patch("app.services.student_service.get_connection")
    def test_delete_executes_delete_query(self, mock_conn, svc):
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor

        svc.delete_student(1)

        call_args = mock_cursor.execute.call_args[0]
        assert "DELETE" in call_args[0]

    @patch("app.services.student_service.get_connection")
    def test_delete_passes_correct_id(self, mock_conn, svc):
        mock_cursor = MagicMock()
        mock_conn.return_value.cursor.return_value = mock_cursor

        svc.delete_student(42)
        call_args = mock_cursor.execute.call_args[0]
        assert 42 in call_args[1]


class TestStudentModel:
    """Unit tests for the Student dataclass."""

    def test_from_row(self):
        row = (3, "Fatima Malik", "8-A", 13)
        s = Student.from_row(row)
        assert s.id == 3
        assert s.name == "Fatima Malik"
        assert s.class_name == "8-A"
        assert s.age == 13

    def test_repr_contains_name(self):
        s = Student(id=1, name="Test Student", class_name="10-A", age=15)
        assert "Test Student" in repr(s)
