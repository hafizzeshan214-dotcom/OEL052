"""
login.py - Login window view for School Management System.
"""
import tkinter as tk
from tkinter import messagebox
from app.services.auth_service import AuthService
from app.utils.styles import (
    COLORS, FONTS, PAD,
    apply_global_style, make_button, make_label, make_entry, make_frame, add_hover,
)
from app.utils.logger import get_logger

logger = get_logger(__name__)


class LoginView:
    """Renders the animated login window and delegates auth to AuthService."""

    def __init__(self, on_login_success):
        """
        Args:
            on_login_success: Callback(user) invoked after successful login.
        """
        self._auth = AuthService()
        self._on_success = on_login_success
        self._root = tk.Tk()
        self._build_ui()

    # ── Public ────────────────────────────────────────────────────────────────
    def run(self) -> None:
        self._root.mainloop()

    # ── Private ───────────────────────────────────────────────────────────────
    def _build_ui(self) -> None:
        root = self._root
        root.title("School Management System — Login")
        root.geometry("480x560")
        root.resizable(False, False)
        root.configure(bg=COLORS["bg_dark"])
        apply_global_style(root)
        root.eval("tk::PlaceWindow . center")

        # ── Background canvas gradient (simulated) ────────────────────────────
        canvas = tk.Canvas(root, width=480, height=560,
                           bg=COLORS["bg_dark"], highlightthickness=0)
        canvas.place(x=0, y=0)

        # Decorative circles
        canvas.create_oval(-60, -60, 160, 160,
                           fill=COLORS["bg_medium"], outline="")
        canvas.create_oval(320, 380, 540, 620,
                           fill=COLORS["bg_medium"], outline="")

        # ── Card ──────────────────────────────────────────────────────────────
        card = tk.Frame(root, bg=COLORS["bg_card"],
                        bd=0, relief="flat",
                        padx=40, pady=40)
        card.place(relx=0.5, rely=0.5, anchor="center", width=380, height=430)

        # Logo / icon area
        icon_frame = tk.Frame(card, bg=COLORS["accent"],
                              width=70, height=70)
        icon_frame.pack(pady=(0, PAD["sm"]))
        icon_frame.pack_propagate(False)
        tk.Label(icon_frame, text="🎓", font=("Segoe UI Emoji", 32),
                 bg=COLORS["accent"], fg="white").pack(expand=True)

        # Title
        tk.Label(card, text="School Management",
                 font=FONTS["title"], bg=COLORS["bg_card"],
                 fg=COLORS["text_primary"]).pack()
        tk.Label(card, text="System",
                 font=FONTS["heading"], bg=COLORS["bg_card"],
                 fg=COLORS["accent"]).pack()
        tk.Label(card, text="Sign in to continue",
                 font=FONTS["small"], bg=COLORS["bg_card"],
                 fg=COLORS["text_muted"]).pack(pady=(4, PAD["lg"]))

        # ── Fields ────────────────────────────────────────────────────────────
        tk.Label(card, text="USERNAME", font=("Segoe UI", 9, "bold"),
                 bg=COLORS["bg_card"], fg=COLORS["text_muted"]).pack(anchor="w")
        self._username_var = tk.StringVar()
        u_entry = tk.Entry(card, textvariable=self._username_var,
                           bg=COLORS["bg_light"], fg=COLORS["text_primary"],
                           insertbackground=COLORS["text_primary"],
                           relief="flat", bd=8, font=FONTS["body"],
                           width=30)
        u_entry.pack(fill="x", pady=(2, PAD["sm"]))

        tk.Label(card, text="PASSWORD", font=("Segoe UI", 9, "bold"),
                 bg=COLORS["bg_card"], fg=COLORS["text_muted"]).pack(anchor="w")
        self._password_var = tk.StringVar()
        p_entry = tk.Entry(card, textvariable=self._password_var, show="●",
                           bg=COLORS["bg_light"], fg=COLORS["text_primary"],
                           insertbackground=COLORS["text_primary"],
                           relief="flat", bd=8, font=FONTS["body"],
                           width=30)
        p_entry.pack(fill="x", pady=(2, PAD["md"]))

        # ── Login button ──────────────────────────────────────────────────────
        login_btn = tk.Button(
            card, text="  LOGIN  →",
            command=self._handle_login,
            bg=COLORS["accent"], fg="white",
            font=("Segoe UI", 12, "bold"),
            relief="flat", bd=0,
            padx=PAD["md"], pady=PAD["sm"],
            cursor="hand2",
            activebackground=COLORS["accent_hover"],
            activeforeground="white",
        )
        login_btn.pack(fill="x", pady=(4, 0))
        add_hover(login_btn, COLORS["accent"], COLORS["accent_hover"])

        # Hint
        tk.Label(card, text="Default: admin / admin123",
                 font=FONTS["small"], bg=COLORS["bg_card"],
                 fg=COLORS["text_muted"]).pack(pady=(PAD["sm"], 0))

        # Bind Enter key
        root.bind("<Return>", lambda _: self._handle_login())
        u_entry.focus_set()

    def _handle_login(self) -> None:
        username = self._username_var.get()
        password = self._password_var.get()
        try:
            user = self._auth.login(username, password)
            self._root.destroy()
            self._on_success(user)
        except ValueError as exc:
            messagebox.showerror("Login Failed", str(exc), parent=self._root)
        except ConnectionError as exc:
            messagebox.showerror("Database Error", str(exc), parent=self._root)
        except Exception as exc:
            logger.exception("Unexpected login error")
            messagebox.showerror("Error", f"An unexpected error occurred:\n{exc}",
                                 parent=self._root)
