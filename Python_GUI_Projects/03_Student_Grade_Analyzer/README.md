# Student Grade Analyzer Using Python

## Objective
Calculate student results and present individual and class performance in a clear GUI.

## Features
- Five validated marks (0–100), total, percentage, grade and subject-level pass/fail
- Add, update, delete, select and clear student records
- Dashboard with counts, class average, highest and lowest percentage
- Individual strongest/weakest subject report and CSV export

## Technologies Used
Python 3, Tkinter/ttk, `csv`, and `pathlib`.

## How the Program Works
`calculate_result()` validates marks, assigns the percentage grade and marks a student failed if any subject is below 40. Records populate the table and dashboard and persist in `student_results.csv`.

## How to Run
From this folder, run `python3 main.py`.

## Main Python Concepts Used
Lists, dictionaries, functions, classes, comprehensions, CSV files, validation and event handling.

## Important Functions
- `calculate_result()` produces the complete result.
- `refresh()` updates the table and dashboard.
- `select()` fills the form and individual report.

## Sample Input
Marks: 92, 88, 95, 90, 89.

## Expected Output
Total 454/500, percentage 90.80%, grade A+, Pass; strongest Subject 3, weakest Subject 2.

## Student Information
**Name:** TIRTH KUMAR JANTILAL KAVAR  
**Enrollment ID:** 92500116005  
**GR No.:** 135965  
**Class:** 3EG1
