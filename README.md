# 🎓 School Management System

A complete **desktop application** built with **Python (Tkinter)** and **MySQL** that manages students, teachers, attendance, and fees for a school environment.

---

## 📌 Description

The School Management System is a modular, OOP-based desktop app that provides a clean dark-themed GUI for school administrators to manage daily operations including student enrolment, teacher records, attendance tracking, and fee collection — all backed by a MySQL relational database.

---

## ✨ Features

| Module | Functionality |
|---|---|
| 🔐 Login | Admin authentication with validation & error messages |
| 👨‍🎓 Student Management | Full CRUD — Add, View, Update, Delete students |
| 👩‍🏫 Teacher Management | Full CRUD — Add, View, Update, Delete teachers |
| 📋 Attendance | Mark and view attendance with Present / Absent / Late status |
| 💰 Fee Management | Record fee payments, view history, total collected |
| 📊 Reports Dashboard | Key stats: total students, teachers, fees, today's attendance |

---

## 🛠️ Technologies Used

- **Python 3.10+**
- **Tkinter** — GUI framework
- **MySQL** — Relational database
- **mysql-connector-python** — MySQL driver
- **pytest** — Unit testing framework
- **Logging** — Python built-in `logging` module

---

## 📁 Project Structure

```
OEL052/
├── app/
│   ├── __init__.py
│   ├── main.py                  # Entry point
│   ├── views/
│   │   ├── login.py             # Login window
│   │   ├── dashboard.py         # Main dashboard with sidebar
│   │   ├── student.py           # Student CRUD view
│   │   ├── teacher.py           # Teacher CRUD view
│   │   ├── attendance.py        # Attendance view
│   │   ├── fees.py              # Fee management view
│   │   └── reports.py           # Reports / analytics view
│   ├── models/
│   │   ├── user_model.py        # User dataclass
│   │   ├── student_model.py     # Student dataclass
│   │   └── teacher_model.py     # Teacher dataclass
│   ├── services/
│   │   ├── auth_service.py      # Login business logic
│   │   ├── student_service.py   # Student CRUD logic
│   │   ├── teacher_service.py   # Teacher CRUD logic
│   │   ├── attendance_service.py# Attendance logic
│   │   └── fee_service.py       # Fee logic
│   └── utils/
│       ├── db.py                # DB connection & initialisation
│       ├── styles.py            # Design tokens & widget factories
│       └── logger.py            # Logging configuration
├── tests/
│   ├── test_auth.py             # Auth unit tests
│   └── test_student.py          # Student CRUD unit tests
├── requirements.txt
└── README.md
```

---

## ⚙️ Database Setup

### Prerequisites
- MySQL Server installed and running
- MySQL user with CREATE DATABASE privileges

### Step 1 — Configure credentials

Open `app/utils/db.py` and update:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",   # ← change this
    "database": "school_db",
}
```

### Step 2 — Database is auto-created on first run

The application automatically:
1. Creates the `school_db` database
2. Creates all 5 tables (`users`, `students`, `teachers`, `attendance`, `fees`)
3. Inserts sample data for testing

### Tables

```sql
users       (id, username, password)
students    (id, name, class, age)
teachers    (id, name, subject)
attendance  (id, student_id, date, status)
fees        (id, student_id, amount, date)
```

### Sample Admin Account

| Username | Password  |
|----------|-----------|
| `admin`  | `admin123`|

---

## 🚀 How to Run the Project

### Step 1 — Clone the repository

```bash
git clone https://github.com/<your-username>/OEL052.git
cd OEL052
```

### Step 2 — Create a virtual environment (recommended)

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Update MySQL password in `app/utils/db.py`

### Step 5 — Run the application

```bash
python -m app.main
```

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

All tests use mocked database connections — no live MySQL required.

---

## 🔄 Git & Version Control

```bash
git init
git add .
git commit -m "Initial commit: School Management System"

# Feature branches used during development:
git checkout -b feature-login
git checkout -b feature-student
git checkout -b feature-teacher
```

---

## 👥 Collaborators

- **shah7008** — GitHub collaborator

---

## 🚨 Error Handling

The application handles:
- ❌ Database connection failures — user-friendly dialog on startup
- ❌ Invalid login credentials — inline error message
- ❌ Empty / invalid input fields — validation warnings per field
- ❌ Unexpected runtime errors — logged to `logs/sms_YYYYMMDD.log`

---

## 📄 License

This project is for educational purposes (Software Construction course OEL).
