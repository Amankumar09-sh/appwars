import sqlite3
from contextlib import closing
from typing import List, Tuple, Optional, Any, Dict

DB_PATH = "students.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with closing(get_connection()) as conn, conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                father_name TEXT,
                admission_date TEXT,
                gender TEXT,
                date_of_birth TEXT,
                email TEXT,
                contact_number TEXT,
                college_name TEXT,
                college_state TEXT,
                branch TEXT,
                year INTEGER,
                semester INTEGER,
                course_name TEXT,
                total_course_fee REAL,
                batch_start_date TEXT,
                duration TEXT,
                image BLOB
            )
            """
        )


def add_student(data: Dict[str, Any]) -> None:
    with closing(get_connection()) as conn, conn:
        conn.execute(
            """
            INSERT INTO students (
                first_name, last_name, father_name,
                admission_date, gender, date_of_birth,
                email, contact_number,
                college_name, college_state, branch, year, semester,
                course_name, total_course_fee, batch_start_date, duration,
                image
            ) VALUES (
                :first_name, :last_name, :father_name,
                :admission_date, :gender, :date_of_birth,
                :email, :contact_number,
                :college_name, :college_state, :branch, :year, :semester,
                :course_name, :total_course_fee, :batch_start_date, :duration,
                :image
            )
            """,
            data,
        )


def get_all_students() -> List[sqlite3.Row]:
    with closing(get_connection()) as conn, conn:
        cur = conn.execute("SELECT * FROM students ORDER BY id DESC")
        return cur.fetchall()


def get_student(student_id: int) -> Optional[sqlite3.Row]:
    with closing(get_connection()) as conn, conn:
        cur = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        row = cur.fetchone()
        return row


def update_student(student_id: int, data: Dict[str, Any]) -> None:
    with closing(get_connection()) as conn, conn:
        conn.execute(
            """
            UPDATE students SET
                first_name = :first_name,
                last_name = :last_name,
                father_name = :father_name,
                admission_date = :admission_date,
                gender = :gender,
                date_of_birth = :date_of_birth,
                email = :email,
                contact_number = :contact_number,
                college_name = :college_name,
                college_state = :college_state,
                branch = :branch,
                year = :year,
                semester = :semester,
                course_name = :course_name,
                total_course_fee = :total_course_fee,
                batch_start_date = :batch_start_date,
                duration = :duration,
                image = :image
            WHERE id = :id
            """,
            {**data, "id": student_id},
        )


def delete_student(student_id: int) -> None:
    with closing(get_connection()) as conn, conn:
        conn.execute("DELETE FROM students WHERE id = ?", (student_id,))


def get_stats() -> Dict[str, Any]:
    with closing(get_connection()) as conn, conn:
        stats: Dict[str, Any] = {}

        cur = conn.execute("SELECT COUNT(*) AS total FROM students")
        stats["total_students"] = cur.fetchone()["total"]

        cur = conn.execute(
            "SELECT course_name, COUNT(*) AS count FROM students GROUP BY course_name"
        )
        stats["by_course"] = [{"course_name": r["course_name"], "count": r["count"]} for r in cur.fetchall()]

        cur = conn.execute(
            "SELECT year, semester, COUNT(*) AS count FROM students GROUP BY year, semester"
        )
        stats["by_year_sem"] = [
            {"year": r["year"], "semester": r["semester"], "count": r["count"]}
            for r in cur.fetchall()
        ]

        return stats

