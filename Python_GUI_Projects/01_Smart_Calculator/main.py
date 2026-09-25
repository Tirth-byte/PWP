"""Smart Calculator - a safe, session-based Tkinter calculator."""
import ast
import math
import operator
import tkinter as tk
from tkinter import messagebox, ttk

STUDENT = ("TIRTH KUMAR JANTILAL KAVAR", "Enrollment ID: 92500116005", "GR No.: 135965", "Class: 3EG1")
BG, CARD, NAVY, BLUE, TEXT, MUTED = "#eef2f7", "#ffffff", "#172554", "#2563eb", "#172033", "#64748b"


class SafeEvaluator(ast.NodeVisitor):
    """Evaluate only the arithmetic syntax exposed by the calculator."""
    binary = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
              ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod}
    unary = {ast.UAdd: operator.pos, ast.USub: operator.neg}
    functions = {"sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan,
                 "log": math.log10, "ln": math.log, "factorial": math.factorial}

    def visit_Expression(self, node): return self.visit(node.body)
    def visit_Constant(self, node):
        if isinstance(node.value, (int, float)): return node.value
        raise ValueError("Only numbers are allowed")
    def visit_BinOp(self, node):
        function = self.binary.get(type(node.op))
        if not function: raise ValueError("Unsupported operation")
        return function(self.visit(node.left), self.visit(node.right))
    def visit_UnaryOp(self, node):
        function = self.unary.get(type(node.op))
        if not function: raise ValueError("Unsupported sign")
        return function(self.visit(node.operand))
    def visit_Call(self, node):
        if not isinstance(node.func, ast.Name) or node.func.id not in self.functions or len(node.args) != 1:
            raise ValueError("Unsupported function")
        value = self.visit(node.args[0])
        if node.func.id == "factorial" and (value < 0 or int(value) != value):
            raise ValueError("Factorial needs a non-negative whole number")
        return self.functions[node.func.id](int(value) if node.func.id == "factorial" else value)
    def visit_Name(self, node):
        if node.id == "pi": return math.pi
        if node.id == "e": return math.e
        raise ValueError("Unknown value")
    def generic_visit(self, node): raise ValueError("Invalid expression")


def evaluate_expression(expression):
    cleaned = expression.replace("×", "*").replace("÷", "/").replace("^", "**")
    # A percent means divide the immediately preceding numeric value by 100.
    import re
    cleaned = re.sub(r"(\d+(?:\.\d+)?)%", r"(\1/100)", cleaned)
    return SafeEvaluator().visit(ast.parse(cleaned, mode="eval"))


class CalculatorApp:
    def __init__(self, root):
        self.root = root
        root.title("Smart Calculator Using Python & Tkinter")
        root.geometry("1200x750"); root.minsize(900, 650); root.configure(bg=BG)
        self.expression = tk.StringVar(); self.status = tk.StringVar(value="Ready")
        self.make_styles(); self.build_header(); self.build_ui()

    def make_styles(self):
        style = ttk.Style(); style.theme_use("clam")
        style.configure("Calc.TButton", font=("Arial", 13, "bold"), padding=11)
        style.configure("Accent.TButton", background=BLUE, foreground="white", font=("Arial", 12, "bold"), padding=11)

    def build_header(self):
        header = tk.Frame(self.root, bg=NAVY, padx=28, pady=16); header.pack(fill="x")
        tk.Label(header, text="SMART CALCULATOR", bg=NAVY, fg="white", font=("Arial", 24, "bold")).pack(side="left")
        info = tk.Frame(header, bg=NAVY); info.pack(side="right")
        for i, line in enumerate(STUDENT):
            tk.Label(info, text=line, anchor="e", bg=NAVY, fg="white" if i == 0 else "#bfdbfe",
                     font=("Arial", 10, "bold" if i == 0 else "normal")).pack(anchor="e")

    def build_ui(self):
        body = tk.Frame(self.root, bg=BG, padx=22, pady=22); body.pack(fill="both", expand=True)
        left = tk.Frame(body, bg=CARD, padx=20, pady=20); left.pack(side="left", fill="both", expand=True)
        right = tk.Frame(body, bg=CARD, padx=18, pady=18, width=330); right.pack(side="right", fill="y", padx=(18, 0)); right.pack_propagate(False)
        entry = tk.Entry(left, textvariable=self.expression, justify="right", font=("Arial", 28), relief="flat", bg="#f8fafc", fg=TEXT)
        entry.pack(fill="x", ipady=16, pady=(0, 15)); entry.focus_set(); entry.bind("<Return>", lambda _e: self.calculate())
        sci = tk.Frame(left, bg=CARD); sci.pack(fill="x", pady=(0, 10))
        for col, (label, value) in enumerate([("√", "sqrt("), ("x²", "**2"), ("xʸ", "**"), ("sin", "sin("), ("cos", "cos("), ("tan", "tan("), ("log", "log("), ("ln", "ln("), ("n!", "factorial("), ("π", "pi"), ("e", "e")]):
            ttk.Button(sci, text=label, command=lambda v=value: self.insert(v)).grid(row=col//6, column=col%6, sticky="nsew", padx=3, pady=3)
        for c in range(6): sci.columnconfigure(c, weight=1)
        grid = tk.Frame(left, bg=CARD); grid.pack(fill="both", expand=True)
        buttons = [("C", self.clear), ("⌫", self.backspace), ("(", lambda: self.insert("(")), (")", lambda: self.insert(")")),
                   ("7", None), ("8", None), ("9", None), ("÷", None), ("4", None), ("5", None), ("6", None), ("×", None),
                   ("1", None), ("2", None), ("3", None), ("-", None), ("±", self.toggle_sign), ("0", None), (".", None), ("+", None),
                   ("%", None), ("=", self.calculate)]
        for index, (label, command) in enumerate(buttons):
            r, c = divmod(index, 4); command = command or (lambda v=label: self.insert(v))
            ttk.Button(grid, text=label, command=command, style="Accent.TButton" if label == "=" else "Calc.TButton").grid(row=r, column=c, sticky="nsew", padx=4, pady=4, columnspan=3 if label == "=" else 1)
        for c in range(4): grid.columnconfigure(c, weight=1)
        for r in range(6): grid.rowconfigure(r, weight=1)
        tk.Label(right, text="CALCULATION HISTORY", bg=CARD, fg=TEXT, font=("Arial", 13, "bold")).pack(anchor="w")
        self.history = tk.Listbox(right, font=("Arial", 11), bg="#f8fafc", relief="flat", activestyle="none")
        self.history.pack(fill="both", expand=True, pady=12); self.history.bind("<Double-1>", self.use_history)
        ttk.Button(right, text="Clear History", command=self.clear_history).pack(fill="x")
        tk.Label(self.root, textvariable=self.status, anchor="w", bg="#dbeafe", fg=NAVY, padx=15, pady=6).pack(fill="x")

    def insert(self, value): self.expression.set(self.expression.get() + value); self.status.set("Editing expression")
    def clear(self): self.expression.set(""); self.status.set("Display cleared")
    def backspace(self): self.expression.set(self.expression.get()[:-1])
    def toggle_sign(self):
        value = self.expression.get().strip(); self.expression.set(value[1:-1] if value.startswith("- (") and value.endswith(")") else f"-({value})" if value else "-")
    def calculate(self):
        original = self.expression.get().strip()
        if not original: return
        try:
            result = evaluate_expression(original)
            if isinstance(result, float) and result.is_integer(): result = int(result)
            shown = f"{result:.12g}" if isinstance(result, float) else str(result)
            self.history.insert(0, f"{original} = {shown}"); self.expression.set(shown); self.status.set("Calculation completed")
        except ZeroDivisionError: messagebox.showerror("Calculation Error", "Division by zero is not allowed.")
        except (ValueError, SyntaxError, OverflowError) as error: messagebox.showerror("Calculation Error", str(error) or "Invalid expression")
    def clear_history(self):
        if self.history.size() and messagebox.askyesno("Clear History", "Remove all session calculations?"):
            self.history.delete(0, tk.END); self.status.set("History cleared")
    def use_history(self, _event):
        if self.history.curselection(): self.expression.set(self.history.get(self.history.curselection()[0]).split(" = ")[0])


if __name__ == "__main__":
    window = tk.Tk(); CalculatorApp(window); window.mainloop()
