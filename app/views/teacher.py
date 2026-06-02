"""
teacher.py - Teacher management view (CRUD).
"""
import tkinter as tk
from tkinter import ttk, messagebox
from app.services.teacher_service import TeacherService
from app.utils.styles import (
    COLORS, FONTS, PAD,
    make_button, make_danger_button,
)
from app.utils.logger import get_logger

logger = get_logger(__name__)


class TeacherView:
    """Full CRUD interface for managing teachers."""

    def __init__(self, parent: tk.Frame):
        self._svc = TeacherService()
        self._parent = parent
        self._selected_id: int | None = None
        self._build_ui()
        self._load_teachers()

    def _build_ui(self) -> None:
        p = self._parent

        hdr = tk.Frame(p, bg=COLORS["bg_dark"])
        hdr.pack(fill="x", pady=(0, PAD["md"]))
        tk.Label(hdr, text="👩‍🏫  Teacher Management",
                 font=FONTS["title"], bg=COLORS["bg_dark"],
                 fg=COLORS["text_primary"]).pack(side="left")

        # Form card
        form_card = tk.Frame(p, bg=COLORS["bg_card"],
                             padx=PAD["lg"], pady=PAD["md"])
        form_card.pack(fill="x", pady=(0, PAD["md"]))

        tk.Label(form_card, text="Teacher Details",
                 font=FONTS["subhead"], bg=COLORS["bg_card"],
                 fg=COLORS["accent"]).grid(row=0, column=0, columnspan=4,
                                           sticky="w", pady=(0, PAD["sm"]))

        self._name_var    = tk.StringVar()
        self._subject_var = tk.StringVar()

        for col, (lbl, var, w) in enumerate([
            ("Full Name:", self._name_var, 28),
            ("Subject:",   self._subject_var, 22),
        ]):
            tk.Label(form_card, text=lbl, font=FONTS["body"],
                     bg=COLORS["bg_card"], fg=COLORS["text_secondary"],
                     ).grid(row=1, column=col * 2, sticky="e",
                            padx=(PAD["sm"], 4), pady=6)
            tk.Entry(form_card, textvariable=var,
                     bg=COLORS["bg_light"], fg=COLORS["text_primary"],
                     insertbackground=COLORS["text_primary"],
                     relief="flat", bd=6, font=FONTS["body"],
                     width=w,
                     ).grid(row=1, column=col * 2 + 1, sticky="ew",
                            padx=(0, PAD["sm"]))

        form_card.columnconfigure(1, weight=3)
        form_card.columnconfigure(3, weight=2)

        # Buttons
        btn_row = tk.Frame(form_card, bg=COLORS["bg_card"])
        btn_row.grid(row=2, column=0, columnspan=4, pady=(PAD["sm"], 0), sticky="w")

        for btn in [
            make_button(btn_row, "➕  Add Teacher",   self._add,    width=16),
            make_button(btn_row, "✏️  Update",        self._update, width=14,
                        bg=COLORS["success"]),
            make_danger_button(btn_row, "🗑️  Delete",  self._delete, width=12),
            make_button(btn_row, "🔄  Clear",         self._clear,  width=12,
                        bg=COLORS["bg_light"]),
        ]:
            btn.pack(side="left", padx=(0, PAD["sm"]))

        # Table
        tbl_frame = tk.Frame(p, bg=COLORS["bg_dark"])
        tbl_frame.pack(fill="both", expand=True)

        cols = ("ID", "Name", "Subject")
        self._tree = ttk.Treeview(tbl_frame, columns=cols,
                                  show="headings", selectmode="browse")
        self._tree.heading("ID",      text="ID")
        self._tree.heading("Name",    text="Name")
        self._tree.heading("Subject", text="Subject")
        self._tree.column("ID",      width=60,  anchor="center")
        self._tree.column("Name",    width=280, anchor="w")
        self._tree.column("Subject", width=200, anchor="w")

        vsb = ttk.Scrollbar(tbl_frame, orient="vertical",
                            command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self._tree.pack(fill="both", expand=True)
        self._tree.bind("<<TreeviewSelect>>", self._on_select)

        self._status_var = tk.StringVar(value="Ready")
        tk.Label(p, textvariable=self._status_var, font=FONTS["small"],
                 bg=COLORS["bg_dark"], fg=COLORS["text_muted"],
                 anchor="w").pack(fill="x", pady=(4, 0))

    def _load_teachers(self) -> None:
        for item in self._tree.get_children():
            self._tree.delete(item)
        teachers = self._svc.get_all_teachers()
        for idx, t in enumerate(teachers):
            tag = "odd" if idx % 2 else "even"
            self._tree.insert("", "end",
                              values=(t.id, t.name, t.subject), tags=(tag,))
        self._tree.tag_configure("odd",  background=COLORS["bg_row_alt"])
        self._tree.tag_configure("even", background=COLORS["bg_card"])
        self._status_var.set(f"{len(teachers)} teacher(s) found.")

    def _on_select(self, _event) -> None:
        sel = self._tree.selection()
        if not sel:
            return
        values = self._tree.item(sel[0])["values"]
        self._selected_id = values[0]
        self._name_var.set(values[1])
        self._subject_var.set(values[2])

    def _add(self) -> None:
        try:
            self._svc.add_teacher(self._name_var.get(), self._subject_var.get())
            messagebox.showinfo("Success", "Teacher added successfully!")
            self._clear(); self._load_teachers()
        except ValueError as e:
            messagebox.showwarning("Validation Error", str(e))
        except Exception as e:
            logger.exception("Error adding teacher")
            messagebox.showerror("Error", str(e))

    def _update(self) -> None:
        if not self._selected_id:
            messagebox.showwarning("No Selection", "Select a teacher first.")
            return
        try:
            self._svc.update_teacher(self._selected_id,
                                     self._name_var.get(),
                                     self._subject_var.get())
            messagebox.showinfo("Success", "Teacher updated successfully!")
            self._clear(); self._load_teachers()
        except ValueError as e:
            messagebox.showwarning("Validation Error", str(e))
        except Exception as e:
            logger.exception("Error updating teacher")
            messagebox.showerror("Error", str(e))

    def _delete(self) -> None:
        if not self._selected_id:
            messagebox.showwarning("No Selection", "Select a teacher first.")
            return
        if not messagebox.askyesno("Confirm", "Delete this teacher?"):
            return
        try:
            self._svc.delete_teacher(self._selected_id)
            messagebox.showinfo("Deleted", "Teacher deleted successfully!")
            self._clear(); self._load_teachers()
        except Exception as e:
            logger.exception("Error deleting teacher")
            messagebox.showerror("Error", str(e))

    def _clear(self) -> None:
        self._selected_id = None
        self._name_var.set("")
        self._subject_var.set("")
        self._tree.selection_remove(self._tree.selection())
