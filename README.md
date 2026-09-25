# Programming with Python (01AP0303) — Project Suite & Lab Manual

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Showcase-brightgreen?style=for-the-badge&logo=github)](https://tirth-byte.github.io/PWP/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![GUI Framework](https://img.shields.io/badge/GUI-Tkinter%20%2F%20ttk-orange?style=for-the-badge)](https://docs.python.org/3/library/tkinter.html)
[![Standard Library](https://img.shields.io/badge/Dependencies-Standard%20Library%20Only-success?style=for-the-badge)](#)

> **Live Interactive Showcase & Documentation:**  
> 🌐 **[https://tirth-byte.github.io/PWP/](https://tirth-byte.github.io/PWP/)**

---

## 👨‍🎓 Student & Course Credentials

| Detail | Information |
| :--- | :--- |
| **Student Name** | TIRTH KUMAR JANTILAL KAVAR (Tirth Patel) |
| **Enrollment ID** | `92500116005` |
| **GR Number** | `135965` |
| **Class & Batch** | `3EG1` |
| **Program** | B.Tech Computer Science & Engineering (AI & ML) |
| **Institution** | Faculty of Engineering & Technology, Marwadi University |
| **Subject** | Programming with Python (`01AP0303`) |

---

## 🚀 Overview

This repository contains the complete coursework, lab manuals, and five production-grade desktop GUI applications built for **Programming with Python (01AP0303)**. 

Every application is engineered exclusively with the **Python 3 Standard Library** (`tkinter`, `ttk`, `ast`, `csv`, `re`, `math`, `pathlib`, `logging`), requiring **zero third-party pip dependencies**.

---

## 🖥️ The 5 Python GUI Projects

### 1. Smart Calculator (`01_Smart_Calculator`)
- **Key Features:** Full arithmetic engine, parentheses, percentage calculations, trigonometric operations (`sin`, `cos`, `tan`), logarithmic functions (`log10`, `ln`), square root, factorials, and constants ($\pi, e$).
- **Safety Architecture:** Employs an Abstract Syntax Tree (`ast.NodeVisitor`) evaluator to safely evaluate math expressions without risky `eval()`.
- **Run:**
  ```bash
  python3 Python_GUI_Projects/01_Smart_Calculator/main.py
  ```

---

### 2. Employee Payroll System (`02_Employee_Payroll_System`)
- **Key Features:** Full CRUD management of employee records, dynamic calculation of basic salary, overtime earnings, performance bonuses, allowances, income tax withholding, and net salary.
- **Persistence:** Local CSV database engine (`payroll_data.csv`) with instant export and interactive Treeview table.
- **Run:**
  ```bash
  python3 Python_GUI_Projects/02_Employee_Payroll_System/main.py
  ```

---

### 3. Student Grade Analyzer (`03_Student_Grade_Analyzer`)
- **Key Features:** Validates 5-subject marks (0–100), checks 40-mark passing benchmarks, calculates overall percentage, assigns grades (A+, A, B+, B, C, D, F), and automatically detects strongest and weakest subjects.
- **Analytics:** Cohort-wide analytics dashboard calculating class average, highest mark, lowest mark, and CSV export.
- **Run:**
  ```bash
  python3 Python_GUI_Projects/03_Student_Grade_Analyzer/main.py
  ```

---

### 4. Inventory Tracker (`04_Inventory_Tracker`)
- **Key Features:** Stock catalog management, real-time inventory valuation ($\text{Qty} \times \text{Unit Price}$), automatic status badges (`IN STOCK`, `LOW STOCK`, `OUT OF STOCK`), and 4-way filter/search.
- **Persistence:** Real-time persistence to `inventory.csv` with low-stock reorder alerts.
- **Run:**
  ```bash
  python3 Python_GUI_Projects/04_Inventory_Tracker/main.py
  ```

---

### 5. Log File Analyzer (`05_Log_File_Analyzer`)
- **Key Features:** Regex-based event log parser for server and application log files. Categorizes logs by severity (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`), displays error rate percentages, and highlights anomalies.
- **Diagnostics:** Dedicated error viewer, live message query filtering, and CSV export for incident reports.
- **Run:**
  ```bash
  python3 Python_GUI_Projects/05_Log_File_Analyzer/main.py
  ```

---

## 📚 Lab Manuals & Documentation

| Document | Format | Description |
| :--- | :---: | :--- |
| **[Complete Python Lab Manual](01AP0303_Programming_with_Python_Complete_Lab_Manual.pdf)** | `PDF` | All-inclusive course lab manual |
| **[Lab Manual Experiments 01 to 05](01AP0303_Programming_with_Python_Lab_Manual_Experiments_01_to_05.pdf)** | `PDF` | Detailed write-ups for Experiments 1 through 5 |
| **[UNIFLEX Project Logbook](UNIFLEX_Project_Logbook.docx)** | `DOCX` | Project progress tracking and review logbook |

---

## ⚡ Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/Tirth-byte/PWP.git
cd PWP

# 2. Launch any application
python3 Python_GUI_Projects/01_Smart_Calculator/main.py
```

---

## 🌐 Live Web Showcase

Visit the GitHub Pages deployment to test interactive web simulators of each project, view screenshots in high resolution, and download documents:
👉 **[https://tirth-byte.github.io/PWP/](https://tirth-byte.github.io/PWP/)**

---

© 2026 **TIRTH KUMAR JANTILAL KAVAR**. All rights reserved.  
Faculty of Engineering & Technology, Marwadi University.
