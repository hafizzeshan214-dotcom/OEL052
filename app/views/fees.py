"""
fees.py - Fee management view.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from app.services.fee_service import FeeService
from app.services.student_service import StudentService
from app.utils.styles import COLORS, FONTS, PAD, make_button
from app.utils.logger import get_logger

logger = get_logger(__name__)


class FeesView:
    """Interface for recording and viewing fee payments."""

    def __init__(self, parent: tk.Frame):
        self._fee_svc = FeeService()
        self._stu_svc = StudentService()
        self._parent  = parent
        self._students = []
        self._build_ui()
        self._load_students_dropdown()
        self._load_fees()

    def _build_ui(self) -> None:
        p = self._parent

        hdr = tk.Frame(p, bg=COLORS["bg_dark"])
        hdr.pack(fill="x", pady=(0, PAD["md"]))
        tk.Label(hdr, text="💰  Fee Management",
                 font=FONTS["title"], bg=COLORS["bg_dark"],
                 fg=COLORS["text_primary"]).pack(side="left")

        # Summary strip
        self._total_var = tk.StringVar(value="Total Collected: PKR 0.00")
        tk.Label(hdr, textvariable=self._total_var,
                 font=FONTS["subhead"], bg=COLORS["bg_dark"],
                 fg=COLORS["success"]).pack(side="right", padx=PAD["md"])

        # ── Form card ─────────────────────────────────────────────────────────
        form_card = tk.Frame(p, bg=COLORS["bg_card"],
                             padx=PAD["lg"], pady=PAD["md"])
        form_card.pack(fill="x", pady=(0, PAD["md"]))

        tk.Label(form_card, text="Add Fee Record",
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

        # Amount
        tk.Label(form_card, text="Amount (PKR):", font=FONTS["body"],
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"],
                 ).grid(row=1, column=2, sticky="e", padx=(PAD["sm"], 4))
        self._amount_var = tk.StringVar()
        tk.Entry(form_card, textvariable=self._amount_var,
                 bg=COLORS["bg_light"], fg=COLORS["text_primary"],
                 insertbackground=COLORS["text_primary"],
                 relief="flat", bd=6, font=FONTS["body"], width=14,
                 ).grid(row=1, column=3, sticky="ew", padx=(0, PAD["sm"]))

        # Date
        tk.Label(form_card, text="Date (YYYY-MM-DD):", font=FONTS["body"],
                 bg=COLORS["bg_card"], fg=COLORS["text_secondary"],
                 ).grid(row=1, column=4, sticky="e", padx=(PAD["sm"], 4))
        self._date_var = tk.StringVar(value=date.today().isoformat())
        tk.Entry(form_card, textvariable=self._date_var,
                 bg=COLORS["bg_light"], fg=COLORS["text_primary"],
                 insertbackground=COLORS["text_primary"],
                 relief="flat", bd=6, font=FONTS["body"], width=14,
                 ).grid(row=1, column=5, sticky="ew", padx=(0, PAD["sm"]))

        form_card.columnconfigure(1, weight=3)
        form_card.columnconfigure(3, weight=2)
        form_card.columnconfigure(5, weight=2)

        btn_row = tk.Frame(form_card, bg=COLORS["bg_card"])
        btn_row.grid(row=2, column=0, columnspan=6, pady=(PAD["sm"], 0), sticky="w")
        make_button(btn_row, "💾  Add Fee Record", self._add, width=18).pack(
            side="left", padx=(0, PAD["sm"]))
        make_button(btn_row, "🔄  Refresh", self._load_fees, width=12,
                    bg=COLORS["bg_light"]).pack(side="left")

        # ── Table ─────────────────────────────────────────────────────────────
        tbl_frame = tk.Frame(p, bg=COLORS["bg_dark"])
        tbl_frame.pack(fill="both", expand=True)

        cols = ("ID", "Student Name", "Amount (PKR)", "Date")
        self._tree = ttk.Treeview(tbl_frame, columns=cols,
                                  show="headings", selectmode="browse")
        for col in cols:
            self._tree.heading(col, text=col)
        self._tree.column("ID",           width=60,  anchor="center")
        self._tree.column("Student Name", width=260, anchor="w")
        self._tree.column("Amount (PKR)", width=140, anchor="e")
        self._tree.column("Date",         width=130, anchor="center")

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

    def _load_fees(self) -> None:
        for item in self._tree.get_children():
            self._tree.delete(item)
        fees = self._fee_svc.get_all_fees()
        for idx, row in enumerate(fees):
            fmt_row = (row[0], row[1], f"{float(row[2]):,.2f}", str(row[3]))
            tag = "odd" if idx % 2 else "even"
            self._tree.insert("", "end", values=fmt_row, tags=(tag,))
        self._tree.tag_configure("odd",  background=COLORS["bg_row_alt"])
        self._tree.tag_configure("even", background=COLORS["bg_card"])

        total = self._fee_svc.get_total_collected()
        self._total_var.set(f"Total Collected: PKR {total:,.2f}")
        self._status_bar.set(f"{len(fees)} fee record(s).")

    def _add(self) -> None:
        sel_str = self._student_var.get()
        if not sel_str:
            messagebox.showwarning("No Student", "Please select a student.")
            return
        try:
            student_id = int(sel_str.split("—")[0].strip())
            self._fee_svc.add_fee(
                student_id,
                self._amount_var.get(),
                self._date_var.get(),
            )
            messagebox.showinfo("Success", "Fee record added successfully!")
            self._amount_var.set("")
            self._load_fees()
        except ValueError as e:
            messagebox.showwarning("Validation Error", str(e))
        except Exception as e:
            logger.exception("Error adding fee")
            messagebox.showerror("Error", str(e))
