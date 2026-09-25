# Employee Payroll System Using Python

## Objective
Calculate and manage employee gross pay, tax, deductions and net salary in a desktop GUI.

## Features
- Validated employee and salary inputs
- Overtime, gross salary, tax, deductions and net salary calculations
- Add, update, delete, select and clear employee records
- Payroll dashboard, automatic local persistence and CSV export

## Technologies Used
Python 3, Tkinter/ttk, `csv`, and `pathlib`.

## How the Program Works
The form is validated before `calculate_payroll()` applies the required formulas. Records are held as dictionaries in a list, shown in a Treeview, and saved to `payroll_data.csv`.

## How to Run
From this folder, run `python3 main.py`.

## Main Python Concepts Used
Lists, dictionaries, functions, classes, CSV files, validation, exceptions and GUI events.

## Important Functions
- `calculate_payroll()` calculates all payroll values.
- `add()`, `update()` and `delete()` manage records.
- `export()` creates a user-selected CSV report.

## Sample Input
Basic salary 30000, overtime 10 hours at 200, bonus 1500, allowances 1000, tax 10%, other deduction 500.

## Expected Output
Gross ₹34,500.00, tax ₹3,450.00, total deductions ₹3,950.00, net ₹30,550.00.

## Student Information
**Name:** TIRTH KUMAR JANTILAL KAVAR  
**Enrollment ID:** 92500116005  
**GR No.:** 135965  
**Class:** 3EG1
