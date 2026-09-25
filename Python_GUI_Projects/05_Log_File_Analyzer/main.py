"""GUI log-file analyzer using standard Python libraries."""
import csv
import logging
import os
import re
import tkinter as tk
from collections import Counter
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

BASE = Path(__file__).parent
logging.basicConfig(filename=BASE / "app_activity.log", level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")
STUDENT = ("TIRTH KUMAR JANTILAL KAVAR", "Enrollment ID: 92500116005", "GR No.: 135965", "Class: 3EG1")
LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
PATTERN = re.compile(r"^(\d{4}-\d{2}-\d{2})[ T](\d{2}:\d{2}:\d{2})(?:,\d+)?\s+(DEBUG|INFO|WARNING|ERROR|CRITICAL)\s+(.*)$", re.I)
COLORS = {
    "page": "#f1f5f9", "card": "#ffffff", "navy": "#172554",
    "blue": "#2563eb", "blue_hover": "#1d4ed8", "text": "#0f172a",
    "muted": "#475569", "border": "#cbd5e1",
}


def parse_log_lines(lines):
    entries, invalid = [], 0
    for line in lines:
        match = PATTERN.match(line.strip())
        if match:
            date, time, level, message = match.groups(); entries.append({"date": date, "time": time, "level": level.upper(), "message": message})
        elif line.strip(): invalid += 1
    return entries, invalid


class LogAnalyzerApp:
    def __init__(self, root):
        self.root, self.entries = root, []
        root.title("Log File Analyzer Using Python, Logging & CSV"); root.geometry("1200x750"); root.minsize(1000, 680); root.configure(bg=COLORS["page"])
        self.file_var = tk.StringVar(); self.level_var = tk.StringVar(value="All"); self.search_var = tk.StringVar(); self.status = tk.StringVar(value="Choose a .log or .txt file to begin")
        self.configure_styles(); self.header(); self.ui()
        sample = BASE / "sample_server.log"
        if sample.exists():
            self.file_var.set(str(sample))
            self.root.after(100, self.analyze)

    def configure_styles(self):
        """Force a readable light palette even when macOS uses dark mode."""
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure(
            "TEntry", fieldbackground=COLORS["card"], foreground=COLORS["text"],
            insertcolor=COLORS["text"], bordercolor=COLORS["border"],
            lightcolor=COLORS["border"], darkcolor=COLORS["border"],
            padding=(8, 7), font=("Arial", 10),
        )
        style.map(
            "TEntry", bordercolor=[("focus", COLORS["blue"])],
            lightcolor=[("focus", COLORS["blue"])],
            darkcolor=[("focus", COLORS["blue"])],
        )
        style.configure(
            "TButton", background="#e2e8f0", foreground=COLORS["text"],
            bordercolor="#94a3b8", padding=(12, 7), font=("Arial", 10, "bold"),
        )
        style.map("TButton", background=[("active", "#cbd5e1"), ("pressed", "#94a3b8")])
        style.configure(
            "Primary.TButton", background=COLORS["blue"], foreground="#ffffff",
            bordercolor=COLORS["blue"], padding=(14, 7), font=("Arial", 10, "bold"),
        )
        style.map(
            "Primary.TButton", background=[("active", COLORS["blue_hover"]), ("pressed", "#1e40af")],
            foreground=[("active", "#ffffff"), ("pressed", "#ffffff")],
        )
        style.configure(
            "TCombobox", fieldbackground=COLORS["card"], background=COLORS["card"],
            foreground=COLORS["text"], arrowcolor=COLORS["navy"],
            bordercolor=COLORS["border"], padding=(7, 6), font=("Arial", 10),
        )
        style.map(
            "TCombobox", fieldbackground=[("readonly", COLORS["card"])],
            foreground=[("readonly", COLORS["text"])],
            selectbackground=[("readonly", COLORS["card"])],
            selectforeground=[("readonly", COLORS["text"])],
        )
        style.configure(
            "Treeview", background=COLORS["card"], fieldbackground=COLORS["card"],
            foreground=COLORS["text"], rowheight=30, borderwidth=0,
            font=("Arial", 10),
        )
        style.configure(
            "Treeview.Heading", background=COLORS["navy"], foreground="#ffffff",
            bordercolor="#334155", padding=(8, 8), font=("Arial", 10, "bold"),
        )
        style.map(
            "Treeview", background=[("selected", COLORS["blue"])],
            foreground=[("selected", "#ffffff")],
        )
        style.map("Treeview.Heading", background=[("active", "#1e3a8a")])
    def header(self):
        h = tk.Frame(self.root, bg=COLORS["navy"], padx=25, pady=14); h.pack(fill="x"); tk.Label(h, text="LOG FILE ANALYZER", bg=COLORS["navy"], fg="white", font=("Arial", 22, "bold")).pack(side="left")
        f = tk.Frame(h, bg=COLORS["navy"]); f.pack(side="right")
        for i, line in enumerate(STUDENT): tk.Label(f, text=line, bg=COLORS["navy"], fg="white" if i == 0 else "#bfdbfe", anchor="e", font=("Arial", 9, "bold" if i == 0 else "normal")).pack(anchor="e")
    def ui(self):
        body = tk.Frame(self.root, bg=COLORS["page"], padx=16, pady=12); body.pack(fill="both", expand=True)
        file_box = tk.LabelFrame(body, text=" Log File ", bg=COLORS["card"], fg=COLORS["text"], highlightbackground=COLORS["border"], padx=12, pady=9, font=("Arial", 11, "bold")); file_box.pack(fill="x")
        ttk.Entry(file_box, textvariable=self.file_var, state="readonly").pack(side="left", fill="x", expand=True, padx=(0, 8)); ttk.Button(file_box, text="Browse File", command=self.browse).pack(side="left", padx=4); ttk.Button(file_box, text="Analyze Logs", command=self.analyze, style="Primary.TButton").pack(side="left", padx=4); ttk.Button(file_box, text="Export CSV", command=self.export).pack(side="left", padx=4)
        cards = tk.Frame(body, bg=COLORS["page"]); cards.pack(fill="x", pady=9); self.cards = {}
        for key, title in [("TOTAL", "TOTAL LOGS"), *[(x, x) for x in LEVELS]]:
            c = tk.Frame(cards, bg=COLORS["card"], highlightbackground=COLORS["border"], highlightthickness=1, padx=9, pady=7); c.pack(side="left", fill="x", expand=True, padx=3); tk.Label(c, text=title, bg=COLORS["card"], fg="#64748b", font=("Arial", 8, "bold")).pack(); self.cards[key] = tk.Label(c, text="0", bg=COLORS["card"], fg=COLORS["blue"], font=("Arial", 14, "bold")); self.cards[key].pack()
        filters = tk.Frame(body, bg=COLORS["page"]); filters.pack(fill="x", pady=(0, 8)); tk.Label(filters, text="Level:", bg=COLORS["page"], fg=COLORS["muted"], font=("Arial", 10, "bold")).pack(side="left"); combo = ttk.Combobox(filters, textvariable=self.level_var, values=("All", *LEVELS), state="readonly", width=12); combo.pack(side="left", padx=6); combo.bind("<<ComboboxSelected>>", lambda _e: self.filter_rows()); tk.Label(filters, text="Search message:", bg=COLORS["page"], fg=COLORS["muted"], font=("Arial", 10, "bold")).pack(side="left", padx=(18, 5)); ttk.Entry(filters, textvariable=self.search_var, width=35).pack(side="left"); self.search_var.trace_add("write", lambda *_: self.filter_rows())
        panes = tk.PanedWindow(body, orient="vertical", bg=COLORS["page"], sashwidth=5, bd=0); panes.pack(fill="both", expand=True)
        all_frame = tk.LabelFrame(panes, text=" Log Entries ", bg=COLORS["card"], fg=COLORS["text"], highlightbackground=COLORS["border"], font=("Arial", 10, "bold")); error_frame = tk.LabelFrame(panes, text=" Errors & Critical Events ", bg=COLORS["card"], fg="#991b1b", highlightbackground=COLORS["border"], font=("Arial", 10, "bold")); panes.add(all_frame, stretch="always"); panes.add(error_frame, stretch="always")
        self.table = self.make_table(all_frame); self.error_table = self.make_table(error_frame)
        summary = tk.Frame(body, bg=COLORS["card"], highlightbackground=COLORS["border"], highlightthickness=1, padx=10, pady=7); summary.pack(fill="x", pady=(8, 0)); self.summary_label = tk.Label(summary, text="Summary will appear after analysis.", bg=COLORS["card"], fg="#334155", anchor="w", justify="left", font=("Arial", 9)); self.summary_label.pack(fill="x")
        tk.Label(self.root, textvariable=self.status, bg="#dbeafe", fg=COLORS["navy"], anchor="w", padx=14, pady=6, font=("Arial", 9)).pack(fill="x")
    def make_table(self, parent):
        cols = ("date", "time", "level", "message"); table = ttk.Treeview(parent, columns=cols, show="headings", height=7)
        for col, title, width in [("date", "Date", 115), ("time", "Time", 95), ("level", "Level", 100), ("message", "Message", 650)]: table.heading(col, text=title); table.column(col, width=width, anchor="center" if col in ("date", "time", "level") else "w")
        table.tag_configure("DEBUG", background="#f1f5f9", foreground="#475569")
        table.tag_configure("INFO", background="#eff6ff", foreground="#1e3a8a")
        table.tag_configure("WARNING", background="#fef3c7", foreground="#78350f")
        table.tag_configure("ERROR", background="#fee2e2", foreground="#991b1b")
        table.tag_configure("CRITICAL", background="#7f1d1d", foreground="#ffffff")
        scroll = ttk.Scrollbar(parent, command=table.yview); table.configure(yscrollcommand=scroll.set); table.pack(side="left", fill="both", expand=True); scroll.pack(side="right", fill="y"); return table
    def browse(self):
        path = filedialog.askopenfilename(filetypes=[("Log and text files", "*.log *.txt"), ("Log files", "*.log"), ("Text files", "*.txt")])
        if path: self.file_var.set(path); self.status.set(f"Selected: {os.path.basename(path)}"); logging.info("File loaded: %s", path)
    def analyze(self):
        path = self.file_var.get()
        if not path: logging.warning("Invalid file: no file selected"); return messagebox.showwarning("No File", "Choose a .log or .txt file first.")
        if Path(path).suffix.lower() not in (".log", ".txt"): logging.warning("Invalid file extension: %s", path); return messagebox.showerror("Invalid File", "Only .log and .txt files are supported.")
        try:
            logging.info("Analysis started: %s", path)
            with open(path, encoding="utf-8", errors="replace") as f: self.entries, invalid = parse_log_lines(f)
            self.update_dashboard(); self.filter_rows(); self.update_errors(); self.update_summary()
            if not self.entries: messagebox.showinfo("Analysis Complete", "No valid log entries were found in this file.")
            self.status.set(f"Analysis complete: {len(self.entries)} valid, {invalid} invalid line(s)"); logging.info("Analysis completed: %d valid, %d invalid", len(self.entries), invalid)
        except OSError as error: logging.exception("Processing error"); messagebox.showerror("File Error", f"Could not read the file:\n{error}")
    def update_dashboard(self):
        counts = Counter(x["level"] for x in self.entries); self.cards["TOTAL"].config(text=str(len(self.entries)))
        for level in LEVELS: self.cards[level].config(text=str(counts[level]))
    def put(self, table, rows):
        table.delete(*table.get_children())
        for x in rows: table.insert("", "end", values=(x["date"], x["time"], x["level"], x["message"]), tags=(x["level"],))
    def filter_rows(self):
        level, text = self.level_var.get(), self.search_var.get().lower().strip(); rows = [x for x in self.entries if (level == "All" or x["level"] == level) and text in x["message"].lower()]; self.put(self.table, rows); self.status.set(f"Showing {len(rows)} of {len(self.entries)} log entries")
    def update_errors(self): self.put(self.error_table, [x for x in self.entries if x["level"] in ("ERROR", "CRITICAL")])
    def update_summary(self):
        counts = Counter(x["level"] for x in self.entries); errors = [x["message"] for x in self.entries if x["level"] in ("ERROR", "CRITICAL")]; common = Counter(errors).most_common(1)[0][0] if errors else "None"; percentage = (len(errors) / len(self.entries) * 100) if self.entries else 0
        self.summary_label.config(text=f"Total: {len(self.entries)}    Errors: {counts['ERROR']}    Warnings: {counts['WARNING']}    Critical: {counts['CRITICAL']}    Error percentage: {percentage:.2f}%\nMost common error message: {common}")
    def export(self):
        if not self.entries: return messagebox.showwarning("No Results", "Analyze a log file before exporting.")
        path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile="log_analysis.csv", filetypes=[("CSV files", "*.csv")])
        if path:
            try:
                with open(path, "w", newline="", encoding="utf-8") as f: w = csv.DictWriter(f, fieldnames=("date", "time", "level", "message")); w.writeheader(); w.writerows(self.entries)
                self.status.set(f"Exported {len(self.entries)} log entries"); logging.info("Export completed: %s", path)
            except OSError as error: logging.exception("Export error"); messagebox.showerror("Export Error", str(error))


if __name__ == "__main__":
    window = tk.Tk(); LogAnalyzerApp(window); window.mainloop()
