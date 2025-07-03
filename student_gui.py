import tkinter as tk
from tkinter import messagebox, ttk

FILE = "students.txt"

# ------------------ File Operations ------------------ #
def load_students():
    try:
        with open(FILE, "r") as f:
            return [line.strip().split(",") for line in f if line.strip()]
    except FileNotFoundError:
        return []

def save_students(students):
    with open(FILE, "w") as f:
        for student in students:
            f.write(",".join(student) + "\n")

# ------------------ GUI Functions ------------------ #
def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    for student in load_students():
        tree.insert("", "end", values=student)

def add_student():
    sid = entry_id.get().strip()
    name = entry_name.get().strip()
    age = entry_age.get().strip()
    dept = entry_dept.get().strip()

    if not (sid and name and age and dept):
        messagebox.showwarning("Input Error", "All fields are required.")
        return

    students = load_students()
    for s in students:
        if s[0] == sid:
            messagebox.showerror("Duplicate ID", "Student ID already exists.")
            return

    students.append([sid, name, age, dept])
    save_students(students)
    refresh_table()
    clear_fields()
    messagebox.showinfo("Success", "Student added successfully!")

def select_student(event):
    selected = tree.focus()
    if selected:
        values = tree.item(selected, 'values')
        entry_id.delete(0, tk.END)
        entry_name.delete(0, tk.END)
        entry_age.delete(0, tk.END)
        entry_dept.delete(0, tk.END)
        entry_id.insert(0, values[0])
        entry_name.insert(0, values[1])
        entry_age.insert(0, values[2])
        entry_dept.insert(0, values[3])
        entry_id.config(state='disabled')

def update_student():
    sid = entry_id.get().strip()
    name = entry_name.get().strip()
    age = entry_age.get().strip()
    dept = entry_dept.get().strip()

    students = load_students()
    for student in students:
        if student[0] == sid:
            student[1] = name
            student[2] = age
            student[3] = dept
            save_students(students)
            refresh_table()
            clear_fields()
            entry_id.config(state='normal')
            messagebox.showinfo("Updated", "Student updated successfully!")
            return

    messagebox.showerror("Not Found", "Student ID not found.")

def delete_student():
    sid = entry_id.get().strip()
    students = load_students()
    new_students = [s for s in students if s[0] != sid]

    if len(new_students) == len(students):
        messagebox.showerror("Not Found", "Student ID not found.")
        return

    save_students(new_students)
    refresh_table()
    clear_fields()
    entry_id.config(state='normal')
    messagebox.showinfo("Deleted", "Student deleted successfully!")

def clear_fields():
    entry_id.config(state='normal')
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_dept.delete(0, tk.END)

# ------------------ GUI Layout ------------------ #
root = tk.Tk()
root.title("Student Record Manager")

# Labels and Entry Fields
tk.Label(root, text="ID").grid(row=0, column=0)
tk.Label(root, text="Name").grid(row=0, column=2)
tk.Label(root, text="Age").grid(row=1, column=0)
tk.Label(root, text="Department").grid(row=1, column=2)

entry_id = tk.Entry(root)
entry_name = tk.Entry(root)
entry_age = tk.Entry(root)
entry_dept = tk.Entry(root)

entry_id.grid(row=0, column=1)
entry_name.grid(row=0, column=3)
entry_age.grid(row=1, column=1)
entry_dept.grid(row=1, column=3)

# Buttons
tk.Button(root, text="Add", width=12, command=add_student).grid(row=2, column=0, pady=10)
tk.Button(root, text="Update", width=12, command=update_student).grid(row=2, column=1)
tk.Button(root, text="Delete", width=12, command=delete_student).grid(row=2, column=2)
tk.Button(root, text="Clear", width=12, command=clear_fields).grid(row=2, column=3)

# Table (Treeview)
cols = ("ID", "Name", "Age", "Department")
tree = ttk.Treeview(root, columns=cols, show='headings')
for col in cols:
    tree.heading(col, text=col)
tree.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

tree.bind("<<TreeviewSelect>>", select_student)

# Initialize table
refresh_table()

# Start the app
root.mainloop()
