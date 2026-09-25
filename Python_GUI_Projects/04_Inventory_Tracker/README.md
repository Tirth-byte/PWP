# Inventory Tracker Using Python

## Objective
Manage, search and monitor item stock and inventory value in a desktop application.

## Features
- Add, update, delete, select and search items
- Automatic stock value and IN STOCK, LOW STOCK or OUT OF STOCK status
- Dashboard totals, color-highlighted warnings, local persistence and CSV export
- Search by item ID, name, category or supplier

## Technologies Used
Python 3, Tkinter/ttk, `csv`, and `pathlib`.

## How the Program Works
The inventory is primarily a list of dictionaries. `prepare_item()` validates data and derives value/status. The Treeview, dashboard and `inventory.csv` are refreshed after changes.

## How to Run
From this folder, run `python3 main.py`.

## Main Python Concepts Used
Lists, dictionaries, functions, classes, CSV persistence, searching, validation and GUI events.

## Important Functions
- `prepare_item()` validates and calculates an item.
- `search()` filters four fields without changing saved data.
- `save()` and `export()` write CSV files.

## Sample Input
Item I002, Printer Paper, quantity 5, unit price 280, reorder level 8.

## Expected Output
Stock value ₹1,400.00 and status LOW STOCK.

## Student Information
**Name:** TIRTH KUMAR JANTILAL KAVAR  
**Enrollment ID:** 92500116005  
**GR No.:** 135965  
**Class:** 3EG1
