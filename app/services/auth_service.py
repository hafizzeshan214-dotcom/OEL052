"""
auth_service.py - Authentication business logic.
"""
from app.utils.db import get_connection
from app.utils.logger import get_logger
from app.models.user_model import User

logger = get_logger(__name__)


class AuthService:
    """Handles user authentication operations."""

    def login(self, username: str, password: str) -> User:
        """
        Validate credentials against the database.

        Args:
            username: Plain-text username.
            password: Plain-text password.

        Returns:
            User: Authenticated user object.

        Raises:
            ValueError: If credentials are invalid or inputs are empty.
            ConnectionError: If the database is unreachable.
        """
        username = username.strip()
        password = password.strip()

        if not username or not password:
            raise ValueError("Username and password cannot be empty.")

        logger.info("Login attempt for user: '%s'", username)

        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, password FROM users "
                "WHERE username = %s AND password = %s",
                (username, password),
            )
            row = cursor.fetchone()
            if row is None:
                logger.warning("Failed login attempt for user: '%s'", username)
                raise ValueError("Invalid username or password.")
            user = User.from_row(row)
            logger.info("User '%s' logged in successfully.", username)
            return user
        finally:
            cursor.close()
            conn.close()
