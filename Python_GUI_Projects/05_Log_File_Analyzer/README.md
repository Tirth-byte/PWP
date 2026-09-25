# Log File Analyzer Using Python, Logging & CSV

## Objective
Read application/server logs, classify events, expose problems and export analysis results.

## Features
- File dialog for `.log` and `.txt` files
- DEBUG, INFO, WARNING, ERROR and CRITICAL recognition
- Live level/message filtering and a separate error/critical table
- Counts, error percentage, most common error, invalid-line handling and CSV export
- Internal activity recording in `app_activity.log`

## Technologies Used
Python 3, Tkinter/ttk, `logging`, `csv`, `re`, `collections`, `os`, and `pathlib`.

## How the Program Works
Each line is matched against a regular expression. Valid entries become dictionaries; invalid non-empty lines are counted and skipped. Tables, counts and the summary are then refreshed.

## How to Run
From this folder, run `python3 main.py`, browse to `sample_server.log`, and click **Analyze Logs**.

## Main Python Concepts Used
Regular expressions, lists, dictionaries, counters, file handling, logging, exception handling and event-driven GUIs.

## Important Functions
- `parse_log_lines()` parses valid entries and counts invalid lines.
- `filter_rows()` combines level and text filters.
- `update_summary()` calculates report statistics.

## Sample Input
`2026-09-25 10:17:05 ERROR Database connection failed`

## Expected Output
An ERROR row, updated ERROR count and recalculated error percentage. The supplied sample has 7 valid and 1 invalid line.

## Student Information
**Name:** TIRTH KUMAR JANTILAL KAVAR  
**Enrollment ID:** 92500116005  
**GR No.:** 135965  
**Class:** 3EG1
