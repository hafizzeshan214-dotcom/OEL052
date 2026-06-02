"""
reports.py - Reports / analytics dashboard view.
"""
import tkinter as tk
from tkinter import ttk
from app.services.student_service import StudentService
from app.services.teacher_service import TeacherService
from app.services.fee_service import FeeService
from app.services.attendance_service import AttendanceService
from app.utils.styles import COLORS, FONTS, PAD
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ReportsView:
    """Dashboard showing key school statistics at a glance."""

    def __init__(self, parent: tk.Frame):
        self._stu_svc = StudentService()
        self._tch_svc = TeacherService()
        self._fee_svc = FeeService()
        self._att_svc = AttendanceService()
        self._parent  = parent
        self._build_ui()
        self._refresh()

    def _build_ui(self) -> None:
        p = self._parent

        hdr = tk.Frame(p, bg=COLORS["bg_dark"])
        hdr.pack(fill="x", pady=(0, PAD["md"]))
        tk.Label(hdr, text="📊  Reports & Analytics",
                 font=FONTS["title"], bg=COLORS["bg_dark"],
                 fg=COLORS["text_primary"]).pack(side="left")

        refresh_btn = tk.Button(
            hdr, text="🔄  Refresh",
            command=self._refresh,
            bg=COLORS["bg_light"], fg=COLORS["text_primary"],
            font=FONTS["button"], relief="flat", bd=0,
            padx=PAD["sm"], pady=PAD["xs"], cursor="hand2",
        )
        refresh_btn.pack(side="right")

        # ── Stat cards row ────────────────────────────────────────────────────
        self._cards_frame = tk.Frame(p, bg=COLORS["bg_dark"])
        self._cards_frame.pack(fill="x", pady=(0, PAD["lg"]))

        # Placeholders — values filled in _refresh()
        self._stat_vars = {}
        stats_cfg = [
            ("👨‍🎓", "Total Students",       "students",   COLORS["accent"]),
            ("👩‍🏫", "Total Teachers",       "teachers",   COLORS["success"]),
            ("💰", "Fees Collected (PKR)", "fees",       COLORS["warning"]),
            ("✅", "Present Today",        "present",    COLORS["info"]),
            ("❌", "Absent Today",         "absent",     COLORS["danger"]),
        ]
        for icon, title, key, color in stats_cfg:
            card = tk.Frame(self._cards_frame, bg=COLORS["bg_card"],
                            padx=PAD["lg"], pady=PAD["lg"])
            card.pack(side="left", fill="both", expand=True, padx=PAD["xs"])

            # Colour bar on top
            tk.Frame(card, bg=color, height=4).pack(fill="x", pady=(0, PAD["sm"]))

            tk.Label(card, text=icon, font=("Segoe UI Emoji", 24),
                     bg=COLORS["bg_card"], fg=color).pack()
            var = tk.StringVar(value="—")
            self._stat_vars[key] = var
            tk.Label(card, textvariable=var,
                     font=("Segoe UI", 22, "bold"),
                     bg=COLORS["bg_card"], fg=color).pack(pady=(4, 2))
            tk.Label(card, text=title, font=FONTS["small"],
                     bg=COLORS["bg_card"], fg=COLORS["text_muted"]).pack()

        # ── Recent fees table ─────────────────────────────────────────────────
        tk.Label(p, text="Recent Fee Payments",
                 font=FONTS["subhead"], bg=COLORS["bg_dark"],
                 fg=COLORS["text_secondary"]).pack(anchor="w",
                                                   pady=(0, PAD["xs"]))

        fees_frame = tk.Frame(p, bg=COLORS["bg_dark"])
        fees_frame.pack(fill="both", expand=True)

        cols = ("ID", "Student Name", "Amount (PKR)", "Date")
        self._fees_tree = ttk.Treeview(fees_frame, columns=cols,
                                       show="headings", height=7)
        for col in cols:
            self._fees_tree.heading(col, text=col)
        self._fees_tree.column("ID",           width=60,  anchor="center")
        self._fees_tree.column("Student Name", width=240, anchor="w")
        self._fees_tree.column("Amount (PKR)", width=130, anchor="e")
        self._fees_tree.column("Date",         width=120, anchor="center")

        vsb = ttk.Scrollbar(fees_frame, orient="vertical",
                            command=self._fees_tree.yview)
        self._fees_tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self._fees_tree.pack(fill="both", expand=True)

        # ── Recent attendance table ───────────────────────────────────────────
        tk.Label(p, text="Recent Attendance Records",
                 font=FONTS["subhead"], bg=COLORS["bg_dark"],
                 fg=COLORS["text_secondary"]).pack(anchor="w",
                                                   pady=(PAD["sm"], PAD["xs"]))

        att_frame = tk.Frame(p, bg=COLORS["bg_dark"])
        att_frame.pack(fill="both", expand=True)

        att_cols = ("ID", "Student Name", "Date", "Status")
        self._att_tree = ttk.Treeview(att_frame, columns=att_cols,
                                      show="headings", height=6)
        for col in att_cols:
            self._att_tree.heading(col, text=col)
        self._att_tree.column("ID",           width=60,  anchor="center")
        self._att_tree.column("Student Name", width=240, anchor="w")
        self._att_tree.column("Date",         width=120, anchor="center")
        self._att_tree.column("Status",       width=100, anchor="center")

        vsb2 = ttk.Scrollbar(att_frame, orient="vertical",
                             command=self._att_tree.yview)
        self._att_tree.configure(yscrollcommand=vsb2.set)
        vsb2.pack(side="right", fill="y")
        self._att_tree.pack(fill="both", expand=True)

    def _refresh(self) -> None:
        """Reload all statistics and tables."""
        try:
            # ── Stats ──────────────────────────────────────────────────────────
            self._stat_vars["students"].set(str(self._stu_svc.get_total_count()))
            self._stat_vars["teachers"].set(str(self._tch_svc.get_total_count()))
            total_fees = self._fee_svc.get_total_collected()
            self._stat_vars["fees"].set(f"{total_fees:,.0f}")

            today_summary = self._att_svc.get_today_summary()
            self._stat_vars["present"].set(str(today_summary.get("Present", 0)))
            self._stat_vars["absent"].set(str(today_summary.get("Absent", 0)))

            # ── Fees table ─────────────────────────────────────────────────────
            for item in self._fees_tree.get_children():
                self._fees_tree.delete(item)
            for idx, row in enumerate(self._fee_svc.get_all_fees()[:15]):
                fmt = (row[0], row[1], f"{float(row[2]):,.2f}", str(row[3]))
                tag = "odd" if idx % 2 else "even"
                self._fees_tree.insert("", "end", values=fmt, tags=(tag,))
            self._fees_tree.tag_configure("odd",  background=COLORS["bg_row_alt"])
            self._fees_tree.tag_configure("even", background=COLORS["bg_card"])

            # ── Attendance table ───────────────────────────────────────────────
            for item in self._att_tree.get_children():
                self._att_tree.delete(item)
            status_colors = {"Present": "#27ae60", "Absent": "#e74c3c",
                             "Late": "#f39c12"}
            for row in self._att_svc.get_all_attendance()[:15]:
                status = row[3]
                tag = status.lower()
                self._att_tree.insert("", "end", values=row, tags=(tag,))
            self._att_tree.tag_configure("present",
                                         foreground=status_colors["Present"])
            self._att_tree.tag_configure("absent",
                                         foreground=status_colors["Absent"])
            self._att_tree.tag_configure("late",
                                         foreground=status_colors["Late"])

            logger.info("Reports dashboard refreshed.")
        except Exception as exc:
            logger.exception("Error loading reports: %s", exc)
