"""
main.py - Application entry point.
Initialises the database, then launches the login window.
"""
import sys
from app.utils.logger import get_logger
from app.utils.db import initialize_database

logger = get_logger(__name__)


def launch_dashboard(user) -> None:
    """Open the dashboard window after successful login."""
    from app.views.dashboard import DashboardView
    DashboardView(user).run()


def main() -> None:
    """Bootstrap the School Management System."""
    logger.info("=== School Management System starting ===")

    # Initialise DB (creates tables + sample data if needed)
    try:
        initialize_database()
    except Exception as exc:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Database Error",
            f"Could not connect to MySQL:\n\n{exc}\n\n"
            "Please check db.py and ensure MySQL is running.",
        )
        root.destroy()
        logger.critical("Startup aborted — database unavailable: %s", exc)
        sys.exit(1)

    from app.views.login import LoginView
    LoginView(launch_dashboard).run()
    logger.info("=== School Management System exited ===")


if __name__ == "__main__":
    main()
