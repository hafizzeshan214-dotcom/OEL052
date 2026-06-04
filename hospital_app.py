import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ==========================
# DATABASE CONNECTION
# ==========================

def connect_db():
    return sqlite3.connect("hospital.db")

# ==========================
# CREATE TABLE
# ==========================

def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100),
        age INT,
        gender VARCHAR(20),
        disease VARCHAR(100)
    )
    """)

    conn.commit()
    conn.close()

# ==========================
# CRUD FUNCTIONS
# ==========================

def add_patient():
    if name_var.get() == "":
        messagebox.showerror("Error", "Name Required")
        return

    conn = connect_db()
    cursor = conn.cursor()

    sql = """
    INSERT INTO patients(name,age,gender,disease)
    VALUES(?,?,?,?)
    """

    values = (
        name_var.get(),
        age_var.get(),
        gender_var.get(),
        disease_var.get()
    )

    cursor.execute(sql, values)
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Patient Added")
    clear_fields()
    show_patients()

def show_patients():

    patient_table.delete(*patient_table.get_children())

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients")

    rows = cursor.fetchall()

    for row in rows:
        patient_table.insert("", tk.END, values=row)

    conn.close()

def delete_patient():

    selected = patient_table.focus()

    if not selected:
        return

    data = patient_table.item(selected)

    pid = data["values"][0]

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM patients WHERE id=?",
        (pid,)
    )

    conn.commit()
    conn.close()

    show_patients()

def update_patient():

    selected = patient_table.focus()

    if not selected:
        return

    data = patient_table.item(selected)

    pid = data["values"][0]

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE patients
    SET name=?,
        age=?,
        gender=?,
        disease=?
    WHERE id=?
    """,
    (
        name_var.get(),
        age_var.get(),
        gender_var.get(),
        disease_var.get(),
        pid
    ))

    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Patient Updated")

    show_patients()

def select_patient(event):

    selected = patient_table.focus()

    data = patient_table.item(selected)

    row = data["values"]

    if row:
        name_var.set(row[1])
        age_var.set(row[2])
        gender_var.set(row[3])
        disease_var.set(row[4])

def clear_fields():
    name_var.set("")
    age_var.set("")
    gender_var.set("")
    disease_var.set("")

# ==========================
# LOGIN
# ==========================

def login():

    username = user_var.get()
    password = pass_var.get()

    if username == "admin" and password == "admin123":
        login_frame.pack_forget()
        main_frame.pack(fill="both", expand=True)
        show_patients()
    else:
        messagebox.showerror(
            "Login Failed",
            "Invalid Username or Password"
        )

# ==========================
# GUI
# ==========================

create_table()

root = tk.Tk()
root.title("Hospital Management System")
root.geometry("1000x600")

# LOGIN VARIABLES

user_var = tk.StringVar()
pass_var = tk.StringVar()

# PATIENT VARIABLES

name_var = tk.StringVar()
age_var = tk.StringVar()
gender_var = tk.StringVar()
disease_var = tk.StringVar()

# ==========================
# LOGIN FRAME
# ==========================

login_frame = tk.Frame(root)
login_frame.pack(fill="both", expand=True)

tk.Label(
    login_frame,
    text="Hospital Login",
    font=("Arial", 20, "bold")
).pack(pady=20)

tk.Label(login_frame, text="Username").pack()
tk.Entry(
    login_frame,
    textvariable=user_var
).pack()

tk.Label(login_frame, text="Password").pack()
tk.Entry(
    login_frame,
    textvariable=pass_var,
    show="*"
).pack()

tk.Button(
    login_frame,
    text="Login",
    command=login,
    bg="green",
    fg="white"
).pack(pady=20)

# ==========================
# MAIN FRAME
# ==========================

main_frame = tk.Frame(root)

tk.Label(
    main_frame,
    text="Hospital Management System",
    font=("Arial", 18, "bold")
).pack(pady=10)

form_frame = tk.Frame(main_frame)
form_frame.pack()

tk.Label(form_frame, text="Name").grid(row=0, column=0)
tk.Entry(
    form_frame,
    textvariable=name_var
).grid(row=0, column=1)

tk.Label(form_frame, text="Age").grid(row=1, column=0)
tk.Entry(
    form_frame,
    textvariable=age_var
).grid(row=1, column=1)

tk.Label(form_frame, text="Gender").grid(row=2, column=0)
tk.Entry(
    form_frame,
    textvariable=gender_var
).grid(row=2, column=1)

tk.Label(form_frame, text="Disease").grid(row=3, column=0)
tk.Entry(
    form_frame,
    textvariable=disease_var
).grid(row=3, column=1)

button_frame = tk.Frame(main_frame)
button_frame.pack(pady=10)

tk.Button(
    button_frame,
    text="Add",
    command=add_patient,
    bg="green",
    fg="white"
).grid(row=0, column=0, padx=5)

tk.Button(
    button_frame,
    text="Update",
    command=update_patient,
    bg="orange"
).grid(row=0, column=1, padx=5)

tk.Button(
    button_frame,
    text="Delete",
    command=delete_patient,
    bg="red",
    fg="white"
).grid(row=0, column=2, padx=5)

tk.Button(
    button_frame,
    text="Clear",
    command=clear_fields
).grid(row=0, column=3, padx=5)

# TABLE

cols = (
    "ID",
    "Name",
    "Age",
    "Gender",
    "Disease"
)

patient_table = ttk.Treeview(
    main_frame,
    columns=cols,
    show="headings"
)

for col in cols:
    patient_table.heading(col, text=col)

patient_table.pack(fill="both", expand=True, pady=10)

patient_table.bind(
    "<ButtonRelease-1>",
    select_patient
)

root.mainloop()
