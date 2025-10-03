import streamlit as st
import json
import os
import pandas as pd

USER_FILE = "users.json"
TIMETABLE_FILE = "timetable.json"

# --- helpers ---
def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

def load_timetable():
    if not os.path.exists(TIMETABLE_FILE):
        return {}
    with open(TIMETABLE_FILE, "r") as f:
        return json.load(f)

def save_timetable(timetable):
    with open(TIMETABLE_FILE, "w") as f:
        json.dump(timetable, f, indent=4)


def add_timetable_entry():
    st.subheader("🗓️ Create Schedule")

    users = load_users()  # 🔹 load users to check teacher assignment

    with st.form("schedule_form", clear_on_submit=True):
        # --- Student input ---
        student_name = st.text_input("Enter student name:", key="student_input")

        # --- Auto-fill teacher name if student exists ---
        assigned_teacher = ""
        if student_name and student_name in users and "teacher" in users[student_name]:
            assigned_teacher = users[student_name]["teacher"]

        # --- Teacher name field (auto-filled if available) ---
        teacher_name = st.text_input("Assigned Teacher", value=assigned_teacher, key="teacher_input")

        # --- Other inputs ---
        day = st.selectbox("Select Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], key="day_input")
        time_slot = st.text_input("Enter Time Slot (e.g. 10:00 AM - 11:00 AM)", key="time_input")

        submitted = st.form_submit_button("Save Schedule")

    if submitted:
        if not student_name.strip():
            st.error("⚠️ Please enter a student name.")
            return
        if not teacher_name.strip():
            st.error("⚠️ No teacher assigned for this student.")
            return
        if not day.strip():
            st.error("⚠️ Please select a valid day.")
            return
        if not time_slot.strip():
            st.error("⚠️ Please enter a valid time slot.")
            return
        # --- Ensure timetable file exists ---
        if not os.path.exists(TIMETABLE_FILE):
            timetable = {"students": {}, "teachers": {}}
        else:
            with open(TIMETABLE_FILE, "r") as f:
                timetable = json.load(f)

        # --- Student schedule ---
        if student_name not in timetable["students"]:
            timetable["students"][student_name] = []

        timetable["students"][student_name].append({
            "day": day,
            "time": time_slot,
            "teacher": teacher_name
        })

        # --- Teacher schedule ---
        if teacher_name not in timetable["teachers"]:
            timetable["teachers"][teacher_name] = []

        timetable["teachers"][teacher_name].append({
            "day": day,
            "time": time_slot,
            "student": student_name
        })

        # --- Save back ---
        with open(TIMETABLE_FILE, "w") as f:
            json.dump(timetable, f, indent=4)

        st.success(f"✅ Added {student_name} with {teacher_name} on {day} at {time_slot}")


def view_student_timetable(student_name):
    if not os.path.exists(TIMETABLE_FILE):
        st.warning("⚠️ No timetable file found yet.")
        return

    with open(TIMETABLE_FILE, "r") as f:
        timetable = json.load(f)

    student_records = timetable.get("students", {}).get(student_name, [])

    if not student_records:
        st.warning(f"⚠️ No timetable found for {student_name}")
        return

    rows = [
        {"Day": record.get("day", "N/A"),
         "Time": record.get("time", "N/A"),
         "Teacher": record.get("teacher", "N/A")}
        for record in student_records
    ]

    df = pd.DataFrame(rows)
    df.index = df.index + 1
    st.subheader(f"📅 Timetable for {student_name}")
    st.dataframe(df, use_container_width=True)


def view_teacher_schedule(teacher_name):
    if not os.path.exists(TIMETABLE_FILE):
        st.warning("⚠️ No timetable file found yet.")
        return

    with open(TIMETABLE_FILE, "r") as f:
        timetable = json.load(f)

    teacher_records = timetable.get("teachers", {}).get(teacher_name, [])
    if not teacher_records:
        st.warning(f"📂 No timetable found for {teacher_name}")
        return

    rows = [
        {"Day": slot.get("day", ""),
         "Time": slot.get("time", ""),
         "Student": slot.get("student", "")}
        for slot in teacher_records
    ]

    df = pd.DataFrame(rows)
    df.index = df.index + 1
    st.subheader(f"📅 Schedule for {teacher_name}")
    st.dataframe(df, use_container_width=True)

def view_all_schedules():
    """Admin views all schedules (students + teachers)."""
    if not os.path.exists(TIMETABLE_FILE):
        st.info("No schedules found yet.")
        return

    with open(TIMETABLE_FILE, "r") as f:
        timetable = json.load(f)

    rows = []
    index = 1
    for student, schedules in timetable.get("students", {}).items():
        first_row = True
        for sched in schedules:
            rows.append({
                "Index": index if first_row else "",
                "Student": student if first_row else "",
                "Day": sched["day"],
                "Time": sched["time"],
                "Teacher": sched["teacher"]
            })
            first_row = False
        index += 1

    # Convert to DataFrame
    df = pd.DataFrame(rows)
    if "Index" in df.columns:
        df.set_index("Index", inplace=True)

    st.subheader("📅 All Schedules")
    st.dataframe(df, use_container_width=True)

