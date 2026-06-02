"""
test_auth.py - Unit tests for the AuthService (login functionality).

Run with:  pytest tests/test_auth.py -v
"""
import pytest
from unittest.mock import patch, MagicMock
from app.services.auth_service import AuthService
from app.models.user_model import User


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def auth_service():
    return AuthService()


# ── Helper: fake DB row ───────────────────────────────────────────────────────

ADMIN_ROW = (1, "admin", "admin123")


# ── Tests ─────────────────────────────────────────────────────────────────────

class TestLoginValidation:
    """Tests that validate input before touching the database."""

    def test_empty_username_raises(self, auth_service):
        with pytest.raises(ValueError, match="empty"):
            auth_service.login("", "somepassword")

    def test_empty_password_raises(self, auth_service):
        with pytest.raises(ValueError, match="empty"):
            auth_service.login("admin", "")

    def test_whitespace_username_raises(self, auth_service):
        with pytest.raises(ValueError, match="empty"):
            auth_service.login("   ", "somepassword")

    def test_whitespace_password_raises(self, auth_service):
        with pytest.raises(ValueError, match="empty"):
            auth_service.login("admin", "   ")


class TestLoginSuccess:
    """Tests for successful authentication (DB mocked)."""

    @patch("app.services.auth_service.get_connection")
    def test_valid_credentials_return_user(self, mock_conn, auth_service):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ADMIN_ROW
        mock_conn.return_value.__enter__ = MagicMock(return_value=mock_conn.return_value)
        mock_conn.return_value.cursor.return_value = mock_cursor

        user = auth_service.login("admin", "admin123")

        assert isinstance(user, User)
        assert user.username == "admin"
        assert user.id == 1

    @patch("app.services.auth_service.get_connection")
    def test_credentials_are_stripped(self, mock_conn, auth_service):
        """Leading/trailing whitespace should be stripped before query."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ADMIN_ROW
        mock_conn.return_value.cursor.return_value = mock_cursor

        user = auth_service.login("  admin  ", "  admin123  ")
        assert user.username == "admin"


class TestLoginFailure:
    """Tests for failed authentication."""

    @patch("app.services.auth_service.get_connection")
    def test_wrong_password_raises_value_error(self, mock_conn, auth_service):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None  # No matching row
        mock_conn.return_value.cursor.return_value = mock_cursor

        with pytest.raises(ValueError, match="Invalid username or password"):
            auth_service.login("admin", "wrongpass")

    @patch("app.services.auth_service.get_connection")
    def test_nonexistent_user_raises_value_error(self, mock_conn, auth_service):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_conn.return_value.cursor.return_value = mock_cursor

        with pytest.raises(ValueError):
            auth_service.login("nobody", "pass")

    @patch("app.services.auth_service.get_connection")
    def test_db_error_raises_connection_error(self, mock_conn, auth_service):
        mock_conn.side_effect = ConnectionError("DB unreachable")
        with pytest.raises(ConnectionError):
            auth_service.login("admin", "admin123")


class TestUserModel:
    """Unit tests for the User dataclass."""

    def test_from_row_constructs_correctly(self):
        row = (5, "teacher1", "pass999")
        user = User.from_row(row)
        assert user.id == 5
        assert user.username == "teacher1"
        assert user.password == "pass999"

    def test_repr_contains_username(self):
        user = User(id=1, username="admin", password="secret")
        assert "admin" in repr(user)
