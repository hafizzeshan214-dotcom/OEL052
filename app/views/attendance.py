"""
attendance.py - Attendance management view.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from app.services.attendance_service import AttendanceService, VALID_STATUSES
from app.services.student_service import StudentService
from app.utils.styles import COLORS, FONTS, PAD, make_button
from app.utils.logger import get_logger

logger = get_logger(__name__)


class AttendanceView:
    """Interface for marking and viewing attendance records."""

    def __init__(self, parent: tk.Frame):
        self._att_svc = AttendanceService()
        self._stu_svc = StudentService()
        self._parent  = parent
        self._students = []     # [(id, name), ...]
        self._build_ui()
        self._load_students_dropdown()
        self._load_attendance()

    def _build_ui(self) -> None:
        p = self._parent

        hdr = tk.Frame(p, bg=COLORS["bg_dark"])
        hdr.pack(fill="x", pady=(0, PAD["md"]))
        tk.Label(hdr, text="📋  Attendance Management",
                 font=FONTS["title"], bg=COLORS["bg_dark"],
                 fg=COLORS["text_primary"]).pack(side="left")

        # ── Form card ─────────────────────────────────────────────────────────
        form_card = tk.Frame(p, bg=COLORS["bg_card"],
                             padx=PAD["lg"], pady=PAD["md"])
        form_card.pack(fill="x", pady=(0, PAD["md"]))

        tk.Label(form_card, text="Mark Attendance",
                 font=FONTS["subhead"], bg=COLORS["bg_card"],
                 fg=COLORS["accent"]).grid(row=0, column=0, columnspan=6,
                                           sticky="w", pady=(0, PAD["sm"]))

        # Student dropdown
        tk.Label(form_card, text="Student:", font=FONTS["body"],
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"],
                 ).grid(row=1, column=0, sticky="e", padx=(PAD["sm"], 4))
        self._student_var = tk.StringVar()
        self._student_cb  = ttk.Combobox(form_card, textvariable=self._student_var,
                                          width=28, state="readonly",
                                          font=FONTS["body"])
        self._student_cb.grid(row=1, column=1, sticky="ew", padx=(0, PAD["sm"]))

        # Date field (defaults to today)
        tk.Label(form_card, text="Date (YYYY-MM-DD):", font=FONTS["body"],
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"],
                 ).grid(row=1, column=2, sticky="e", padx=(PAD["sm"], 4))
        self._date_var = tk.StringVar(value=date.today().isoformat())
        tk.Entry(form_card, textvariable=self._date_var,
                 bg=COLORS["bg_light"], fg=COLORS["text_primary"],
                 insertbackground=COLORS["text_primary"],
                 relief="flat", bd=6, font=FONTS["body"],
                 width=16,
                 ).grid(row=1, column=3, sticky="ew", padx=(0, PAD["sm"]))

        # Status dropdown
        tk.Label(form_card, text="Status:", font=FONTS["body"],
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"],
                 ).grid(row=1, column=4, sticky="e", padx=(PAD["sm"], 4))
        self._status_var = tk.StringVar(value="Present")
        status_cb = ttk.Combobox(form_card, textvariable=self._status_var,
                                  values=sorted(VALID_STATUSES),
                                  state="readonly", width=12, font=FONTS["body"])
        status_cb.grid(row=1, column=5, sticky="ew", padx=(0, PAD["sm"]))

        form_card.columnconfigure(1, weight=3)
        form_card.columnconfigure(3, weight=2)

        # Button
        btn_row = tk.Frame(form_card, bg=COLORS["bg_card"])
        btn_row.grid(row=2, column=0, columnspan=6, pady=(PAD["sm"], 0), sticky="w")
        make_button(btn_row, "✅  Mark Attendance", self._mark, width=20).pack(
            side="left", padx=(0, PAD["sm"]))
        make_button(btn_row, "🔄  Refresh", self._load_attendance, width=12,
                    bg=COLORS["bg_light"]).pack(side="left")

        # ── Table ─────────────────────────────────────────────────────────────
        tbl_frame = tk.Frame(p, bg=COLORS["bg_dark"])
        tbl_frame.pack(fill="both", expand=True)

        cols = ("ID", "Student Name", "Date", "Status")
        self._tree = ttk.Treeview(tbl_frame, columns=cols,
                                  show="headings", selectmode="browse")
        for col in cols:
            self._tree.heading(col, text=col)
        self._tree.column("ID",           width=60,  anchor="center")
        self._tree.column("Student Name", width=260, anchor="w")
        self._tree.column("Date",         width=130, anchor="center")
        self._tree.column("Status",       width=100, anchor="center")

        vsb = ttk.Scrollbar(tbl_frame, orient="vertical",
                            command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self._tree.pack(fill="both", expand=True)

        self._status_bar = tk.StringVar(value="Ready")
        tk.Label(p, textvariable=self._status_bar, font=FONTS["small"],
                 bg=COLORS["bg_dark"], fg=COLORS["text_muted"],
                 anchor="w").pack(fill="x", pady=(4, 0))

    def _load_students_dropdown(self) -> None:
        self._students = self._stu_svc.get_all_students()
        names = [f"{s.id} — {s.name}" for s in self._students]
        self._student_cb["values"] = names
        if names:
            self._student_cb.current(0)

    def _load_attendance(self) -> None:
        for item in self._tree.get_children():
            self._tree.delete(item)
        records = self._att_svc.get_all_attendance()
        status_colors = {
            "Present": "#27ae60",
            "Absent":  "#e74c3c",
            "Late":    "#f39c12",
        }
        for idx, row in enumerate(records):
            status = row[3]
            tag = status.lower()
            self._tree.insert("", "end", values=row, tags=(tag,))
        self._tree.tag_configure("present", foreground=status_colors["Present"])
        self._tree.tag_configure("absent",  foreground=status_colors["Absent"])
        self._tree.tag_configure("late",    foreground=status_colors["Late"])
        self._status_bar.set(f"{len(records)} attendance record(s).")

    def _mark(self) -> None:
        sel_str = self._student_var.get()
        if not sel_str:
            messagebox.showwarning("No Student", "Please select a student.")
            return
        try:
            student_id = int(sel_str.split("—")[0].strip())
            self._att_svc.mark_attendance(
                student_id,
                self._date_var.get(),
                self._status_var.get(),
            )
            messagebox.showinfo("Success", "Attendance marked successfully!")
            self._load_attendance()
        except ValueError as e:
            messagebox.showwarning("Validation Error", str(e))
        except Exception as e:
            logger.exception("Error marking attendance")
            messagebox.showerror("Error", str(e))
