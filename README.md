# Appwars Technologies PVT. LTD – Student Dashboard

This is a simple student management dashboard for **Appwars Technologies PVT. LTD** built with **Python** and **Streamlit**.

It provides:
- Admin panel
- Employee panel

Both panels can manage student records with CRUD (Create/Read/Update/Delete) operations and image upload.

## Features

- Role-based login: **Admin** and **Employee** (simple, in-memory credentials)
- Manage student records with fields:
  - Student first name, last name, father name
  - Admission date, gender, date of birth
  - Email, contact number
  - College name, college state, branch, year, semester
  - Course name, total course fee, batch start date, duration
  - Student image (upload from local gallery)
- Admin dashboard statistics:
  - Total students
  - Students per course
  - Students per year and semester
- Data stored in a local SQLite database (`students.db`)

## Installation

1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the App

From the project root directory:

```bash
streamlit run app.py
```

Then open the URL shown in the terminal (usually `http://localhost:8501`) in your browser.

## Default Credentials

- Admin:
  - Username: `admin`
  - Password: `admin123`
- Employee:
  - Username: `emp`
  - Password: `emp123`

You can change these in `app.py` inside the `USERS` dictionary.

