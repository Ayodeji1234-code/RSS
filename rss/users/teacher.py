import streamlit as st
from users.user import User
from operations.assessment import record_assessment, view_assessments
from operations.attendance import view_attendance, record_attendance
from operations.schedule import view_teacher_schedule
from operations.pairing import assigned_students, load_users   # ✅ make sure this points to your user utils


def get_fullname_from_username(username):
    """Return the FULL NAME of a teacher given their username."""
    users = load_users()
    for fullname, info in users.items():
        if info.get("username") == username and info.get("role", "").lower() == "teacher":
            return fullname
    return username  # fallback if not found


class Teacher(User):
    def __init__(self, username):
        fullname = get_fullname_from_username(username)
        super().__init__(username, fullname, role="Teacher")

    def get_actions(self):
        return [
            "Profile",
            "View Schedule",
            "My Students",
            "Record Assessment",
            "View Assessment",
            "Record Attendance",
            "View Attendance",
            "Logout"
        ]

    def action(self, choice):
        if choice == "View Schedule":
            view_teacher_schedule(self.name)   # ✅ full name like "Okenla Qahar"
        elif choice == "My Students":    
            assigned_students(self.name)       # ✅ full name
        elif choice == "Record Assessment":
            record_assessment(self.name)
        elif choice == "View Assessment":
            view_assessments()
        elif choice == "Record Attendance":
            record_attendance(self.name)       # ✅ matches student["teacher"]
        elif choice == "View Attendance":
            view_attendance()
