import sys
sys.path.append(r'C:\Users\user\Documents\python')
from users.user import User
from operations.attendance import view_my_attendance
from operations.schedule import view_student_timetable
from operations.pairing import assigned_teacher
from operations.assessment import view_my_assessments
import streamlit as st


class Student(User):
    def __init__(self, name, username, stage):
        super().__init__(username, name, role='Student')
        self.stage = stage

    def get_actions(self):
        """Return list of actions available to Student"""
        return [
            "Profile",
            "My Teacher",
            "View Time Table",
            "View My Attendance",
            "View My Assessment",
            "Logout"
        ]

    def action(self, choice):
        if choice == "My Teacher":
            assigned_teacher(self.name)

        elif choice == "View Time Table":
            view_student_timetable(self.name)   # ✅ full name is key in timetable

        elif choice == "View My Attendance":
            view_my_attendance(self.name)      # ✅ full name is key in attendance

        elif choice == "View My Assessment":
            view_my_assessments(self.name)  # ✅ username + full name
