"""
db.py - Database connection and initialization for School Management System.
Uses MySQL via mysql-connector-python.
"""
import mysql.connector
from mysql.connector import Error
from app.utils.logger import get_logger

logger = get_logger(__name__)

# ── Database configuration ────────────────────────────────────────────────────
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "school_db",
}


def get_connection():
    """
    Create and return a live MySQL connection.

    Returns:
        mysql.connector.connection.MySQLConnection

    Raises:
        ConnectionError: If the database cannot be reached.
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            logger.debug("Database connection established.")
            return conn
    except Error as exc:
        logger.error("Database connection failed: %s", exc)
        raise ConnectionError(f"Cannot connect to database: {exc}") from exc


def initialize_database() -> None:
    """
    Create the school_db database, all required tables, and insert sample data
    if the tables are empty.  Safe to call multiple times (idempotent).
    """
    try:
        # Connect without specifying a database so we can CREATE it
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
        )
        cursor = conn.cursor()

        # ── Database ──────────────────────────────────────────────────────────
        cursor.execute("CREATE DATABASE IF NOT EXISTS school_db")
        cursor.execute("USE school_db")

        # ── Tables ────────────────────────────────────────────────────────────
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id       INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id    INT AUTO_INCREMENT PRIMARY KEY,
                name  VARCHAR(150) NOT NULL,
                class VARCHAR(50)  NOT NULL,
                age   INT          NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS teachers (
                id      INT AUTO_INCREMENT PRIMARY KEY,
                name    VARCHAR(150) NOT NULL,
                subject VARCHAR(100) NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id         INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT         NOT NULL,
                date       DATE        NOT NULL,
                status     VARCHAR(20) NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fees (
                id         INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT           NOT NULL,
                amount     DECIMAL(10,2) NOT NULL,
                date       DATE          NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
            )
        """)

        # ── Sample data ───────────────────────────────────────────────────────
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                ("admin", "admin123"),
            )

        cursor.execute("SELECT COUNT(*) FROM students")
        if cursor.fetchone()[0] == 0:
            sample_students = [
                ("Ali Hassan",     "10-A", 15),
                ("Sara Khan",      "9-B",  14),
                ("Usman Ahmed",    "11-C", 16),
                ("Fatima Malik",   "8-A",  13),
                ("Bilal Raza",     "12-B", 17),
                ("Hina Tariq",     "9-A",  14),
                ("Zaid Iqbal",     "10-B", 15),
                ("Maira Shahid",   "11-A", 16),
            ]
            cursor.executemany(
                "INSERT INTO students (name, class, age) VALUES (%s, %s, %s)",
                sample_students,
            )

        cursor.execute("SELECT COUNT(*) FROM teachers")
        if cursor.fetchone()[0] == 0:
            sample_teachers = [
                ("Mr. Tariq Ahmed",     "Mathematics"),
                ("Ms. Ayesha Siddiqui", "English"),
                ("Mr. Zubair Hussain",  "Physics"),
                ("Ms. Nadia Akhtar",    "Chemistry"),
                ("Mr. Kamran Ali",      "Computer Science"),
                ("Ms. Sana Javed",      "Biology"),
            ]
            cursor.executemany(
                "INSERT INTO teachers (name, subject) VALUES (%s, %s)",
                sample_teachers,
            )

        cursor.execute("SELECT COUNT(*) FROM attendance")
        if cursor.fetchone()[0] == 0:
            sample_attendance = [
                (1, "2024-01-15", "Present"),
                (2, "2024-01-15", "Absent"),
                (3, "2024-01-15", "Present"),
                (4, "2024-01-15", "Present"),
                (5, "2024-01-15", "Late"),
                (1, "2024-01-16", "Present"),
                (2, "2024-01-16", "Present"),
                (3, "2024-01-16", "Absent"),
            ]
            cursor.executemany(
                "INSERT INTO attendance (student_id, date, status) VALUES (%s, %s, %s)",
                sample_attendance,
            )

        cursor.execute("SELECT COUNT(*) FROM fees")
        if cursor.fetchone()[0] == 0:
            sample_fees = [
                (1, 5000.00, "2024-01-10"),
                (2, 4500.00, "2024-01-12"),
                (3, 5500.00, "2024-01-08"),
                (4, 4000.00, "2024-01-15"),
                (5, 6000.00, "2024-01-05"),
                (6, 4800.00, "2024-01-18"),
                (7, 5200.00, "2024-01-20"),
                (8, 4700.00, "2024-01-22"),
            ]
            cursor.executemany(
                "INSERT INTO fees (student_id, amount, date) VALUES (%s, %s, %s)",
                sample_fees,
            )

        conn.commit()
        cursor.close()
        conn.close()
        logger.info("Database initialized successfully with sample data.")

    except Error as exc:
        logger.error("Database initialization error: %s", exc)
        raise
