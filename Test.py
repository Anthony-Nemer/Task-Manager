import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime

class Task:
    def __init__(self, name, category, priority, due_date):
        self.name = name
        self.category = category
        self.priority = priority
        self.due_date = due_date

class TaskManagerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Task Manager")

        self.tasks = []

        self.create_widgets()

    def create_widgets(self):
        self.task_frame = tk.Frame(self.master)
        self.task_frame.pack(padx=10, pady=10, anchor="w")

        self.task_label = tk.Label(self.task_frame, text="Task:", font=("Helvetica", 12, "bold"))
        self.task_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.task_entry = tk.Entry(self.task_frame, width=50, font=("Helvetica", 12))
        self.task_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.category_label = tk.Label(self.task_frame, text="Category:", font=("Helvetica", 12, "bold"))
        self.category_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.category_entry = tk.Entry(self.task_frame, width=20, font=("Helvetica", 12))
        self.category_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.priority_label = tk.Label(self.task_frame, text="Priority:", font=("Helvetica", 12, "bold"))
        self.priority_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.priority_combo = ttk.Combobox(self.task_frame, values=["Low", "Medium", "High"], width=17, font=("Helvetica", 12))
        self.priority_combo.current(0)
        self.priority_combo.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.due_date_label = tk.Label(self.task_frame, text="Due Date (YYYY-MM-DD):", font=("Helvetica", 12, "bold"))
        self.due_date_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        self.due_date_entry = tk.Entry(self.task_frame, width=20, font=("Helvetica", 12))
        self.due_date_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.add_button = tk.Button(self.task_frame, text="Add Task", command=self.add_task, font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", relief="raised", padx=10)
        self.add_button.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        self.task_listbox = tk.Listbox(self.master, width=70, height=15, font=("Helvetica", 12))
        self.task_listbox.pack(padx=10, pady=10)

        self.remove_button = tk.Button(self.master, text="Remove Task", command=self.remove_task, font=("Helvetica", 12, "bold"), bg="#f44336", fg="white", relief="raised", padx=10)
        self.remove_button.pack(padx=10, pady=5)

        self.remove_all_button = tk.Button(self.master, text="Remove All", command=self.remove_all_tasks, font=("Helvetica", 12, "bold"), bg="#f44336", fg="white", relief="raised", padx=10)
        self.remove_all_button.pack(padx=10, pady=5)

        # Bind the delete key to the remove_task function
        self.master.bind("<Delete>", lambda event: self.remove_task())

    def add_task(self):
        name = self.task_entry.get().strip()
        category = self.category_entry.get().strip()
        priority = self.priority_combo.get()
        due_date_str = self.due_date_entry.get().strip()

        if name and category and due_date_str:
            try:
                due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
                new_task = Task(name, category, priority, due_date)
                self.tasks.append(new_task)
                self.task_listbox.insert(tk.END, f"{new_task.name} ({new_task.category}) - Due: {new_task.due_date.strftime('%Y-%m-%d')} - Priority: {new_task.priority}")
                self.clear_fields()
            except ValueError:
                messagebox.showerror("Error", "Invalid due date format. Please enter in YYYY-MM-DD format.")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def remove_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task_index = selected_index[0]
            self.task_listbox.delete(task_index)
            del self.tasks[task_index]
        else:
            messagebox.showwarning("Warning", "Please select a task to remove.")

    def remove_all_tasks(self):
        self.task_listbox.delete(0, tk.END)
        self.tasks = []

    def clear_fields(self):
        self.task_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.priority_combo.current(0)
        self.due_date_entry.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
