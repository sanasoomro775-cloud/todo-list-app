
import tkinter as tk
from tkinter import messagebox
import json
import os

# Colors
NAVY = "#142B4A"
BLUE = "#2463A6"
LIGHT_BLUE = "#DCEBFA"
WHITE = "#FFFFFF"
BG = "#F3F7FC"
TEXT = "#26374A"

# Save file in the same folder as this Python file
DATA_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "tasks.json"
)


def save_tasks():
    """Save all tasks to a JSON file."""
    tasks = list(task_list.get(0, tk.END))

    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(tasks, file, ensure_ascii=False, indent=4)
    except OSError as error:
        messagebox.showerror(
            "Save Error",
            f"Tasks could not be saved:\n{error}"
        )


def load_tasks():
    """Load previously saved tasks."""
    if not os.path.exists(DATA_FILE):
        return

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            tasks = json.load(file)

        if not isinstance(tasks, list) or not all(
            isinstance(task, str) for task in tasks
        ):
            raise ValueError("Invalid task data.")

        task_list.delete(0, tk.END)

        for task in tasks:
            task_list.insert(tk.END, task)

    except (OSError, json.JSONDecodeError, ValueError) as error:
        messagebox.showerror(
            "Load Error",
            f"Saved tasks could not be loaded:\n{error}"
        )


def add_task():
    task = task_entry.get().strip()

    if not task:
        messagebox.showwarning(
            "Empty Task",
            "Please enter a task."
        )
        return

    task_list.insert(tk.END, "  " + task)
    task_entry.delete(0, tk.END)
    save_tasks()


def delete_task():
    selected = task_list.curselection()

    if not selected:
        messagebox.showinfo(
            "Select Task",
            "Please select a task first."
        )
        return

    task_list.delete(selected[0])
    save_tasks()


def complete_task():
    selected = task_list.curselection()

    if not selected:
        messagebox.showinfo(
            "Select Task",
            "Please select a task first."
        )
        return

    index = selected[0]
    task = task_list.get(index).strip()

    if not task.startswith("✓ "):
        task_list.delete(index)
        task_list.insert(index, "  ✓ " + task)
        save_tasks()


# Main window
root = tk.Tk()
root.title("MM Digital Hub | To-Do List")
root.geometry("560x600")
root.configure(bg=BG)
root.resizable(False, False)

# Header
header = tk.Frame(root, bg=NAVY, height=115)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="MY TO-DO LIST",
    font=("Segoe UI", 23, "bold"),
    bg=NAVY,
    fg=WHITE
).pack(pady=(22, 3))

tk.Label(
    header,
    text="Plan your day. Focus on what matters.",
    font=("Segoe UI", 10),
    bg=NAVY,
    fg=LIGHT_BLUE
).pack()

# Main content
content = tk.Frame(root, bg=BG, padx=30, pady=22)
content.pack(fill="both", expand=True)

tk.Label(
    content,
    text="Add a new task",
    font=("Segoe UI", 12, "bold"),
    bg=BG,
    fg=TEXT
).pack(anchor="w", pady=(0, 8))

# Input field
task_entry = tk.Entry(
    content,
    font=("Segoe UI", 12),
    bg=WHITE,
    fg=TEXT,
    insertbackground=NAVY,
    relief="solid",
    bd=1
)
task_entry.pack(fill="x", ipady=11, pady=(0, 12))
task_entry.bind("<Return>", lambda event: add_task())

# Add button
tk.Button(
    content,
    text="+   Add Task",
    command=add_task,
    font=("Segoe UI", 11, "bold"),
    bg=BLUE,
    fg=WHITE,
    activebackground=NAVY,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    pady=10
).pack(fill="x")

tk.Label(
    content,
    text="YOUR TASKS",
    font=("Segoe UI", 10, "bold"),
    bg=BG,
    fg=TEXT
).pack(anchor="w", pady=(22, 8))

# Task list
list_frame = tk.Frame(
    content,
    bg=WHITE,
    bd=1,
    relief="solid"
)
list_frame.pack(fill="both", expand=True)

task_list = tk.Listbox(
    list_frame,
    font=("Segoe UI", 11),
    bg=WHITE,
    fg=TEXT,
    selectbackground=LIGHT_BLUE,
    selectforeground=NAVY,
    relief="flat",
    bd=0,
    activestyle="none",
    height=9
)
task_list.pack(fill="both", expand=True, padx=8, pady=8)

# Action buttons
actions = tk.Frame(content, bg=BG)
actions.pack(fill="x", pady=(12, 0))

tk.Button(
    actions,
    text="✓  Complete",
    command=complete_task,
    font=("Segoe UI", 10, "bold"),
    bg=LIGHT_BLUE,
    fg=NAVY,
    relief="flat",
    cursor="hand2",
    pady=9
).pack(side="left", fill="x", expand=True, padx=(0, 5))

tk.Button(
    actions,
    text="Delete Task",
    command=delete_task,
    font=("Segoe UI", 10, "bold"),
    bg=NAVY,
    fg=WHITE,
    relief="flat",
    cursor="hand2",
    pady=9
).pack(side="left", fill="x", expand=True, padx=(5, 0))

# Footer
tk.Label(
    root,
    text="Built with Python  |  MM Digital Hub",
    font=("Segoe UI", 9),
    bg=BG,
    fg="#64748B"
).pack(pady=(0, 12))

# Load saved tasks when app starts
load_tasks()

root.mainloop()
