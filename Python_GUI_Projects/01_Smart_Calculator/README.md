# Smart Calculator Using Python & Tkinter

## Objective
Build a safe, multi-functional desktop calculator for arithmetic, percentages and scientific calculations.

## Features
- Addition, subtraction, multiplication, division, decimals, signs, parentheses and percentages
- Square root, square, power, trigonometry, logarithms, factorial, pi and e
- Session history, reusable history entries, clear/backspace and friendly errors
- Responsive professional Tkinter interface

## Technologies Used
Python 3, Tkinter/ttk, `ast`, `math`, `operator`, and `re` (all standard library).

## How the Program Works
Button presses build an expression. `SafeEvaluator` parses it into an AST and permits only approved numbers, operators, constants and functions. The answer is displayed and added to session history.

## How to Run
From this folder, run `python3 main.py`. No package installation is needed.

## Main Python Concepts Used
Classes, functions, dictionaries, exception handling, event-driven programming, AST traversal and Tkinter variables.

## Important Functions
- `evaluate_expression()` normalizes and safely evaluates input.
- `calculate()` displays results or a friendly error.
- `clear_history()` confirms before removing history.

## Sample Input
`100 × 5%` or `sqrt(81)`

## Expected Output
`5` or `9`, with the complete calculation added to History.

## Student Information
**Name:** TIRTH KUMAR JANTILAL KAVAR  
**Enrollment ID:** 92500116005  
**GR No.:** 135965  
**Class:** 3EG1
