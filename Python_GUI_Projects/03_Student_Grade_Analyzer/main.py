"""Student Grade Analyzer using Tkinter and CSV."""
import csv
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

STUDENT = ("TIRTH KUMAR JANTILAL KAVAR", "Enrollment ID: 92500116005", "GR No.: 135965", "Class: 3EG1")
DATA_FILE = Path(__file__).with_name("student_results.csv")
SUBJECTS = [f"subject{i}" for i in range(1, 6)]


def calculate_result(values):
    marks = []
    for index, key in enumerate(SUBJECTS, 1):
        try: mark = float(values[key])
        except ValueError: raise ValueError(f"Subject {index} Marks must be a number.")
        if not 0 <= mark <= 100: raise ValueError(f"Subject {index} Marks must be between 0 and 100.")
        marks.append(mark)
    total, percentage = sum(marks), sum(marks) / 5
    grade = "A+" if percentage >= 90 else "A" if percentage >= 80 else "B+" if percentage >= 70 else "B" if percentage >= 60 else "C" if percentage >= 50 else "D" if percentage >= 40 else "F"
    result = "Pass" if all(mark >= 40 for mark in marks) else "Fail"
    return {**values, **dict(zip(SUBJECTS, marks)), "total": total, "percentage": percentage,
            "grade": grade, "result": result, "strongest": marks.index(max(marks)) + 1, "weakest": marks.index(min(marks)) + 1}


class GradeApp:
    def __init__(self, root):
        self.root, self.records = root, []
        root.title("Student Grade Analyzer Using Python"); root.geometry("1200x750"); root.minsize(1020, 690); root.configure(bg="#eef2f7")
        self.vars = {key: tk.StringVar() for key in ["student_id", "name", *SUBJECTS]}; self.status = tk.StringVar(value="Ready")
        self.header(); self.ui(); self.load()
    def header(self):
        h = tk.Frame(self.root, bg="#172554", padx=25, pady=14); h.pack(fill="x")
        tk.Label(h, text="STUDENT GRADE ANALYZER", bg="#172554", fg="white", font=("Arial", 22, "bold")).pack(side="left")
        f = tk.Frame(h, bg="#172554"); f.pack(side="right")
        for i, line in enumerate(STUDENT): tk.Label(f, text=line, bg="#172554", fg="white" if i == 0 else "#bfdbfe", anchor="e", font=("Arial", 9, "bold" if i == 0 else "normal")).pack(anchor="e")
    def ui(self):
        body = tk.Frame(self.root, bg="#eef2f7", padx=16, pady=12); body.pack(fill="both", expand=True)
        form = tk.LabelFrame(body, text=" Student Details & Marks ", bg="white", padx=12, pady=9, font=("Arial", 12, "bold")); form.pack(fill="x")
        fields = [("student_id", "Student ID"), ("name", "Student Name")] + [(key, f"Subject {i} Marks") for i, key in enumerate(SUBJECTS, 1)]
        for i, (key, label) in enumerate(fields):
            tk.Label(form, text=label, bg="white", fg="#475569").grid(row=(i//4)*2, column=i%4, sticky="w", padx=7)
            ttk.Entry(form, textvariable=self.vars[key]).grid(row=(i//4)*2+1, column=i%4, sticky="ew", padx=7, pady=(2, 7))
        for c in range(4): form.columnconfigure(c, weight=1)
        buttons = tk.Frame(body, bg="#eef2f7"); buttons.pack(fill="x", pady=8)
        for text, cmd in [("Calculate Result", self.preview), ("Add Student", self.add), ("Update Student", self.update), ("Delete Student", self.delete), ("Clear", self.clear), ("Export Report", self.export)]: ttk.Button(buttons, text=text, command=cmd).pack(side="left", padx=(0, 7))
        cards = tk.Frame(body, bg="#eef2f7"); cards.pack(fill="x", pady=(0, 8)); self.cards = {}
        for key, title in [("total", "TOTAL STUDENTS"), ("passed", "PASSED"), ("failed", "FAILED"), ("average", "CLASS AVERAGE"), ("highest", "HIGHEST"), ("lowest", "LOWEST")]:
            c = tk.Frame(cards, bg="white", padx=10, pady=7); c.pack(side="left", fill="x", expand=True, padx=3); tk.Label(c, text=title, bg="white", fg="#64748b", font=("Arial", 8, "bold")).pack(); self.cards[key] = tk.Label(c, text="0", bg="white", fg="#2563eb", font=("Arial", 14, "bold")); self.cards[key].pack()
        lower = tk.PanedWindow(body, orient="horizontal", bg="#eef2f7", sashwidth=5); lower.pack(fill="both", expand=True)
        table_frame = tk.Frame(lower); report = tk.LabelFrame(lower, text=" Individual Performance Report ", bg="white", padx=14, pady=10, font=("Arial", 11, "bold")); lower.add(table_frame, stretch="always"); lower.add(report, width=280)
        cols = ("student_id", "name", *SUBJECTS, "total", "percentage", "grade", "result"); self.table = ttk.Treeview(table_frame, columns=cols, show="headings")
        labels = ("ID", "Name", "Sub 1", "Sub 2", "Sub 3", "Sub 4", "Sub 5", "Total", "%", "Grade", "Result")
        for col, label in zip(cols, labels): self.table.heading(col, text=label); self.table.column(col, width=70 if col != "name" else 130, anchor="center")
        sy = ttk.Scrollbar(table_frame, command=self.table.yview); self.table.configure(yscrollcommand=sy.set); self.table.pack(side="left", fill="both", expand=True); sy.pack(side="right", fill="y"); self.table.bind("<<TreeviewSelect>>", self.select)
        self.report_text = tk.Label(report, text="Select a student to view the report.", bg="white", fg="#334155", justify="left", anchor="nw", font=("Arial", 11)); self.report_text.pack(fill="both", expand=True)
        tk.Label(self.root, textvariable=self.status, bg="#dbeafe", fg="#172554", anchor="w", padx=14, pady=5).pack(fill="x")
    def values(self): return {k: v.get().strip() for k, v in self.vars.items()}
    def validated(self):
        values = self.values()
        if not values["student_id"] or not values["name"]: raise ValueError("Student ID and Student Name are required.")
        return calculate_result(values)
    def preview(self):
        try:
            r = self.validated(); messagebox.showinfo("Calculated Result", f"Total: {r['total']:.0f}/500\nPercentage: {r['percentage']:.2f}%\nGrade: {r['grade']}\nResult: {r['result']}")
        except ValueError as e: messagebox.showerror("Invalid Input", str(e))
    def add(self):
        try:
            r = self.validated()
            if any(x["student_id"].lower() == r["student_id"].lower() for x in self.records): raise ValueError("Student ID already exists.")
            self.records.append(r); self.commit("Student added")
        except ValueError as e: messagebox.showerror("Invalid Input", str(e))
    def update(self):
        if not self.table.selection(): return messagebox.showwarning("Select Student", "Select a student to update.")
        try:
            r = self.validated(); old = self.table.item(self.table.selection()[0], "values")[0]
            if any(x["student_id"].lower() == r["student_id"].lower() and x["student_id"] != old for x in self.records): raise ValueError("Student ID already exists.")
            self.records[next(i for i, x in enumerate(self.records) if x["student_id"] == old)] = r; self.commit("Student updated")
        except ValueError as e: messagebox.showerror("Invalid Input", str(e))
    def delete(self):
        if not self.table.selection(): return messagebox.showwarning("Select Student", "Select a student to delete.")
        sid = self.table.item(self.table.selection()[0], "values")[0]
        if messagebox.askyesno("Confirm Delete", f"Delete student {sid}?"): self.records = [r for r in self.records if r["student_id"] != sid]; self.commit("Student deleted")
    def select(self, _event):
        if not self.table.selection(): return
        sid = self.table.item(self.table.selection()[0], "values")[0]; r = next(x for x in self.records if x["student_id"] == sid)
        for key, var in self.vars.items(): var.set(f"{r[key]:g}" if isinstance(r[key], float) else r[key])
        self.report_text.config(text=f"Name: {r['name']}\n\nTotal Marks: {r['total']:.0f} / 500\nPercentage: {r['percentage']:.2f}%\nGrade: {r['grade']}\nResult: {r['result']}\n\nStrongest Subject: Subject {r['strongest']}\nWeakest Subject: Subject {r['weakest']}")
    def clear(self):
        for v in self.vars.values(): v.set("")
        self.table.selection_remove(*self.table.selection()); self.report_text.config(text="Select a student to view the report."); self.status.set("Fields cleared")
    def refresh(self):
        self.table.delete(*self.table.get_children())
        for r in self.records: self.table.insert("", "end", values=(r["student_id"], r["name"], *[f"{r[s]:g}" for s in SUBJECTS], f"{r['total']:g}", f"{r['percentage']:.2f}", r["grade"], r["result"]))
        percentages = [r["percentage"] for r in self.records]; passed = sum(r["result"] == "Pass" for r in self.records)
        values = {"total": len(self.records), "passed": passed, "failed": len(self.records)-passed, "average": f"{sum(percentages)/len(percentages):.2f}%" if percentages else "0%", "highest": f"{max(percentages):.2f}%" if percentages else "0%", "lowest": f"{min(percentages):.2f}%" if percentages else "0%"}
        for key, value in values.items(): self.cards[key].config(text=value)
    def save(self):
        fields = ["student_id", "name", *SUBJECTS, "total", "percentage", "grade", "result", "strongest", "weakest"]
        with DATA_FILE.open("w", newline="", encoding="utf-8") as f: w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(self.records)
    def commit(self, message): self.save(); self.refresh(); self.clear(); self.status.set(message)
    def load(self):
        if DATA_FILE.exists():
            try:
                with DATA_FILE.open(encoding="utf-8") as f:
                    for row in csv.DictReader(f): self.records.append(calculate_result(row))
            except (OSError, ValueError): messagebox.showwarning("Data File", "Saved student data could not be loaded.")
        self.refresh()
    def export(self):
        if not self.records: return messagebox.showwarning("No Data", "Add a student before exporting.")
        path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile="student_report.csv", filetypes=[("CSV files", "*.csv")])
        if path:
            fields = ["student_id", "name", *SUBJECTS, "total", "percentage", "grade", "result", "strongest", "weakest"]
            with open(path, "w", newline="", encoding="utf-8") as f: w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(self.records)
            self.status.set(f"Exported {len(self.records)} student records")


if __name__ == "__main__":
    window = tk.Tk(); GradeApp(window); window.mainloop()
