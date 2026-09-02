import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np


# Grade points
GRADE_POINTS = {
    "O": 10,
    "A+": 9,
    "A": 8,
    "B+": 7,
    "B": 6,
    "C": 5,
    "F": 0
}


class StudentResultApp:
    def __init__(self, root):
        self.root = root
        self.root.title("B.Tech Student Results Management System")
        self.root.geometry("950x700")
        self.root.minsize(850, 600)

        # Main frame with 4-side margins
        main_frame = tk.Frame(root, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        # Heading
        title = tk.Label(
            main_frame,
            text="B.Tech Student Results Management System",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=(0, 15))

        # Student details
        details_frame = tk.LabelFrame(
            main_frame,
            text="Student Details",
            font=("Arial", 12, "bold"),
            padx=15,
            pady=15
        )
        details_frame.pack(fill="x", pady=5)

        tk.Label(details_frame, text="Student Name:").grid(
            row=0, column=0, padx=10, pady=8, sticky="w"
        )

        self.name_entry = tk.Entry(details_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=10, pady=8)

        tk.Label(details_frame, text="Roll Number:").grid(
            row=0, column=2, padx=10, pady=8, sticky="w"
        )

        self.roll_entry = tk.Entry(details_frame, width=25)
        self.roll_entry.grid(row=0, column=3, padx=10, pady=8)

        # Semester
        tk.Label(details_frame, text="Semester:").grid(
            row=1, column=0, padx=10, pady=8, sticky="w"
        )

        self.semester_combo = ttk.Combobox(
            details_frame,
            values=[
                "I-I", "I-II",
                "II-I", "II-II",
                "III-I", "III-II",
                "IV-I", "IV-II"
            ],
            state="readonly",
            width=27
        )
        self.semester_combo.grid(row=1, column=1, padx=10, pady=8)
        self.semester_combo.current(0)

        # Number of subjects
        tk.Label(details_frame, text="Number of Subjects:").grid(
            row=1, column=2, padx=10, pady=8, sticky="w"
        )

        self.subject_count = tk.Spinbox(
            details_frame,
            from_=1,
            to=15,
            width=23,
            command=self.create_subjects
        )
        self.subject_count.grid(row=1, column=3, padx=10, pady=8)

        # Subject section
        subject_frame = tk.LabelFrame(
            main_frame,
            text="Subject Details",
            font=("Arial", 12, "bold")
        )
        subject_frame.pack(fill="both", expand=True, pady=10)

        # Canvas + scrollbar
        self.canvas = tk.Canvas(subject_frame)

        scrollbar = ttk.Scrollbar(
            subject_frame,
            orient="vertical",
            command=self.canvas.yview
        )

        self.subject_inner = tk.Frame(self.canvas)

        self.subject_inner.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.subject_inner,
            anchor="nw"
        )

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mouse wheel scrolling
        self.canvas.bind_all(
            "<MouseWheel>",
            lambda event: self.canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )
        )

        # Table headings
        headings = [
            "S.No",
            "Subject Name",
            "Credits",
            "Grade"
        ]

        for col, heading in enumerate(headings):
            tk.Label(
                self.subject_inner,
                text=heading,
                font=("Arial", 11, "bold"),
                width=18
            ).grid(
                row=0,
                column=col,
                padx=5,
                pady=8
            )

        self.subject_entries = []

        self.create_subjects()

        # Buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Calculate CGPA",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=8,
            command=self.calculate_cgpa
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            button_frame,
            text="Clear",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=8,
            command=self.clear_all
        ).grid(row=0, column=1, padx=10)

        # Result
        self.result_label = tk.Label(
            main_frame,
            text="CGPA: --",
            font=("Arial", 16, "bold")
        )
        self.result_label.pack(pady=5)

    def create_subjects(self):
        """Create subject input rows."""

        # Remove old rows
        for widget in self.subject_inner.winfo_children():
            if widget.grid_info()["row"] != "0":
                widget.destroy()

        self.subject_entries = []

        try:
            count = int(self.subject_count.get())
        except ValueError:
            count = 1

        for i in range(count):

            # Serial number
            tk.Label(
                self.subject_inner,
                text=str(i + 1),
                width=18
            ).grid(
                row=i + 1,
                column=0,
                padx=5,
                pady=5
            )

            # Subject name
            subject_entry = tk.Entry(
                self.subject_inner,
                width=22
            )
            subject_entry.grid(
                row=i + 1,
                column=1,
                padx=5,
                pady=5
            )

            # Credits
            credit_entry = tk.Entry(
                self.subject_inner,
                width=15
            )
            credit_entry.grid(
                row=i + 1,
                column=2,
                padx=5,
                pady=5
            )

            # Grade
            grade_combo = ttk.Combobox(
                self.subject_inner,
                values=list(GRADE_POINTS.keys()),
                state="readonly",
                width=15
            )
            grade_combo.grid(
                row=i + 1,
                column=3,
                padx=5,
                pady=5
            )
            grade_combo.current(0)

            self.subject_entries.append(
                (subject_entry, credit_entry, grade_combo)
            )

        self.canvas.update_idletasks()
        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    def calculate_cgpa(self):
        """Calculate CGPA using NumPy."""

        name = self.name_entry.get().strip()
        roll = self.roll_entry.get().strip()

        if not name or not roll:
            messagebox.showerror(
                "Error",
                "Please enter Student Name and Roll Number."
            )
            return

        credits = []
        grade_points = []

        try:
            for subject_entry, credit_entry, grade_combo in self.subject_entries:

                subject = subject_entry.get().strip()
                credit_text = credit_entry.get().strip()
                grade = grade_combo.get()

                if not subject:
                    messagebox.showerror(
                        "Error",
                        "Please enter all subject names."
                    )
                    return

                if not credit_text:
                    messagebox.showerror(
                        "Error",
                        "Please enter credits for all subjects."
                    )
                    return

                credit = float(credit_text)

                if credit <= 0:
                    raise ValueError

                credits.append(credit)
                grade_points.append(GRADE_POINTS[grade])

        except ValueError:
            messagebox.showerror(
                "Error",
                "Credits must be positive numbers."
            )
            return

        # Convert lists into NumPy arrays
        credits_array = np.array(credits)
        grade_array = np.array(grade_points)

        # B.Tech CGPA formula:
        # CGPA = Sum(Credits × Grade Point) / Sum(Credits)

        weighted_points = credits_array * grade_array

        total_credits = np.sum(credits_array)
        total_weighted_points = np.sum(weighted_points)

        if total_credits == 0:
            messagebox.showerror(
                "Error",
                "Total credits cannot be zero."
            )
            return

        cgpa = total_weighted_points / total_credits

        self.result_label.config(
            text=f"CGPA: {cgpa:.2f}"
        )

        messagebox.showinfo(
            "Result",
            f"Student Name: {name}\n"
            f"Roll Number: {roll}\n"
            f"Semester: {self.semester_combo.get()}\n\n"
            f"Total Credits: {total_credits:g}\n"
            f"CGPA: {cgpa:.2f}"
        )

    def clear_all(self):

        self.name_entry.delete(0, tk.END)
        self.roll_entry.delete(0, tk.END)

        self.semester_combo.current(0)
        self.subject_count.delete(0, tk.END)
        self.subject_count.insert(0, "1")

        self.create_subjects()

        self.result_label.config(
            text="CGPA: --"
        )


# Main program
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentResultApp(root)
    root.mainloop()
