import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import calendar
import json
import os

DATA_FILE = "calendar_data.json"

class SimpleCalendar(tk.Tk):

    def tasks_prioritizer_gui(self):
        def on_submit():
            # Weights for Importance, Urgency, and Significance
            w1, w2, w3 = 0.5, 0.3, 0.2

            importance = float(importance_entry.get())
            days_till_deadline = float(days_till_deadline_entry.get())
            urgency = 1 - (days_till_deadline / 7)
            hours_required = float(hours_required_entry.get())
            significance = hours_required / 24
            priority_score = w1 * importance + w2 * urgency + w3 * significance

            # Add to tasks dictionary
            task_name = task_entry.get()
            tasks[task_name] = priority_score

            # Clear the entry
            task_entry.delete(0, tk.END)

        tasks = {}

        # Create a new window
        task_window = tk.Toplevel(self)
        task_window.title("Smart Task Adder")

        ttk.Label(task_window, text="Task Name:").grid(row=0, column=0)
        task_entry = ttk.Entry(task_window)
        task_entry.grid(row=0, column=1)

        ttk.Label(task_window, text="Importance (0-1):").grid(row=1, column=0)
        importance_entry = ttk.Entry(task_window)
        importance_entry.grid(row=1, column=1)

        ttk.Label(task_window, text="Days till deadline (0-7):").grid(row=2, column=0)
        days_till_deadline_entry = ttk.Entry(task_window)
        days_till_deadline_entry.grid(row=2, column=1)

        ttk.Label(task_window, text="Hours required (0-24):").grid(row=3, column=0)
        hours_required_entry = ttk.Entry(task_window)
        hours_required_entry.grid(row=3, column=1)

        submit_btn = ttk.Button(task_window, text="Add Task", command=on_submit)
        submit_btn.grid(row=4, column=0, columnspan=2)

        # Update the tasks list textbox
        def update_tasks_list():
            sorted_tasks = sorted(tasks, key=tasks.get, reverse=True)
            for task in sorted_tasks:
                self.tasks_list.insert(tk.END, task + "\n")

        done_btn = ttk.Button(task_window, text="Done", command=lambda: [update_tasks_list(), task_window.destroy])
        done_btn.grid(row=5, column=0, columnspan=2)
    def __init__(self):
        super().__init__()

        self.title("Simple Calendar")
        self.geometry("600x400")

        self.month_var = tk.StringVar()
        self.month_dropdown = ttk.Combobox(self, textvariable=self.month_var, values=list(calendar.month_name)[1:])
        self.month_dropdown.current(0)
        self.month_dropdown.bind("<<ComboboxSelected>>", self.draw_calendar)
        self.month_dropdown.pack(pady=20)

        self.left_frame = ttk.Frame(self)
        self.left_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=1)

        self.calendar_frame = ttk.Frame(self.left_frame)
        self.calendar_frame.pack(fill=tk.BOTH, expand=1)

        self.right_frame = ttk.Frame(self)
        self.right_frame.pack(side=tk.RIGHT, padx=10, fill=tk.BOTH)

        self.goals_label = ttk.Label(self.right_frame, text="Goals List:")
        self.goals_label.pack(anchor="w")
        self.goals_list = tk.Text(self.right_frame, height=10, width=30)
        self.goals_list.pack(fill=tk.BOTH, pady=5)

        self.tasks_label = ttk.Label(self.right_frame, text="Tasks List:")
        self.tasks_label.pack(anchor="w")
        self.tasks_list = tk.Text(self.right_frame, height=10, width=30)
        self.tasks_list.pack(fill=tk.BOTH, pady=5)

        self.general_label = ttk.Label(self.right_frame, text="General Notes:")
        self.general_label.pack(anchor="w")
        self.general_list = tk.Text(self.right_frame, height=10, width=30)
        self.general_list.pack(fill=tk.BOTH,pady=5)

        self.notes = {}
        self.smart_add_btn = ttk.Button(self, text="Smart Add", command=self.tasks_prioritizer_gui)
        self.smart_add_btn.pack(pady=10)
        self.load_data()
        self.draw_calendar()

    def draw_calendar(self, event=None):
        month_index = self.month_dropdown.current() + 1
        cal = calendar.monthcalendar(2023, month_index)

        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for col, day in enumerate(days):
            label = ttk.Label(self.calendar_frame, text=day)
            label.grid(row=0, column=col)

        for row, week in enumerate(cal):
            for col, day in enumerate(week):
                if day == 0:
                    continue

                btn_text = str(day)
                note_preview = self.notes.get((month_index, day), "")
                if note_preview:
                    note_preview = "\n" + note_preview[:10] + ("..." if len(note_preview) > 10 else "")

                btn_text += note_preview

                btn = ttk.Button(self.calendar_frame, text=btn_text, command=lambda day=day: self.add_or_view_notes(month_index, day))
                btn.grid(row=row+1, column=col, sticky="nsew")
                self.calendar_frame.columnconfigure(col, weight=1)
            self.calendar_frame.rowconfigure(row+1, weight=1)

    def add_or_view_notes(self, month, day):
        key = (month, day)
        note = simpledialog.askstring("Notes", f"Notes for {calendar.month_name[month]} {day}, 2023:", initialvalue=self.notes.get(key, ""))
        if note is not None:  # to handle when the user hits 'Cancel' on the dialog
            self.notes[key] = note
        self.draw_calendar()

    def load_data(self):
        # Default initialization
        self.notes = {}
        self.goals = ""
        self.tasks = ""
        self.general = ""

        if os.path.exists("data.json"):
            try:
                with open("data.json", "r") as f:
                    data = json.load(f)

                # Convert string keys back to tuples
                self.notes = {eval(key): value for key, value in data['notes'].items()}
                self.goals = data['goals']
                self.tasks = data['tasks']
                self.general = data['general']

                # Populate the textboxes with the saved content
                self.goals_list.delete("1.0", tk.END)
                self.goals_list.insert(tk.END, self.goals)

                self.tasks_list.delete("1.0", tk.END)
                self.tasks_list.insert(tk.END, self.tasks)

                self.general_list.delete("1.0", tk.END)
                self.general_list.insert(tk.END, self.general)

            except Exception as e:
                print(f"Error loading data: {e}")
                messagebox.showerror("Error", f"Error loading data: {e}")

    def on_closing(self):
        self.save_data()
        self.destroy()

    def save_data(self):
        data = {
            'notes': {str(key): value for key, value in self.notes.items()},
            'goals': self.goals_list.get("1.0", tk.END).strip(),
            'tasks': self.tasks_list.get("1.0", tk.END).strip(),
            'general': self.general_list.get("1.0", tk.END).strip()
        }

        with open("data.json", "w") as f:
            json.dump(data, f)

if __name__ == "__main__":
    app = SimpleCalendar()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
