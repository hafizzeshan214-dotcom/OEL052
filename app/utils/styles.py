"""
styles.py - Centralised design tokens and widget-factory helpers.
All colours, fonts, and padding live here so every view stays consistent.
"""
from tkinter import ttk
import tkinter as tk

# ── Colour palette ────────────────────────────────────────────────────────────
COLORS = {
    # Backgrounds
    "bg_dark":      "#0f1923",
    "bg_medium":    "#1a2d42",
    "bg_card":      "#1e3448",
    "bg_light":     "#243b55",
    "bg_row_alt":   "#1b2e40",

    # Accents
    "accent":       "#3498db",
    "accent_hover": "#2980b9",
    "accent_light": "#5dade2",

    # Status
    "success":      "#27ae60",
    "warning":      "#f39c12",
    "danger":       "#e74c3c",
    "danger_hover": "#c0392b",
    "info":         "#16a085",

    # Text
    "text_primary":   "#ecf0f1",
    "text_secondary": "#bdc3c7",
    "text_muted":     "#7f8c8d",

    # Borders
    "border":       "#2c4a6e",
    "border_light": "#34567e",

    # Sidebar
    "sidebar_bg":       "#0d1f30",
    "sidebar_hover":    "#1a3550",
    "sidebar_selected": "#3498db",
}

# ── Typography ────────────────────────────────────────────────────────────────
FONTS = {
    "title":    ("Segoe UI", 22, "bold"),
    "heading":  ("Segoe UI", 14, "bold"),
    "subhead":  ("Segoe UI", 12, "bold"),
    "body":     ("Segoe UI", 11),
    "small":    ("Segoe UI", 10),
    "button":   ("Segoe UI", 11, "bold"),
    "table":    ("Segoe UI", 10),
    "table_hd": ("Segoe UI", 10, "bold"),
    "mono":     ("Consolas", 10),
}

# ── Padding / geometry ────────────────────────────────────────────────────────
PAD = {"xs": 4, "sm": 8, "md": 14, "lg": 20, "xl": 30}


# ── Widget factories ──────────────────────────────────────────────────────────

def apply_global_style(root: tk.Tk) -> None:
    """Apply a dark ttk theme and global widget colours to *root*."""
    style = ttk.Style(root)
    style.theme_use("clam")

    # General frame / label defaults
    style.configure("TFrame",  background=COLORS["bg_dark"])
    style.configure("TLabel",  background=COLORS["bg_dark"],
                    foreground=COLORS["text_primary"], font=FONTS["body"])

    # Entry
    style.configure("TEntry",
                    fieldbackground=COLORS["bg_light"],
                    foreground=COLORS["text_primary"],
                    insertcolor=COLORS["text_primary"],
                    bordercolor=COLORS["border"],
                    font=FONTS["body"])

    # Combobox
    style.configure("TCombobox",
                    fieldbackground=COLORS["bg_light"],
                    foreground=COLORS["text_primary"],
                    selectbackground=COLORS["accent"],
                    font=FONTS["body"])
    style.map("TCombobox", fieldbackground=[("readonly", COLORS["bg_light"])])

    # Scrollbar
    style.configure("TScrollbar",
                    background=COLORS["bg_medium"],
                    troughcolor=COLORS["bg_dark"],
                    arrowcolor=COLORS["text_secondary"])

    # Treeview
    style.configure("Treeview",
                    background=COLORS["bg_card"],
                    foreground=COLORS["text_primary"],
                    fieldbackground=COLORS["bg_card"],
                    rowheight=30,
                    font=FONTS["table"])
    style.configure("Treeview.Heading",
                    background=COLORS["bg_medium"],
                    foreground=COLORS["accent_light"],
                    font=FONTS["table_hd"],
                    relief="flat")
    style.map("Treeview",
              background=[("selected", COLORS["accent"])],
              foreground=[("selected", COLORS["text_primary"])])
    style.map("Treeview.Heading",
              background=[("active", COLORS["bg_light"])])

    root.configure(bg=COLORS["bg_dark"])


def make_button(parent, text: str, command=None,
                bg: str = None, fg: str = None,
                width: int = 18, font=None) -> tk.Button:
    """Return a styled flat tk.Button."""
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg or COLORS["accent"],
        fg=fg or COLORS["text_primary"],
        font=font or FONTS["button"],
        width=width,
        relief="flat",
        bd=0,
        padx=PAD["sm"],
        pady=PAD["xs"],
        cursor="hand2",
        activebackground=COLORS["accent_hover"],
        activeforeground=COLORS["text_primary"],
    )


def make_danger_button(parent, text: str, command=None, width: int = 18) -> tk.Button:
    return make_button(parent, text, command,
                       bg=COLORS["danger"], fg=COLORS["text_primary"], width=width)


def make_label(parent, text: str, font=None, fg: str = None, bg: str = None) -> tk.Label:
    return tk.Label(
        parent,
        text=text,
        font=font or FONTS["body"],
        fg=fg or COLORS["text_primary"],
        bg=bg or COLORS["bg_dark"],
    )


def make_entry(parent, width: int = 28, show: str = None) -> tk.Entry:
    entry = tk.Entry(
        parent,
        width=width,
        bg=COLORS["bg_light"],
        fg=COLORS["text_primary"],
        insertbackground=COLORS["text_primary"],
        relief="flat",
        bd=6,
        font=FONTS["body"],
    )
    if show:
        entry.config(show=show)
    return entry


def make_frame(parent, bg: str = None, padx: int = 0, pady: int = 0) -> tk.Frame:
    return tk.Frame(parent, bg=bg or COLORS["bg_dark"], padx=padx, pady=pady)


def make_card(parent, bg: str = None) -> tk.Frame:
    """A slightly-raised card panel."""
    return tk.Frame(parent, bg=bg or COLORS["bg_card"],
                    bd=0, relief="flat", padx=PAD["md"], pady=PAD["md"])


def make_separator(parent, orient: str = "horizontal") -> ttk.Separator:
    sep = ttk.Separator(parent, orient=orient)
    return sep


def add_hover(widget: tk.Button,
              normal_bg: str, hover_bg: str,
              normal_fg: str = None, hover_fg: str = None) -> None:
    """Bind hover colours to a tk.Button."""
    nfg = normal_fg or COLORS["text_primary"]
    hfg = hover_fg  or COLORS["text_primary"]
    widget.bind("<Enter>", lambda _: widget.config(bg=hover_bg, fg=hfg))
    widget.bind("<Leave>", lambda _: widget.config(bg=normal_bg, fg=nfg))
