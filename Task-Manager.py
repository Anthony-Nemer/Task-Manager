#Project by Anthony Nemer, 60282
#        and Jennifer El fakir, 60396.


import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import os
from tkinter import PhotoImage
from PIL import Image, ImageTk

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("600x600")
        self.root.resizable(True, True)

        self.TaskList = []
        self.CompletedTaskList = []
        self.TaskID = 1  # Counter for task IDs


        
        pathOfThisCode = os.path.dirname(os.path.abspath(__file__))
        checkImage = os.path.join(pathOfThisCode, "icon.png")
        if os.path.exists(checkImage):
            image = Image.open(checkImage)
            image = image.resize((50, 50))
            self.logo_image = ImageTk.PhotoImage(image)
        else:
            self.logo_image = None


        style = ttk.Style()
        #buttons
        style.configure("TButton", font=("Helvetica", 10))
        #labels
        style.configure("TLabel", font=("Helvetica", 12))
        #entries
        style.configure("TEntry", font=("Helvetica", 12))


        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(expand=True, fill=tk.BOTH)


        #load the logo image in the top of the frame
        if self.logo_image:
            self.logo_label = tk.Label(main_frame, image=self.logo_image)
            self.logo_label.pack(side=tk.TOP, padx=10, pady=10)


        # Ongoing tasks label
        self.OngoingTasksLabel = ttk.Label(main_frame, text="Ongoing Tasks", font=("Helvetica", 14))
        self.OngoingTasksLabel.pack()

        # Creating a listbox for ongoing tasks with a scrollbar
        self.TaskListBox = tk.Listbox(main_frame, selectmode=tk.MULTIPLE, font=("Helvetica", 12), height=10)
        self.TaskListBox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
        
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.TaskListBox.yview)
        self.TaskListBox.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Entry to add tasks
        entry_frame = ttk.Frame(root, padding="10")
        entry_frame.pack(fill=tk.X)

        self.addTask_label = ttk.Label(entry_frame, text="Enter new Task:", font=("Helvetica", 12))
        self.addTask_label.pack(side=tk.LEFT, padx=5)    
        self.EnterTask = ttk.Entry(entry_frame, width=30)
        self.EnterTask.pack(side=tk.LEFT, padx=5)
        
        self.AddTask = ttk.Button(entry_frame, text="Add Task \u2795", command=self.Add_Task)
        self.AddTask.pack(side=tk.LEFT, padx=5)

        # Buttons frame
        buttons_frame = ttk.Frame(root, padding="10")
        buttons_frame.pack(fill=tk.X)

        self.DeleteTask = ttk.Button(buttons_frame, text="Delete Task \u2716", command=self.Delete_Task)
        self.DeleteTask.pack(side=tk.LEFT, padx=5)
        
        self.CompleteTask = ttk.Button(buttons_frame, text="Mark as Complete ✔", command=self.Marked_Completed)
        self.CompleteTask.pack(side=tk.LEFT, padx=5)

        # Export button
        self.ExportButton = ttk.Button(buttons_frame, text="Export Completed Tasks \u2192", command=self.Export_Completed_Tasks)
        self.ExportButton.pack(side=tk.LEFT, padx=5)

        # frame for completed tasks
        completed_frame = ttk.Frame(root, padding="10")
        completed_frame.pack(expand=True, fill=tk.BOTH)

        # Completed tasks label
        self.CompletedTasksLabel = ttk.Label(completed_frame, text="Completed Tasks", font=("Helvetica", 14))
        self.CompletedTasksLabel.pack()

        # Creating a listbox for completed tasks with a scrollbar
        self.CompletedTaskListBox = tk.Listbox(completed_frame, font=("Helvetica", 12), height=10)
        self.CompletedTaskListBox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
        
        completed_scrollbar = ttk.Scrollbar(completed_frame, orient=tk.VERTICAL, command=self.CompletedTaskListBox.yview)
        self.CompletedTaskListBox.config(yscrollcommand=completed_scrollbar.set)
        completed_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def Add_Task(self):
        new_task = self.EnterTask.get()
        if not new_task:
            messagebox.showinfo("Add New Task", "Enter a task to add.")
        elif new_task:
            timestamp = datetime.now().strftime("%I:%M:%S %p")
            task_with_id = f"#{self.TaskID}: {new_task} (Added: {timestamp})"
            self.TaskList.append(task_with_id)
            self.TaskID += 1
            self.Update_Task_List()
            self.EnterTask.delete(0, tk.END)

    def Delete_Task(self):
        selections = self.TaskListBox.curselection()
        if not selections:
            messagebox.showinfo("Delete Task", "No task selected.")          
        elif selections:
            for index in reversed(selections):
                del self.TaskList[index]
            self.Update_Task_List()

    def Marked_Completed(self):
        selections = self.TaskListBox.curselection()
        if not selections:
            messagebox.showinfo("Mark as complete", "No task selected.") 
        elif selections:
            for index in reversed(selections):
                task = self.TaskList.pop(index)
                if not task.startswith('\u2713'):
                    completion_time = datetime.now().strftime("%I:%M:%S %p")
                    completed_task = f'\u2713 {task} (Completed: {completion_time})'
                    self.CompletedTaskList.append(completed_task)
            self.Update_Task_List()
            self.Update_Completed_Task_List()
            self.TaskListBox.selection_clear(0, tk.END)

    def Update_Task_List(self):
        self.TaskListBox.delete(0, tk.END)
        for task in self.TaskList:
            self.TaskListBox.insert(tk.END, task)

    def Update_Completed_Task_List(self):
        self.CompletedTaskListBox.delete(0, tk.END)
        for task in self.CompletedTaskList:
            self.CompletedTaskListBox.insert(tk.END, task)
            self.CompletedTaskListBox.itemconfig(tk.END, {'fg': 'gray'})

    def Export_Completed_Tasks(self):
        if not self.CompletedTaskList:
            messagebox.showerror("Export Completed Tasks", "No completed tasks to export.")
            return
        try:
            pathOfThisCode = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(pathOfThisCode, "completed_tasks.txt")
            with open(file_path, "w", encoding="utf-8") as file:
                for task in self.CompletedTaskList:
                    file.write(task + "\n")
            messagebox.showinfo("Export Completed Tasks", f"Completed tasks successfully exported to '{file_path}'.")
        except Exception as e:
            messagebox.showerror("Export Completed Tasks", f"Error: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()
