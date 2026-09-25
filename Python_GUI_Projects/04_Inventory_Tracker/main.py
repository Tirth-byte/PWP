"""Inventory Tracker using lists, dictionaries, Tkinter and CSV."""
import csv
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

STUDENT = ("TIRTH KUMAR JANTILAL KAVAR", "Enrollment ID: 92500116005", "GR No.: 135965", "Class: 3EG1")
DATA_FILE = Path(__file__).with_name("inventory.csv")
FIELDS = [("item_id", "Item ID"), ("name", "Item Name"), ("category", "Category"), ("quantity", "Quantity"),
          ("unit_price", "Unit Price"), ("supplier", "Supplier"), ("reorder", "Reorder Level")]

# Explicit colours prevent macOS dark mode from producing dark fields or
# white table text on pale warning rows.
COLORS = {
    "page": "#f1f5f9", "card": "#ffffff", "navy": "#172554",
    "blue": "#2563eb", "blue_hover": "#1d4ed8", "text": "#0f172a",
    "muted": "#475569", "border": "#cbd5e1", "header": "#e2e8f0",
}


def prepare_item(values):
    try: quantity, price, reorder = int(values["quantity"]), float(values["unit_price"]), int(values["reorder"])
    except ValueError: raise ValueError("Quantity and Reorder Level must be whole numbers; Unit Price must be numeric.")
    if quantity < 0 or price < 0 or reorder < 0: raise ValueError("Quantity, Unit Price and Reorder Level cannot be negative.")
    status = "OUT OF STOCK" if quantity == 0 else "LOW STOCK" if quantity <= reorder else "IN STOCK"
    return {**values, "quantity": quantity, "unit_price": price, "reorder": reorder, "stock_value": quantity * price, "status": status}


class InventoryApp:
    def __init__(self, root):
        self.root, self.inventory = root, []  # Required runtime list of item dictionaries.
        root.title("Inventory Tracker Using Python"); root.geometry("1200x750"); root.minsize(1020, 680); root.configure(bg=COLORS["page"])
        self.vars = {k: tk.StringVar() for k, _ in FIELDS}; self.search_var = tk.StringVar(); self.status = tk.StringVar(value="Ready")
        self.configure_styles(); self.header(); self.ui(); self.load()

    def configure_styles(self):
        """Create a readable light theme independent of the OS appearance."""
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure(
            "TEntry", fieldbackground=COLORS["card"], foreground=COLORS["text"],
            bordercolor=COLORS["border"], lightcolor=COLORS["border"],
            darkcolor=COLORS["border"], insertcolor=COLORS["text"],
            padding=(8, 7), font=("Arial", 11),
        )
        style.map(
            "TEntry",
            bordercolor=[("focus", COLORS["blue"])],
            lightcolor=[("focus", COLORS["blue"])],
            darkcolor=[("focus", COLORS["blue"])],
        )
        style.configure(
            "TButton", background="#e2e8f0", foreground=COLORS["text"],
            bordercolor="#94a3b8", padding=(12, 7), font=("Arial", 10, "bold"),
        )
        style.map(
            "TButton", background=[("active", "#cbd5e1"), ("pressed", "#94a3b8")],
            foreground=[("disabled", "#94a3b8")],
        )
        style.configure(
            "Primary.TButton", background=COLORS["blue"], foreground="#ffffff",
            bordercolor=COLORS["blue"], padding=(14, 7), font=("Arial", 10, "bold"),
        )
        style.map(
            "Primary.TButton",
            background=[("active", COLORS["blue_hover"]), ("pressed", "#1e40af")],
            foreground=[("active", "#ffffff"), ("pressed", "#ffffff")],
        )
        style.configure(
            "Treeview", background=COLORS["card"], fieldbackground=COLORS["card"],
            foreground=COLORS["text"], rowheight=32, borderwidth=0,
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
        style.map(
            "Treeview.Heading", background=[("active", "#1e3a8a")],
            foreground=[("active", "#ffffff")],
        )
    def header(self):
        h = tk.Frame(self.root, bg=COLORS["navy"], padx=25, pady=14); h.pack(fill="x"); tk.Label(h, text="INVENTORY TRACKER", bg=COLORS["navy"], fg="white", font=("Arial", 22, "bold")).pack(side="left")
        f = tk.Frame(h, bg=COLORS["navy"]); f.pack(side="right")
        for i, line in enumerate(STUDENT): tk.Label(f, text=line, bg=COLORS["navy"], fg="white" if i == 0 else "#bfdbfe", anchor="e", font=("Arial", 9, "bold" if i == 0 else "normal")).pack(anchor="e")
    def ui(self):
        body = tk.Frame(self.root, bg=COLORS["page"], padx=16, pady=12); body.pack(fill="both", expand=True)
        form = tk.LabelFrame(body, text=" Item Details ", bg=COLORS["card"], fg=COLORS["text"], highlightbackground=COLORS["border"], padx=12, pady=9, font=("Arial", 12, "bold")); form.pack(fill="x")
        for i, (key, label) in enumerate(FIELDS):
            tk.Label(form, text=label, bg=COLORS["card"], fg=COLORS["muted"], font=("Arial", 10, "bold")).grid(row=(i//4)*2, column=i%4, sticky="w", padx=7); ttk.Entry(form, textvariable=self.vars[key]).grid(row=(i//4)*2+1, column=i%4, sticky="ew", padx=7, pady=(3, 8))
        for c in range(4): form.columnconfigure(c, weight=1)
        actions = tk.Frame(body, bg=COLORS["page"]); actions.pack(fill="x", pady=9)
        for index, (text, cmd) in enumerate([("Add Item", self.add), ("Update Item", self.update), ("Delete Item", self.delete), ("Clear", self.clear), ("Export CSV", self.export)]): ttk.Button(actions, text=text, command=cmd, style="Primary.TButton" if index == 0 else "TButton").pack(side="left", padx=(0, 7))
        search_group = tk.Frame(actions, bg=COLORS["page"]); search_group.pack(side="right")
        tk.Label(search_group, text="Search:", bg=COLORS["page"], fg=COLORS["muted"], font=("Arial", 10, "bold")).pack(side="left", padx=(0, 6))
        ttk.Entry(search_group, textvariable=self.search_var, width=25).pack(side="left", padx=(0, 5)); ttk.Button(search_group, text="Search Item", command=self.search).pack(side="left"); ttk.Button(search_group, text="Show All", command=self.show_all).pack(side="left", padx=(5, 0))
        self.search_var.trace_add("write", lambda *_: self.search())
        cards = tk.Frame(body, bg=COLORS["page"]); cards.pack(fill="x", pady=(0, 9)); self.cards = {}
        for key, title in [("items", "TOTAL ITEMS"), ("quantity", "TOTAL QUANTITY"), ("low", "LOW STOCK"), ("out", "OUT OF STOCK"), ("value", "INVENTORY VALUE")]:
            c = tk.Frame(cards, bg=COLORS["card"], highlightbackground=COLORS["border"], highlightthickness=1, padx=11, pady=8); c.pack(side="left", fill="x", expand=True, padx=3); tk.Label(c, text=title, bg=COLORS["card"], fg="#64748b", font=("Arial", 8, "bold")).pack(); self.cards[key] = tk.Label(c, text="0", bg=COLORS["card"], fg=COLORS["blue"], font=("Arial", 14, "bold")); self.cards[key].pack()
        frame = tk.Frame(body, bg=COLORS["card"], highlightbackground=COLORS["border"], highlightthickness=1); frame.pack(fill="both", expand=True); cols = ("item_id", "name", "category", "quantity", "unit_price", "supplier", "reorder", "stock_value", "status")
        self.table = ttk.Treeview(frame, columns=cols, show="headings"); labels = ("Item ID", "Item Name", "Category", "Quantity", "Unit Price", "Supplier", "Reorder Level", "Stock Value", "Status")
        widths = (85, 145, 115, 85, 100, 135, 105, 110, 120)
        for col, label, width in zip(cols, labels, widths): self.table.heading(col, text=label); self.table.column(col, width=width, minwidth=70, anchor="w" if col in ("name", "category", "supplier") else "center")
        self.table.tag_configure("even", background="#f8fafc", foreground=COLORS["text"])
        self.table.tag_configure("odd", background="#ffffff", foreground=COLORS["text"])
        self.table.tag_configure("low", background="#fef3c7", foreground="#78350f")
        self.table.tag_configure("out", background="#fee2e2", foreground="#991b1b")
        sy = ttk.Scrollbar(frame, command=self.table.yview); self.table.configure(yscrollcommand=sy.set); self.table.pack(side="left", fill="both", expand=True); sy.pack(side="right", fill="y"); self.table.bind("<<TreeviewSelect>>", self.select)
        tk.Label(self.root, textvariable=self.status, bg="#dbeafe", fg=COLORS["navy"], anchor="w", padx=14, pady=6, font=("Arial", 9)).pack(fill="x")
    def values(self): return {k: v.get().strip() for k, v in self.vars.items()}
    def validated(self):
        values = self.values()
        if any(not values[k] for k in ("item_id", "name", "category", "supplier")): raise ValueError("Item ID, Item Name, Category and Supplier are required.")
        return prepare_item(values)
    def add(self):
        try:
            item = self.validated()
            if any(x["item_id"].lower() == item["item_id"].lower() for x in self.inventory): raise ValueError("Item ID already exists.")
            self.inventory.append(item); self.commit("Item added")
        except ValueError as e: messagebox.showerror("Invalid Input", str(e))
    def update(self):
        if not self.table.selection(): return messagebox.showwarning("Select Item", "Select an item to update.")
        try:
            item = self.validated(); old = self.table.item(self.table.selection()[0], "values")[0]
            if any(x["item_id"].lower() == item["item_id"].lower() and x["item_id"] != old for x in self.inventory): raise ValueError("Item ID already exists.")
            self.inventory[next(i for i, x in enumerate(self.inventory) if x["item_id"] == old)] = item; self.commit("Item updated")
        except (ValueError, StopIteration) as e: messagebox.showerror("Update Error", str(e) or "The selected item is no longer available.")
    def delete(self):
        if not self.table.selection(): return messagebox.showwarning("Select Item", "Select an item to delete.")
        item_id = self.table.item(self.table.selection()[0], "values")[0]
        if messagebox.askyesno("Confirm Delete", f"Delete item {item_id}?"): self.inventory = [x for x in self.inventory if x["item_id"] != item_id]; self.commit("Item deleted")
    def select(self, _event):
        if not self.table.selection(): return
        item_id = self.table.item(self.table.selection()[0], "values")[0]
        try: item = next(x for x in self.inventory if x["item_id"] == item_id)
        except StopIteration: return
        for key, var in self.vars.items(): var.set(f"{item[key]:g}" if isinstance(item[key], (int, float)) else item[key])
    def clear(self):
        for v in self.vars.values(): v.set("")
        self.table.selection_remove(*self.table.selection()); self.status.set("Fields cleared")
    def rows(self, items):
        self.table.delete(*self.table.get_children())
        for index, x in enumerate(items):
            tag = "out" if x["status"] == "OUT OF STOCK" else "low" if x["status"] == "LOW STOCK" else "even" if index % 2 == 0 else "odd"
            self.table.insert("", "end", values=(x["item_id"], x["name"], x["category"], x["quantity"], f"{x['unit_price']:.2f}", x["supplier"], x["reorder"], f"{x['stock_value']:.2f}", x["status"]), tags=(tag,))
    def refresh(self):
        self.rows(self.inventory); values = {"items": len(self.inventory), "quantity": sum(x["quantity"] for x in self.inventory), "low": sum(x["status"] == "LOW STOCK" for x in self.inventory), "out": sum(x["status"] == "OUT OF STOCK" for x in self.inventory), "value": f"₹{sum(x['stock_value'] for x in self.inventory):,.2f}"}
        for key, value in values.items(): self.cards[key].config(text=value)
    def search(self):
        term = self.search_var.get().strip().lower()
        matches = [x for x in self.inventory if not term or any(term in str(x[k]).lower() for k in ("item_id", "name", "category", "supplier"))]; self.rows(matches); self.status.set(f"Showing {len(matches)} matching item(s)")
    def show_all(self): self.search_var.set(""); self.refresh(); self.status.set("Showing all items")
    def save(self):
        fields = [k for k, _ in FIELDS] + ["stock_value", "status"]
        with DATA_FILE.open("w", newline="", encoding="utf-8") as f: w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(self.inventory)
    def commit(self, message): self.save(); self.refresh(); self.clear(); self.status.set(message)
    def load(self):
        if DATA_FILE.exists():
            try:
                with DATA_FILE.open(encoding="utf-8") as f:
                    for row in csv.DictReader(f): self.inventory.append(prepare_item(row))
            except (OSError, ValueError): messagebox.showwarning("Data File", "Saved inventory data could not be loaded.")
        self.refresh()
    def export(self):
        if not self.inventory: return messagebox.showwarning("No Data", "Add an item before exporting.")
        path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile="inventory_report.csv", filetypes=[("CSV files", "*.csv")])
        if path:
            fields = [k for k, _ in FIELDS] + ["stock_value", "status"]
            with open(path, "w", newline="", encoding="utf-8") as f: w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(self.inventory)
            self.status.set(f"Exported {len(self.inventory)} inventory records")


if __name__ == "__main__":
    window = tk.Tk(); InventoryApp(window); window.mainloop()
