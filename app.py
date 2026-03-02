from typing import Dict, Any, Optional, List
import base64

import streamlit as st  # type: ignore[import]

import db


st.set_page_config(
    page_title="Appwars Technologies PVT. LTD – Student Dashboard",
    layout="wide",
)


def apply_global_theme() -> None:
    """Apply royal blue background to the whole app."""
    st.markdown(
        """
        <style>
        body {
            background-color: #4169e1; /* royal blue */
        }
        .stApp {
            background-color: transparent;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_logo_video() -> None:
    """Render the video as a small logo at the top of the page."""
    try:
        video_path = "Image_To_Live_Wallpaper_Conversion.mp4"
        with open(video_path, "rb") as f:
            video_bytes = f.read()

        video_b64 = base64.b64encode(video_bytes).decode("utf-8")

        html_code = f"""
        <style>
        .appwars-logo-wrapper {{
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 0.5rem;
            margin-bottom: 0.75rem;
        }}
        .appwars-logo-video {{
            height: 250px;
            border-radius: 4px;
        }}
        </style>
        <div class="appwars-logo-wrapper">
            <video class="appwars-logo-video" autoplay muted loop playsinline>
                <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
            </video>
        </div>
        """
        st.markdown(html_code, unsafe_allow_html=True)
    except Exception:
        # If the video isn't available, silently skip the logo
        pass


# Simple in-memory users for demo purposes
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "emp": {"password": "emp123", "role": "employee"},
}


def init_app_state() -> None:
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "role" not in st.session_state:
        st.session_state.role = None
    if "username" not in st.session_state:
        st.session_state.username = None


def login_form() -> None:
    st.title("Appwars Technologies PVT. LTD")
    st.subheader("Student Management Dashboard")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Login as", ["admin", "employee"])
        submitted = st.form_submit_button("Login")

        if submitted:
            user = USERS.get(username)
            if user and user["password"] == password and user["role"] == role:
                st.session_state.logged_in = True
                st.session_state.role = role
                st.session_state.username = username
                st.success(f"Logged in as {role.capitalize()}")
                st.experimental_rerun()
            else:
                st.error("Invalid username, password, or role")


def logout_button() -> None:
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.username = None
        st.experimental_rerun()


def student_form(existing: Optional[Dict[str, Any]] = None, prefix: str = "") -> Dict[str, Any]:
    """Reusable student form. Prefix ensures unique Streamlit widget keys."""
    col1, col2, col3 = st.columns(3)

    with col1:
        first_name = st.text_input(
            "Student First Name",
            value=existing.get("first_name") if existing else "",
            key=f"{prefix}_first_name",
        )
        last_name = st.text_input(
            "Student Last Name",
            value=existing.get("last_name") if existing else "",
            key=f"{prefix}_last_name",
        )
        father_name = st.text_input(
            "Father Name",
            value=existing.get("father_name") if existing else "",
            key=f"{prefix}_father_name",
        )
        admission_date = st.date_input(
            "Admission Date",
            value=existing.get("admission_date") if existing and existing.get("admission_date") else None,
            key=f"{prefix}_admission_date",
        )
        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"],
            index=(
                ["Male", "Female", "Other"].index(existing.get("gender"))
                if existing and existing.get("gender") in ["Male", "Female", "Other"]
                else 0
            ),
            key=f"{prefix}_gender",
        )
        date_of_birth = st.date_input(
            "Date of Birth",
            value=existing.get("date_of_birth") if existing and existing.get("date_of_birth") else None,
            key=f"{prefix}_dob",
        )

    with col2:
        email = st.text_input(
            "Email",
            value=existing.get("email") if existing else "",
            key=f"{prefix}_email",
        )
        contact_number = st.text_input(
            "Contact Number",
            value=existing.get("contact_number") if existing else "",
            key=f"{prefix}_contact_number",
        )
        college_name = st.text_input(
            "College Name",
            value=existing.get("college_name") if existing else "",
            key=f"{prefix}_college_name",
        )
        college_state = st.text_input(
            "College State",
            value=existing.get("college_state") if existing else "",
            key=f"{prefix}_college_state",
        )
        branch = st.text_input(
            "Branch",
            value=existing.get("branch") if existing else "",
            key=f"{prefix}_branch",
        )
        year = st.number_input(
            "Year",
            min_value=1,
            max_value=10,
            step=1,
            value=int(existing.get("year")) if existing and existing.get("year") else 1,
            key=f"{prefix}_year",
        )
        semester = st.number_input(
            "Semester",
            min_value=1,
            max_value=20,
            step=1,
            value=int(existing.get("semester"))
            if existing and existing.get("semester")
            else 1,
            key=f"{prefix}_semester",
        )

    with col3:
        course_name = st.text_input(
            "Course Name",
            value=existing.get("course_name") if existing else "",
            key=f"{prefix}_course_name",
        )
        total_course_fee = st.number_input(
            "Total Course Fee",
            min_value=0.0,
            step=100.0,
            value=float(existing.get("total_course_fee"))
            if existing and existing.get("total_course_fee")
            else 0.0,
            key=f"{prefix}_total_course_fee",
        )
        batch_start_date = st.date_input(
            "Batch Start Date",
            value=existing.get("batch_start_date")
            if existing and existing.get("batch_start_date")
            else None,
            key=f"{prefix}_batch_start_date",
        )
        duration = st.text_input(
            "Duration (e.g., 6 months, 1 year)",
            value=existing.get("duration") if existing else "",
            key=f"{prefix}_duration",
        )

        st.markdown("**Student Image (from gallery)**")
        uploaded_file = st.file_uploader(
            "Upload Image",
            type=["png", "jpg", "jpeg"],
            key=f"{prefix}_image_{existing.get('id') if existing else 'new'}",
        )

        image_bytes: Optional[bytes] = None
        if uploaded_file is not None:
            image_bytes = uploaded_file.read()
            try:
                st.image(image_bytes, caption="Preview", use_column_width=True)
            except Exception:
                st.warning("Could not preview image, but it will be saved.")
        else:
            if existing and existing.get("image"):
                image_bytes = existing.get("image")
                try:
                    st.image(image_bytes, caption="Current Image", use_column_width=True)
                except Exception:
                    st.warning("Could not preview existing image.")

    data: Dict[str, Any] = {
        "first_name": first_name.strip(),
        "last_name": last_name.strip(),
        "father_name": father_name.strip(),
        "admission_date": admission_date.isoformat() if admission_date else "",
        "gender": gender,
        "date_of_birth": date_of_birth.isoformat() if date_of_birth else "",
        "email": email.strip(),
        "contact_number": contact_number.strip(),
        "college_name": college_name.strip(),
        "college_state": college_state.strip(),
        "branch": branch.strip(),
        "year": int(year),
        "semester": int(semester),
        "course_name": course_name.strip(),
        "total_course_fee": float(total_course_fee),
        "batch_start_date": batch_start_date.isoformat() if batch_start_date else "",
        "duration": duration.strip(),
        "image": image_bytes if image_bytes is not None else (existing.get("image") if existing else None),
    }
    return data


def filter_students(
    students: List[dict],
    search: str,
    course: str,
    year: Optional[int],
    semester: Optional[int],
    state: str,
) -> List[dict]:
    result = []
    search_lower = search.lower()
    for s in students:
        if search_lower:
            haystack = " ".join(
                [
                    str(s.get("first_name", "")),
                    str(s.get("last_name", "")),
                    str(s.get("email", "")),
                    str(s.get("college_name", "")),
                    str(s.get("course_name", "")),
                ]
            ).lower()
            if search_lower not in haystack:
                continue

        if course and s.get("course_name") != course:
            continue
        if year and s.get("year") != year:
            continue
        if semester and s.get("semester") != semester:
            continue
        if state and s.get("college_state") != state:
            continue

        result.append(s)
    return result


def admin_panel() -> None:
    st.title("Admin Panel")
    st.write("Manage student records for Appwars Technologies PVT. LTD.")

    tabs = st.tabs(["Dashboard", "Add Student", "View / Edit Students"])

    # Dashboard tab with statistics
    with tabs[0]:
        stats = db.get_stats()
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Total Students", stats.get("total_students", 0))

        with c2:
            st.write("Students by Course")
            if stats.get("by_course"):
                for item in stats["by_course"]:
                    st.write(f"- {item['course_name'] or 'Unknown'}: {item['count']}")
            else:
                st.write("No data yet.")

        st.write("Students by Year & Semester")
        if stats.get("by_year_sem"):
            for item in stats["by_year_sem"]:
                year = item["year"] if item["year"] is not None else "N/A"
                sem = item["semester"] if item["semester"] is not None else "N/A"
                st.write(f"- Year {year}, Semester {sem}: {item['count']}")
        else:
            st.write("No data yet.")

    # Add student tab
    with tabs[1]:
        st.subheader("Add New Student")
        data = student_form(prefix="admin_add")
        if st.button("Save Student"):
            if not data["first_name"] or not data["last_name"]:
                st.error("First name and last name are required.")
            else:
                db.add_student(data)
                st.success("Student added successfully.")

    # View / Edit students tab
    with tabs[2]:
        st.subheader("Students List")
        rows = db.get_all_students()
        students = [dict(r) for r in rows]

        all_courses = sorted({s["course_name"] for s in students if s.get("course_name")})
        all_states = sorted({s["college_state"] for s in students if s.get("college_state")})

        with st.expander("Search & Filters", expanded=True):
            search = st.text_input("Search (name, email, college, course)")
            course = st.selectbox("Course", [""] + all_courses)
            state = st.selectbox("College State", [""] + all_states)
            year = st.number_input("Year (0 = any)", min_value=0, max_value=10, value=0, step=1)
            semester = st.number_input("Semester (0 = any)", min_value=0, max_value=20, value=0, step=1)

        filtered = filter_students(
            students,
            search=search,
            course=course,
            year=int(year) if year else None,
            semester=int(semester) if semester else None,
            state=state,
        )

        if filtered:
            st.write(f"Showing {len(filtered)} students")
            st.dataframe(
                [
                    {
                        "ID": s["id"],
                        "Name": f"{s['first_name']} {s['last_name']}",
                        "Email": s["email"],
                        "Contact": s["contact_number"],
                        "College": s["college_name"],
                        "Course": s["course_name"],
                        "Year": s["year"],
                        "Semester": s["semester"],
                    }
                    for s in filtered
                ],
                use_container_width=True,
            )

            selected_id = st.selectbox(
                "Select Student ID to View / Edit / Delete",
                [s["id"] for s in filtered],
            )

            if selected_id:
                selected_row = next(s for s in filtered if s["id"] == selected_id)
                st.markdown("---")
                st.subheader(f"Edit Student – ID {selected_row['id']}")

                col_left, col_right = st.columns([2, 1])
                with col_left:
                    updated_data = student_form(existing=selected_row, prefix=f"admin_edit_{selected_row['id']}")
                    if st.button("Update Student"):
                        db.update_student(selected_row["id"], updated_data)
                        st.success("Student updated successfully.")
                        st.experimental_rerun()

                with col_right:
                    st.markdown("### Quick View")
                    st.write(f"**Name:** {selected_row['first_name']} {selected_row['last_name']}")
                    st.write(f"**Email:** {selected_row['email']}")
                    st.write(f"**Contact:** {selected_row['contact_number']}")
                    st.write(f"**College:** {selected_row['college_name']} ({selected_row['college_state']})")
                    st.write(f"**Course:** {selected_row['course_name']}")
                    st.write(f"**Year/Semester:** {selected_row['year']} / {selected_row['semester']}")

                    if selected_row.get("image"):
                        try:
                            st.image(selected_row["image"], caption="Student Image", use_column_width=True)
                        except Exception:
                            st.warning("Could not display student image.")

                    if st.button("Delete Student", type="primary"):
                        confirm = st.checkbox("Confirm delete permanently")
                        if confirm:
                            db.delete_student(selected_row["id"])
                            st.success("Student deleted successfully.")
                            st.experimental_rerun()
        else:
            st.info("No students found.")


def employee_panel() -> None:
    st.title("Employee Panel")
    st.write("Manage student records assigned to you.")

    tabs = st.tabs(["Add Student", "View / Edit Students"])

    with tabs[0]:
        st.subheader("Add New Student")
        data = student_form(prefix="emp_add")
        if st.button("Save Student (Employee)"):
            if not data["first_name"] or not data["last_name"]:
                st.error("First name and last name are required.")
            else:
                db.add_student(data)
                st.success("Student added successfully.")

    with tabs[1]:
        st.subheader("Students List")
        rows = db.get_all_students()
        students = [dict(r) for r in rows]

        all_courses = sorted({s["course_name"] for s in students if s.get("course_name")})
        all_states = sorted({s["college_state"] for s in students if s.get("college_state")})

        with st.expander("Search & Filters", expanded=True):
            search = st.text_input("Search (name, email, college, course)", key="emp_search")
            course = st.selectbox("Course", [""] + all_courses, key="emp_course")
            state = st.selectbox("College State", [""] + all_states, key="emp_state")
            year = st.number_input(
                "Year (0 = any)", min_value=0, max_value=10, value=0, step=1, key="emp_year"
            )
            semester = st.number_input(
                "Semester (0 = any)", min_value=0, max_value=20, value=0, step=1, key="emp_semester"
            )

        filtered = filter_students(
            students,
            search=search,
            course=course,
            year=int(year) if year else None,
            semester=int(semester) if semester else None,
            state=state,
        )

        if filtered:
            st.write(f"Showing {len(filtered)} students")
            st.dataframe(
                [
                    {
                        "ID": s["id"],
                        "Name": f"{s['first_name']} {s['last_name']}",
                        "Email": s["email"],
                        "Contact": s["contact_number"],
                        "College": s["college_name"],
                        "Course": s["course_name"],
                        "Year": s["year"],
                        "Semester": s["semester"],
                    }
                    for s in filtered
                ],
                use_container_width=True,
            )

            selected_id = st.selectbox(
                "Select Student ID to View / Edit",
                [s["id"] for s in filtered],
                key="emp_selected_id",
            )

            if selected_id:
                selected_row = next(s for s in filtered if s["id"] == selected_id)
                st.markdown("---")
                st.subheader(f"Edit Student – ID {selected_row['id']}")

                col_left, col_right = st.columns([2, 1])
                with col_left:
                    updated_data = student_form(existing=selected_row, prefix=f"emp_edit_{selected_row['id']}")
                    if st.button("Update Student (Employee)"):
                        db.update_student(selected_row["id"], updated_data)
                        st.success("Student updated successfully.")
                        st.experimental_rerun()

                with col_right:
                    st.markdown("### Quick View")
                    st.write(f"**Name:** {selected_row['first_name']} {selected_row['last_name']}")
                    st.write(f"**Email:** {selected_row['email']}")
                    st.write(f"**Contact:** {selected_row['contact_number']}")
                    st.write(f"**College:** {selected_row['college_name']} ({selected_row['college_state']})")
                    st.write(f"**Course:** {selected_row['course_name']}")
                    st.write(f"**Year/Semester:** {selected_row['year']} / {selected_row['semester']}")

                    if selected_row.get("image"):
                        try:
                            st.image(selected_row["image"], caption="Student Image", use_column_width=True)
                        except Exception:
                            st.warning("Could not display student image.")

        else:
            st.info("No students found.")


def main() -> None:
    db.init_db()
    init_app_state()
    render_logo_video()

    st.sidebar.title("Navigation")
    if st.session_state.logged_in:
        st.sidebar.write(f"Logged in as **{st.session_state.username}** ({st.session_state.role})")
        logout_button()

        if st.session_state.role == "admin":
            admin_panel()
        elif st.session_state.role == "employee":
            employee_panel()
        else:
            st.error("Unknown role.")
    else:
        login_form()


if __name__ == "__main__":
    main()

