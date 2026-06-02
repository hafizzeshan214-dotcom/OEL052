"""
student.py - Student management view (CRUD).
"""
import tkinter as tk
from tkinter import ttk, messagebox
from app.services.student_service import StudentService
from app.utils.styles import (
    COLORS, FONTS, PAD,
    make_button, make_danger_button, make_label, add_hover,
)
from app.utils.logger import get_logger

logger = get_logger(__name__)


class StudentView:
    """Full CRUD interface for managing students."""

    def __init__(self, parent: tk.Frame):
        self._svc = StudentService()
        self._parent = parent
        self._selected_id: int | None = None
        self._build_ui()
        self._load_students()

    # ── UI Builder ────────────────────────────────────────────────────────────
    def _build_ui(self) -> None:
        p = self._parent

        # Page title
        hdr = tk.Frame(p, bg=COLORS["bg_dark"])
        hdr.pack(fill="x", pady=(0, PAD["md"]))
        tk.Label(hdr, text="👨‍🎓  Student Management",
                 font=FONTS["title"], bg=COLORS["bg_dark"],
                 fg=COLORS["text_primary"]).pack(side="left")

        # ── Form card ─────────────────────────────────────────────────────────
        form_card = tk.Frame(p, bg=COLORS["bg_card"],
                             padx=PAD["lg"], pady=PAD["md"])
        form_card.pack(fill="x", pady=(0, PAD["md"]))

        tk.Label(form_card, text="Student Details",
                 font=FONTS["subhead"], bg=COLORS["bg_card"],
                 fg=COLORS["accent"]).grid(row=0, column=0, columnspan=6,
                                           sticky="w", pady=(0, PAD["sm"]))

        fields = [("Full Name:", 0, 1), ("Class:", 0, 3), ("Age:", 0, 5)]
        self._name_var  = tk.StringVar()
        self._class_var = tk.StringVar()
        self._age_var   = tk.StringVar()
        vars_list = [self._name_var, self._class_var, self._age_var]

        for (lbl_txt, row, col), var in zip(fields, vars_list):
            tk.Label(form_card, text=lbl_txt, font=FONTS["body"],
                     bg=COLORS["bg_card"], fg=COLORS["text_secondary"],
                     ).grid(row=row, column=col - 1, sticky="e",
                            padx=(PAD["sm"], 4), pady=6)
            entry = tk.Entry(form_card, textvariable=var,
                             bg=COLORS["bg_light"], fg=COLORS["text_primary"],
                             insertbackground=COLORS["text_primary"],
                             relief="flat", bd=6, font=FONTS["body"],
                             width=20 if col == 1 else 12)
            entry.grid(row=row, column=col, sticky="ew", padx=(0, PAD["sm"]))

        form_card.columnconfigure(1, weight=3)
        form_card.columnconfigure(3, weight=2)
        form_card.columnconfigure(5, weight=1)

        # Buttons row
        btn_row = tk.Frame(form_card, bg=COLORS["bg_card"])
        btn_row.grid(row=1, column=0, columnspan=6, pady=(PAD["sm"], 0), sticky="w")

        add_btn  = make_button(btn_row, "➕  Add Student",   self._add,    width=16)
        upd_btn  = make_button(btn_row, "✏️  Update",        self._update, width=14,
                               bg=COLORS["success"])
        del_btn  = make_danger_button(btn_row, "🗑️  Delete",  self._delete, width=12)
        clr_btn  = make_button(btn_row, "🔄  Clear",         self._clear,  width=12,
                               bg=COLORS["bg_light"])
        for b in (add_btn, upd_btn, del_btn, clr_btn):
            b.pack(side="left", padx=(0, PAD["sm"]))

        # ── Table ─────────────────────────────────────────────────────────────
        tbl_frame = tk.Frame(p, bg=COLORS["bg_dark"])
        tbl_frame.pack(fill="both", expand=True)

        cols = ("ID", "Name", "Class", "Age")
        self._tree = ttk.Treeview(tbl_frame, columns=cols,
                                  show="headings", selectmode="browse")
        for col in cols:
            self._tree.heading(col, text=col)
        self._tree.column("ID",    width=60,  anchor="center")
        self._tree.column("Name",  width=250, anchor="w")
        self._tree.column("Class", width=120, anchor="center")
        self._tree.column("Age",   width=80,  anchor="center")

        vsb = ttk.Scrollbar(tbl_frame, orient="vertical",
                            command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self._tree.pack(fill="both", expand=True)
        self._tree.bind("<<TreeviewSelect>>", self._on_select)

        # Status bar
        self._status_var = tk.StringVar(value="Ready")
        tk.Label(p, textvariable=self._status_var, font=FONTS["small"],
                 bg=COLORS["bg_dark"], fg=COLORS["text_muted"],
                 anchor="w").pack(fill="x", pady=(4, 0))

    # ── Data operations ───────────────────────────────────────────────────────
    def _load_students(self) -> None:
        for item in self._tree.get_children():
            self._tree.delete(item)
        students = self._svc.get_all_students()
        for idx, s in enumerate(students):
            tag = "odd" if idx % 2 else "even"
            self._tree.insert("", "end",
                              values=(s.id, s.name, s.class_name, s.age),
                              tags=(tag,))
        self._tree.tag_configure("odd",  background=COLORS["bg_row_alt"])
        self._tree.tag_configure("even", background=COLORS["bg_card"])
        self._status_var.set(f"{len(students)} student(s) found.")
        logger.debug("Student table refreshed: %d rows", len(students))

    def _on_select(self, _event) -> None:
        sel = self._tree.selection()
        if not sel:
            return
        values = self._tree.item(sel[0])["values"]
        self._selected_id = values[0]
        self._name_var.set(values[1])
        self._class_var.set(values[2])
        self._age_var.set(values[3])

    def _add(self) -> None:
        try:
            self._svc.add_student(
                self._name_var.get(),
                self._class_var.get(),
                self._age_var.get(),
            )
            messagebox.showinfo("Success", "Student added successfully!")
            self._clear()
            self._load_students()
        except ValueError as e:
            messagebox.showwarning("Validation Error", str(e))
        except Exception as e:
            logger.exception("Error adding student")
            messagebox.showerror("Error", str(e))

    def _update(self) -> None:
        if not self._selected_id:
            messagebox.showwarning("No Selection", "Please select a student first.")
            return
        try:
            self._svc.update_student(
                self._selected_id,
                self._name_var.get(),
                self._class_var.get(),
                self._age_var.get(),
            )
            messagebox.showinfo("Success", "Student updated successfully!")
            self._clear()
            self._load_students()
        except ValueError as e:
            messagebox.showwarning("Validation Error", str(e))
        except Exception as e:
            logger.exception("Error updating student")
            messagebox.showerror("Error", str(e))

    def _delete(self) -> None:
        if not self._selected_id:
            messagebox.showwarning("No Selection", "Please select a student first.")
            return
        if not messagebox.askyesno("Confirm Delete",
                                   "Delete this student and all related records?"):
            return
        try:
            self._svc.delete_student(self._selected_id)
            messagebox.showinfo("Deleted", "Student deleted successfully!")
            self._clear()
            self._load_students()
        except Exception as e:
            logger.exception("Error deleting student")
            messagebox.showerror("Error", str(e))

    def _clear(self) -> None:
        self._selected_id = None
        self._name_var.set("")
        self._class_var.set("")
        self._age_var.set("")
        self._tree.selection_remove(self._tree.selection())
