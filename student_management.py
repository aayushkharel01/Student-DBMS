import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Bronite@2025",
    database="student_db"
)
cursor = conn.cursor()

# Function to add a student
def add_student():
    name = entry_name.get()
    age = entry_age.get()
    grade = entry_grade.get()
    email = entry_email.get()

    if name and age and grade and email:
        try:
            cursor.execute("INSERT INTO students (name, age, grade, email) VALUES (%s, %s, %s, %s)", 
                           (name, age, grade, email))
            conn.commit()
            messagebox.showinfo("Success", "Student Added Successfully!")
            view_students()
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "Email already exists!")
    else:
        messagebox.showwarning("Error", "All fields are required!")

# Function to view students
def view_students():
    tree.delete(*tree.get_children())  # Clear table
    cursor.execute("SELECT * FROM students")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

# Function to delete a student
def delete_student():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select a student to delete!")
        return

    student_id = tree.item(selected)['values'][0]
    cursor.execute("DELETE FROM students WHERE id=%s", (student_id,))
    conn.commit()
    messagebox.showinfo("Success", "Student Deleted!")
    view_students()

# Function to update a student
def update_student():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select a student to update!")
        return

    student_id = tree.item(selected)['values'][0]
    new_name = entry_name.get()
    new_age = entry_age.get()
    new_grade = entry_grade.get()
    new_email = entry_email.get()

    if new_name and new_age and new_grade and new_email:
        cursor.execute("UPDATE students SET name=%s, age=%s, grade=%s, email=%s WHERE id=%s", 
                       (new_name, new_age, new_grade, new_email, student_id))
        conn.commit()
        messagebox.showinfo("Success", "Student Updated!")
        view_students()
    else:
        messagebox.showwarning("Error", "All fields are required!")

# GUI Setup
root = tk.Tk()
root.title("Student Management System")
root.geometry("600x500")

# Input Fields
tk.Label(root, text="Name").grid(row=0, column=0)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1)

tk.Label(root, text="Age").grid(row=1, column=0)
entry_age = tk.Entry(root)
entry_age.grid(row=1, column=1)

tk.Label(root, text="Grade").grid(row=2, column=0)
entry_grade = tk.Entry(root)
entry_grade.grid(row=2, column=1)

tk.Label(root, text="Email").grid(row=3, column=0)
entry_email = tk.Entry(root)
entry_email.grid(row=3, column=1)

# Buttons
tk.Button(root, text="Add Student", command=add_student).grid(row=4, column=0, columnspan=2, pady=10)
tk.Button(root, text="Update Student", command=update_student).grid(row=5, column=0, columnspan=2, pady=10)
tk.Button(root, text="Delete Student", command=delete_student).grid(row=6, column=0, columnspan=2, pady=10)

# Table to Display Data
tree = ttk.Treeview(root, columns=("ID", "Name", "Age", "Grade", "Email"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.heading("Grade", text="Grade")
tree.heading("Email", text="Email")
tree.grid(row=7, column=0, columnspan=2)

view_students()
root.mainloop()
