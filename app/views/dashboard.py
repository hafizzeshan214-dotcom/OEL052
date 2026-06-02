"""
dashboard.py - Main dashboard window with sidebar navigation.
"""
import tkinter as tk
from tkinter import messagebox
from app.utils.styles import COLORS, FONTS, PAD, add_hover
from app.utils.logger import get_logger
from app.models.user_model import User

logger = get_logger(__name__)


class DashboardView:
    """
    Main application window.  Contains a fixed sidebar and a content frame
    that swaps modules (students, teachers, attendance, fees, reports) on demand.
    """

    def __init__(self, user: User):
        self._user = user
        self._root = tk.Tk()
        self._active_btn = None
        self._content_frame = None
        self._build_ui()

    # ── Public ────────────────────────────────────────────────────────────────
    def run(self) -> None:
        self._root.mainloop()

    def show_module(self, module_name: str) -> None:
        """Clear the content area and load the requested module."""
        for widget in self._content_frame.winfo_children():
            widget.destroy()

        match module_name:
            case "students":
                from app.views.student import StudentView
                StudentView(self._content_frame)
            case "teachers":
                from app.views.teacher import TeacherView
                TeacherView(self._content_frame)
            case "attendance":
                from app.views.attendance import AttendanceView
                AttendanceView(self._content_frame)
            case "fees":
                from app.views.fees import FeesView
                FeesView(self._content_frame)
            case "reports":
                from app.views.reports import ReportsView
                ReportsView(self._content_frame)
            case _:
                self._show_home()

    # ── Private builders ──────────────────────────────────────────────────────
    def _build_ui(self) -> None:
        root = self._root
        root.title("School Management System")
        root.geometry("1100x680")
        root.resizable(True, True)
        root.configure(bg=COLORS["bg_dark"])
        root.eval("tk::PlaceWindow . center")

        # ── Outer layout ──────────────────────────────────────────────────────
        main = tk.Frame(root, bg=COLORS["bg_dark"])
        main.pack(fill="both", expand=True)

        # Sidebar
        sidebar = tk.Frame(main, bg=COLORS["sidebar_bg"], width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        self._build_sidebar(sidebar)

        # Content wrapper
        right = tk.Frame(main, bg=COLORS["bg_dark"])
        right.pack(side="left", fill="both", expand=True)

        self._build_topbar(right)

        self._content_frame = tk.Frame(right, bg=COLORS["bg_dark"])
        self._content_frame.pack(fill="both", expand=True,
                                 padx=PAD["lg"], pady=PAD["md"])

        self._show_home()

    def _build_sidebar(self, parent: tk.Frame) -> None:
        # Brand
        brand = tk.Frame(parent, bg=COLORS["sidebar_bg"], pady=PAD["xl"])
        brand.pack(fill="x")
        tk.Label(brand, text="🎓", font=("Segoe UI Emoji", 30),
                 bg=COLORS["sidebar_bg"], fg="white").pack()
        tk.Label(brand, text="School MS",
                 font=FONTS["heading"], bg=COLORS["sidebar_bg"],
                 fg=COLORS["text_primary"]).pack()
        tk.Label(brand, text="Management System",
                 font=FONTS["small"], bg=COLORS["sidebar_bg"],
                 fg=COLORS["text_muted"]).pack()

        # Divider
        tk.Frame(parent, bg=COLORS["border"], height=1).pack(fill="x", pady=8)

        # Navigation items
        nav_items = [
            ("🏠  Home",          "home"),
            ("👨‍🎓  Students",      "students"),
            ("👩‍🏫  Teachers",      "teachers"),
            ("📋  Attendance",    "attendance"),
            ("💰  Fees",          "fees"),
            ("📊  Reports",       "reports"),
        ]

        self._nav_buttons = {}
        for label, key in nav_items:
            btn = tk.Button(
                parent, text=label,
                command=lambda k=key: self._nav_click(k),
                bg=COLORS["sidebar_bg"], fg=COLORS["text_secondary"],
                font=FONTS["body"], relief="flat", bd=0,
                anchor="w", padx=PAD["lg"], pady=PAD["sm"],
                cursor="hand2",
                activebackground=COLORS["sidebar_hover"],
                activeforeground=COLORS["text_primary"],
                width=22,
            )
            btn.pack(fill="x")
            add_hover(btn, COLORS["sidebar_bg"], COLORS["sidebar_hover"],
                      COLORS["text_secondary"], COLORS["text_primary"])
            self._nav_buttons[key] = btn

        # Logout at bottom
        tk.Frame(parent, bg=COLORS["border"], height=1).pack(
            fill="x", pady=8, side="bottom")
        logout_btn = tk.Button(
            parent, text="🚪  Logout",
            command=self._logout,
            bg=COLORS["sidebar_bg"], fg=COLORS["danger"],
            font=FONTS["body"], relief="flat", bd=0,
            anchor="w", padx=PAD["lg"], pady=PAD["sm"],
            cursor="hand2", side="bottom", width=22,
        )
        logout_btn.pack(fill="x", side="bottom")

    def _build_topbar(self, parent: tk.Frame) -> None:
        topbar = tk.Frame(parent, bg=COLORS["bg_medium"], height=56, pady=0)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        tk.Label(topbar, text="School Management System",
                 font=FONTS["heading"], bg=COLORS["bg_medium"],
                 fg=COLORS["text_primary"]).pack(side="left",
                                                  padx=PAD["lg"])

        user_lbl = tk.Label(
            topbar,
            text=f"👤  {self._user.username}",
            font=FONTS["body"], bg=COLORS["bg_medium"],
            fg=COLORS["accent"],
        )
        user_lbl.pack(side="right", padx=PAD["lg"])

    def _nav_click(self, key: str) -> None:
        # Reset previously highlighted button
        if self._active_btn:
            self._active_btn.config(bg=COLORS["sidebar_bg"],
                                    fg=COLORS["text_secondary"])
        btn = self._nav_buttons[key]
        btn.config(bg=COLORS["sidebar_selected"], fg="white")
        self._active_btn = btn
        self.show_module(key)

    def _show_home(self) -> None:
        """Render the home/welcome panel."""
        f = self._content_frame
        # Welcome
        tk.Label(f, text=f"Welcome back, {self._user.username}! 👋",
                 font=FONTS["title"], bg=COLORS["bg_dark"],
                 fg=COLORS["text_primary"]).pack(pady=(PAD["xl"], PAD["sm"]),
                                                  anchor="w")
        tk.Label(f, text="Use the sidebar to navigate between modules.",
                 font=FONTS["body"], bg=COLORS["bg_dark"],
                 fg=COLORS["text_muted"]).pack(anchor="w")

        # Quick-access cards
        card_row = tk.Frame(f, bg=COLORS["bg_dark"])
        card_row.pack(fill="x", pady=PAD["xl"])

        quick_items = [
            ("👨‍🎓", "Students",   COLORS["accent"],   "students"),
            ("👩‍🏫", "Teachers",   COLORS["success"],  "teachers"),
            ("📋", "Attendance", COLORS["warning"],   "attendance"),
            ("💰", "Fees",       COLORS["info"],      "fees"),
            ("📊", "Reports",    "#8e44ad",           "reports"),
        ]
        for icon, label, color, key in quick_items:
            card = tk.Frame(card_row, bg=COLORS["bg_card"],
                            padx=20, pady=20, cursor="hand2")
            card.pack(side="left", padx=PAD["sm"], fill="both", expand=True)
            tk.Label(card, text=icon, font=("Segoe UI Emoji", 26),
                     bg=COLORS["bg_card"], fg=color).pack()
            tk.Label(card, text=label, font=FONTS["subhead"],
                     bg=COLORS["bg_card"], fg=COLORS["text_primary"]).pack()
            card.bind("<Button-1>", lambda _, k=key: self._nav_click(k))
            for child in card.winfo_children():
                child.bind("<Button-1>", lambda _, k=key: self._nav_click(k))

    def _logout(self) -> None:
        if messagebox.askyesno("Logout", "Are you sure you want to logout?",
                               parent=self._root):
            logger.info("User '%s' logged out.", self._user.username)
            self._root.destroy()
            # Restart login
            from app.views.login import LoginView
            from app.main import launch_dashboard
            LoginView(launch_dashboard).run()
