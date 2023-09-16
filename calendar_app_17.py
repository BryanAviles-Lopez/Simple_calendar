import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import calendar
import json
import os

DATA_FILE = "calendar_data.json"

class SimpleCalendar(tk.Tk):
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
