from sqlalchemy import create_engine, MetaData, insert, delete, update
from sqlalchemy.orm import sessionmaker
import json
import sqlite3
from tkinter import *
from tkinter import messagebox, ttk
with open('config.json', 'w') as file:
    data = {'user':'postgres','password':'Andrey36912'}
    json.dump(data,file)
with open('config.json', 'r') as file:
    data = json.load(file)
    db_user = data['user']
    db_password = data['password']

db_url = f'postgresql+psycopg2://{db_user}:{db_password}@localhost:5432/Academy'
engine = create_engine(db_url)

metadata = MetaData()
metadata.reflect(bind=engine)

connection = engine.connect()



class AcademyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Academy Database Management")

        self.create_widgets()

    def create_widgets(self):
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(expand=1, fill="both")

        self.add_tab = Frame(self.tabs)
        self.update_tab = Frame(self.tabs)
        self.delete_tab = Frame(self.tabs)
        self.reports_tab = Frame(self.tabs)

        self.tabs.add(self.add_tab, text="Add Records")
        self.tabs.add(self.update_tab, text="Update Records")
        self.tabs.add(self.delete_tab, text="Delete Records")
        self.tabs.add(self.reports_tab, text="Generate Reports")

        self.create_add_tab()
        self.create_update_tab()
        self.create_delete_tab()
        self.create_reports_tab()

    def create_add_tab(self):
        Label(self.add_tab, text="Select Table to Add Record").grid(row=0, column=0, padx=10, pady=10)

        self.add_table_option = StringVar()
        self.add_table_option.set("Faculties")

        add_options = ["Faculties", "Departments", "Groups", "Curators", "GroupsCurators", "Subjects", "Teachers",
                       "Lectures", "GroupsLectures"]
        self.add_table_menu = OptionMenu(self.add_tab, self.add_table_option, *add_options)
        self.add_table_menu.grid(row=0, column=1, padx=10, pady=10)

        self.add_button = Button(self.add_tab, text="Add Record", command=self.add_record)
        self.add_button.grid(row=1, column=0, columnspan=2, pady=10)

    def create_update_tab(self):
        Label(self.update_tab, text="Select Table to Update Record").grid(row=0, column=0, padx=10, pady=10)

        self.update_table_option = StringVar()
        self.update_table_option.set("Faculties")

        update_options = ["Faculties", "Departments", "Groups", "Curators", "GroupsCurators", "Subjects", "Teachers",
                          "Lectures", "GroupsLectures"]
        self.update_table_menu = OptionMenu(self.update_tab, self.update_table_option, *update_options)
        self.update_table_menu.grid(row=0, column=1, padx=10, pady=10)

        self.update_button = Button(self.update_tab, text="Update Record", command=self.update_record)
        self.update_button.grid(row=1, column=0, columnspan=2, pady=10)

    def create_delete_tab(self):
        Label(self.delete_tab, text="Select Table to Delete Record").grid(row=0, column=0, padx=10, pady=10)

        self.delete_table_option = StringVar()
        self.delete_table_option.set("Faculties")

        delete_options = ["Faculties", "Departments", "Groups", "Curators", "GroupsCurators", "Subjects", "Teachers",
                          "Lectures", "GroupsLectures"]
        self.delete_table_menu = OptionMenu(self.delete_tab, self.delete_table_option, *delete_options)
        self.delete_table_menu.grid(row=0, column=1, padx=10, pady=10)

        self.delete_button = Button(self.delete_tab, text="Delete Record", command=self.delete_record)
        self.delete_button.grid(row=1, column=0, columnspan=2, pady=10)

    def create_reports_tab(self):
        Label(self.reports_tab, text="Select Report to Generate").grid(row=0, column=0, padx=10, pady=10)

        self.report_option = StringVar()
        self.report_option.set("Groups Information")

        report_options = [
            "Groups Information",
            "Teachers Information",
            "Departments Information",
            "Teachers Lectures in Group",
            "Departments and Groups",
            "Department with Max Groups",
            "Department with Min Groups",
            "Subjects by Teacher",
            "Departments with Subject",
            "Groups in Faculty",
            "Max Lectures by Subject",
            "Min Lectures by Subject"
        ]
        self.report_menu = OptionMenu(self.reports_tab, self.report_option, *report_options)
        self.report_menu.grid(row=0, column=1, padx=10, pady=10)

        self.report_button = Button(self.reports_tab, text="Generate Report", command=self.generate_report)
        self.report_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.report_output = Text(self.reports_tab, width=80, height=20)
        self.report_output.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def add_record(self):
        table = self.add_table_option.get()
        self.show_record_entry_form(table, "add")

    def update_record(self):
        table = self.update_table_option.get()
        self.show_record_entry_form(table, "update")

    def delete_record(self):
        table = self.delete_table_option.get()
        self.show_record_entry_form(table, "delete")

    def show_record_entry_form(self, table, operation):
        record_window = Toplevel(self.root)
        record_window.title(f"{operation.capitalize()} Record in {table}")

        if table == "Faculties":
            fields = ["Financing", "Name"]
        elif table == "Departments":
            fields = ["Financing", "Name", "FacultyId"]
        elif table == "Groups":
            fields = ["Name", "Year", "DepartmentId"]
        elif table == "Curators":
            fields = ["Name", "Surname"]
        elif table == "GroupsCurators":
            fields = ["CuratorId", "GroupId"]
        elif table == "Subjects":
            fields = ["Name"]
        elif table == "Teachers":
            fields = ["Name", "Surname", "Salary"]
        elif table == "Lectures":
            fields = ["LectureRoom", "SubjectId", "TeacherId"]
        elif table == "GroupsLectures":
            fields = ["GroupId", "LectureId"]

        entries = {}
        for i, field in enumerate(fields):
            Label(record_window, text=field).grid(row=i, column=0, padx=10, pady=10)
            entry = Entry(record_window)
            entry.grid(row=i, column=1, padx=10, pady=10)
            entries[field] = entry

        if operation == "add":
            Button(record_window, text="Add", command=lambda: self.execute_add(entries, table)).grid(row=len(fields),
                                                                                                     column=0,
                                                                                                     columnspan=2,
                                                                                                     pady=10)
        elif operation == "update":
            Label(record_window, text="ID").grid(row=len(fields), column=0, padx=10, pady=10)
            id_entry = Entry(record_window)
            id_entry.grid(row=len(fields), column=1, padx=10, pady=10)
            entries["ID"] = id_entry
            Button(record_window, text="Update", command=lambda: self.execute_update(entries, table)).grid(
                row=len(fields) + 1, column=0, columnspan=2, pady=10)
        elif operation == "delete":
            Label(record_window, text="ID").grid(row=0, column=0, padx=10, pady=10)
            id_entry = Entry(record_window)
            id_entry.grid(row=0, column=1, padx=10, pady=10)
            entries["ID"] = id_entry
            Button(record_window, text="Delete", command=lambda: self.execute_delete(entries, table)).grid(row=1,
                                                                                                           column=0,
                                                                                                           columnspan=2,
                                                                                                           pady=10)

    def execute_add(self, entries, table):
        values = [entry.get() for entry in entries.values()]
        columns = ', '.join(entries.keys())
        placeholders = ', '.join(['?' for _ in entries])

        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        conn = sqlite3.connect('academy.db')
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Record added to {table}")

    def execute_update(self, entries, table):
        id_value = entries.pop("ID").get()
        values = [entry.get() for entry in entries.values()]
        set_clause = ', '.join([f"{key} = ?" for key in entries])

        query = f"UPDATE {table} SET {set_clause} WHERE Id = ?"
        conn = sqlite3.connect('academy.db')
        cursor = conn.cursor()
        cursor.execute(query, values + [id_value])
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Record updated in {table}")

    def execute_delete(self, entries, table):
        id_value = entries["ID"].get()

        query = f"DELETE FROM {table} WHERE Id = ?"
        conn = sqlite3.connect('academy.db')
        cursor = conn.cursor()
        cursor.execute(query, (id_value,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Record deleted from {table}")

    def generate_report(self):
        report_type = self.report_option.get()
        query = ""

        if report_type == "Groups Information":
            query = "SELECT * FROM Groups"
        elif report_type == "Teachers Information":
            query = "SELECT * FROM Teachers"
        elif report_type == "Departments Information":
            query = "SELECT * FROM Departments"
        elif report_type == "Teachers Lectures in Group":
            group_id = int(input("Enter Group ID: "))
            query = f"SELECT Teachers.Name, Teachers.Surname FROM Teachers JOIN Lectures ON Teachers.Id = Lectures.TeacherId JOIN GroupsLectures ON Lectures.Id = GroupsLectures.LectureId WHERE GroupsLectures.GroupId = {group_id}"
        elif report_type == "Departments and Groups":
            query = "SELECT Departments.Name, Groups.Name FROM Departments JOIN Groups ON Departments.Id = Groups.DepartmentId"
        elif report_type == "Department with Max Groups":
            query = "SELECT Departments.Name, COUNT(Groups.Id) AS GroupCount FROM Departments JOIN Groups ON Departments.Id = Groups.DepartmentId GROUP BY Departments.Id ORDER BY GroupCount DESC LIMIT 1"
        elif report_type == "Department with Min Groups":
            query = "SELECT Departments.Name, COUNT(Groups.Id) AS GroupCount FROM Departments JOIN Groups ON Departments.Id = Groups.DepartmentId GROUP BY Departments.Id ORDER BY GroupCount ASC LIMIT 1"
        elif report_type == "Subjects by Teacher":
            teacher_id = int(input("Enter Teacher ID: "))
            query = f"SELECT Subjects.Name FROM Subjects JOIN Lectures ON Subjects.Id = Lectures.SubjectId WHERE Lectures.TeacherId = {teacher_id}"
        elif report_type == "Departments with Subject":
            subject_id = int(input("Enter Subject ID: "))
            query = f"SELECT Departments.Name FROM Departments JOIN Groups ON Departments.Id = Groups.DepartmentId JOIN GroupsLectures ON Groups.Id = GroupsLectures.GroupId JOIN Lectures ON GroupsLectures.LectureId = Lectures.Id WHERE Lectures.SubjectId = {subject_id}"
        elif report_type == "Groups in Faculty":
            faculty_id = int(input("Enter Faculty ID: "))
            query = f"SELECT Groups.Name FROM Groups JOIN Departments ON Groups.DepartmentId = Departments.Id WHERE Departments.FacultyId = {faculty_id}"
        elif report_type == "Max Lectures by Subject":
            query = "SELECT Subjects.Name, COUNT(Lectures.Id) AS LectureCount FROM Subjects JOIN Lectures ON Subjects.Id = Lectures.SubjectId GROUP BY Subjects.Id ORDER BY LectureCount DESC LIMIT 1"
        elif report_type == "Min Lectures by Subject":
            query = "SELECT Subjects.Name, COUNT(Lectures.Id) AS LectureCount FROM Subjects JOIN Lectures ON Subjects.Id = Lectures.SubjectId GROUP BY Subjects.Id ORDER BY LectureCount ASC LIMIT 1"

        conn = sqlite3.connect('academy.db')
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()

        self.report_output.delete(1.0, END)
        for row in results:
            self.report_output.insert(END, str(row) + "\n")


if __name__ == "__main__":
    root = Tk()
    app = AcademyApp(root)
    root.mainloop()
def save_report(self):
    report_text = self.report_output.get(1.0, END)
    with open("report.txt", "w") as file:
        file.write(report_text)
    messagebox.showinfo("Success", "Report saved to report.txt")


def login(self):
    login_window = Toplevel(self.root)
    login_window.title("Login")

    Label(login_window, text="Username").grid(row=0, column=0, padx=10, pady=10)
    username_entry = Entry(login_window)
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    Label(login_window, text="Password").grid(row=1, column=0, padx=10, pady=10)
    password_entry = Entry(login_window, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    def verify_login():
        username = username_entry.get()
        password = password_entry.get()

        # Simple verification, can be expanded for more security
        if username == "admin" and password == "admin":
            self.access_level = "admin"
        elif username == "user" and password == "user":
            self.access_level = "user"
        else:
            self.access_level = "guest"

        login_window.destroy()
        self.update_access_level()

    Button(login_window, text="Login", command=verify_login).grid(row=2, column=0, columnspan=2, pady=10)


def update_access_level(self):
    if self.access_level == "admin":
        self.add_button.config(state=NORMAL)
        self.update_button.config(state=NORMAL)
        self.delete_button.config(state=NORMAL)
    elif self.access_level == "user":
        self.add_button.config(state=DISABLED)
        self.update_button.config(state=DISABLED)
        self.delete_button.config(state=DISABLED)
    else:
        self.add_button.config(state=DISABLED)
        self.update_button.config(state=DISABLED)
        self.delete_button.config(state=DISABLED)
        self.report_button.config(state=DISABLED)
