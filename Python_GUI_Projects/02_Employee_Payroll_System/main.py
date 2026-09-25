"""Employee Payroll System using Tkinter and CSV."""
import csv
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

STUDENT = ("TIRTH KUMAR JANTILAL KAVAR", "Enrollment ID: 92500116005", "GR No.: 135965", "Class: 3EG1")
FIELDS = [("employee_id", "Employee ID"), ("name", "Employee Name"), ("department", "Department"),
          ("basic", "Basic Salary"), ("days", "Working Days"), ("hours", "Overtime Hours"),
          ("rate", "Overtime Rate"), ("bonus", "Bonus"), ("allowances", "Allowances"),
          ("tax_percent", "Tax Percentage"), ("other_deductions", "Other Deductions")]
COLS = ("employee_id", "name", "department", "basic", "overtime", "gross", "tax", "deductions", "net")
DATA_FILE = Path(__file__).with_name("payroll_data.csv")


def calculate_payroll(values):
    numeric = {}
    for key in ("basic", "days", "hours", "rate", "bonus", "allowances", "tax_percent", "other_deductions"):
        try: numeric[key] = float(values[key] or 0)
        except ValueError: raise ValueError(f"{dict(FIELDS)[key]} must be a number.")
        if numeric[key] < 0: raise ValueError(f"{dict(FIELDS)[key]} cannot be negative.")
    if numeric["tax_percent"] > 100: raise ValueError("Tax Percentage cannot exceed 100.")
    if numeric["days"] > 31: raise ValueError("Working Days cannot exceed 31.")
    overtime = numeric["hours"] * numeric["rate"]
    gross = numeric["basic"] + overtime + numeric["bonus"] + numeric["allowances"]
    tax = gross * numeric["tax_percent"] / 100
    deductions = tax + numeric["other_deductions"]
    return {**values, **numeric, "overtime": overtime, "gross": gross, "tax": tax,
            "deductions": deductions, "net": gross - deductions}


class PayrollApp:
    def __init__(self, root):
        self.root, self.records = root, []
        root.title("Employee Payroll System Using Python"); root.geometry("1200x750"); root.minsize(1000, 680); root.configure(bg="#eef2f7")
        self.vars = {key: tk.StringVar() for key, _ in FIELDS}; self.status = tk.StringVar(value="Ready")
        self.build_header(); self.build_ui(); self.load_data()

    def build_header(self):
        h = tk.Frame(self.root, bg="#172554", padx=25, pady=14); h.pack(fill="x")
        tk.Label(h, text="EMPLOYEE PAYROLL SYSTEM", bg="#172554", fg="white", font=("Arial", 22, "bold")).pack(side="left")
        info = tk.Frame(h, bg="#172554"); info.pack(side="right")
        for i, line in enumerate(STUDENT): tk.Label(info, text=line, bg="#172554", fg="white" if i == 0 else "#bfdbfe", anchor="e", font=("Arial", 9, "bold" if i == 0 else "normal")).pack(anchor="e")

    def build_ui(self):
        body = tk.Frame(self.root, bg="#eef2f7", padx=16, pady=14); body.pack(fill="both", expand=True)
        form = tk.LabelFrame(body, text=" Employee Details ", bg="white", fg="#172033", font=("Arial", 12, "bold"), padx=12, pady=9); form.pack(fill="x")
        for i, (key, label) in enumerate(FIELDS):
            r, c = divmod(i, 4); tk.Label(form, text=label, bg="white", fg="#475569").grid(row=r*2, column=c, sticky="w", padx=7)
            ttk.Entry(form, textvariable=self.vars[key]).grid(row=r*2+1, column=c, sticky="ew", padx=7, pady=(2, 7))
        for c in range(4): form.columnconfigure(c, weight=1)
        actions = tk.Frame(body, bg="#eef2f7"); actions.pack(fill="x", pady=9)
        for text, command in [("Calculate Salary", self.preview), ("Add Employee", self.add), ("Update Employee", self.update), ("Delete Employee", self.delete), ("Clear Fields", self.clear), ("Export CSV", self.export)]:
            ttk.Button(actions, text=text, command=command).pack(side="left", padx=(0, 7))
        cards = tk.Frame(body, bg="#eef2f7"); cards.pack(fill="x", pady=(0, 9)); self.summary = {}
        for key, title in [("count", "TOTAL EMPLOYEES"), ("gross", "TOTAL GROSS PAYROLL"), ("tax", "TOTAL TAX"), ("net", "TOTAL NET PAYROLL")]:
            card = tk.Frame(cards, bg="white", padx=15, pady=8); card.pack(side="left", fill="x", expand=True, padx=4)
            tk.Label(card, text=title, bg="white", fg="#64748b", font=("Arial", 9, "bold")).pack(anchor="w"); self.summary[key] = tk.Label(card, text="0", bg="white", fg="#2563eb", font=("Arial", 16, "bold")); self.summary[key].pack(anchor="w")
        table_frame = tk.Frame(body); table_frame.pack(fill="both", expand=True)
        self.table = ttk.Treeview(table_frame, columns=COLS, show="headings")
        headings = ["Employee ID", "Name", "Department", "Basic Salary", "Overtime", "Gross Salary", "Tax", "Deductions", "Net Salary"]
        for col, title in zip(COLS, headings): self.table.heading(col, text=title); self.table.column(col, width=110, anchor="center")
        scroll = ttk.Scrollbar(table_frame, command=self.table.yview); self.table.configure(yscrollcommand=scroll.set); self.table.pack(side="left", fill="both", expand=True); scroll.pack(side="right", fill="y")
        self.table.bind("<<TreeviewSelect>>", self.select)
        tk.Label(self.root, textvariable=self.status, bg="#dbeafe", fg="#172554", anchor="w", padx=14, pady=5).pack(fill="x")

    def form_values(self): return {key: var.get().strip() for key, var in self.vars.items()}
    def validated(self):
        values = self.form_values()
        if not values["employee_id"] or not values["name"] or not values["department"]: raise ValueError("Employee ID, Name and Department are required.")
        return calculate_payroll(values)
    def preview(self):
        try:
            r = self.validated(); messagebox.showinfo("Salary Calculation", f"Gross Salary: ₹{r['gross']:,.2f}\nTax: ₹{r['tax']:,.2f}\nTotal Deductions: ₹{r['deductions']:,.2f}\nNet Salary: ₹{r['net']:,.2f}")
        except ValueError as e: messagebox.showerror("Invalid Input", str(e))
    def add(self):
        try:
            r = self.validated()
            if any(x["employee_id"].lower() == r["employee_id"].lower() for x in self.records): raise ValueError("Employee ID already exists.")
            self.records.append(r); self.commit("Employee added")
        except ValueError as e: messagebox.showerror("Invalid Input", str(e))
    def update(self):
        selected = self.table.selection()
        if not selected: return messagebox.showwarning("Select Employee", "Select an employee to update.")
        try:
            r = self.validated(); old_id = self.table.item(selected[0], "values")[0]
            if any(x["employee_id"].lower() == r["employee_id"].lower() and x["employee_id"] != old_id for x in self.records): raise ValueError("Employee ID already exists.")
            index = next(i for i, x in enumerate(self.records) if x["employee_id"] == old_id); self.records[index] = r; self.commit("Employee updated")
        except ValueError as e: messagebox.showerror("Invalid Input", str(e))
    def delete(self):
        selected = self.table.selection()
        if not selected: return messagebox.showwarning("Select Employee", "Select an employee to delete.")
        employee_id = self.table.item(selected[0], "values")[0]
        if messagebox.askyesno("Confirm Delete", f"Delete employee {employee_id}?"):
            self.records = [r for r in self.records if r["employee_id"] != employee_id]; self.commit("Employee deleted")
    def select(self, _event):
        if not self.table.selection(): return
        employee_id = self.table.item(self.table.selection()[0], "values")[0]; record = next(r for r in self.records if r["employee_id"] == employee_id)
        for key, var in self.vars.items(): var.set(f"{record[key]:g}" if isinstance(record[key], float) else record[key])
    def clear(self):
        for var in self.vars.values(): var.set("")
        self.table.selection_remove(*self.table.selection()); self.status.set("Fields cleared")
    def commit(self, message): self.save_data(); self.refresh(); self.clear(); self.status.set(message)
    def refresh(self):
        self.table.delete(*self.table.get_children())
        for r in self.records: self.table.insert("", "end", values=(r["employee_id"], r["name"], r["department"], *[f"{r[k]:.2f}" for k in ("basic", "overtime", "gross", "tax", "deductions", "net")]))
        self.summary["count"].config(text=str(len(self.records)))
        for key in ("gross", "tax", "net"): self.summary[key].config(text=f"₹{sum(r[key] for r in self.records):,.2f}")
    def save_data(self):
        with DATA_FILE.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[k for k, _ in FIELDS] + ["overtime", "gross", "tax", "deductions", "net"]); writer.writeheader(); writer.writerows(self.records)
    def load_data(self):
        if DATA_FILE.exists():
            try:
                with DATA_FILE.open(encoding="utf-8") as f:
                    for row in csv.DictReader(f): self.records.append(calculate_payroll(row))
            except (OSError, ValueError): messagebox.showwarning("Data File", "Saved payroll data could not be loaded.")
        self.refresh()
    def export(self):
        if not self.records: return messagebox.showwarning("No Data", "Add an employee before exporting.")
        path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile="payroll_report.csv", filetypes=[("CSV files", "*.csv")])
        if path:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=[k for k, _ in FIELDS] + ["overtime", "gross", "tax", "deductions", "net"]); writer.writeheader(); writer.writerows(self.records)
            self.status.set(f"Exported {len(self.records)} records")


if __name__ == "__main__":
    window = tk.Tk(); PayrollApp(window); window.mainloop()
