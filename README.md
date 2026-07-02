# ⚡ DSP Lab Automation Engine

A clean, reproducible workspace designed to automate the process of executing Digital Signal Processing (DSP) lab sheets, capturing graphical results, and compiling a simple, compact 1st-year BTech student style LaTeX report with student credentials.

---

## 🛠️ System Architecture & Workflow

The workspace is structured to parse lab requirements, run simulations, and compile reports with zero manual formatting residue:

```
                  ┌────────────────────────┐
                  │   Labsheet_X.md (Input) │
                  └───────────┬────────────┘
                              ▼
                  ┌────────────────────────┐
                  │    Octave Scripts      │ ◄─── (Beginner-style, no underscores)
                  └───────────┬────────────┘
                              ▼
        ┌─────────────────────┴─────────────────────┐
        ▼                                           ▼
┌───────────────┐                           ┌───────────────┐
│  PNG Plots    │                           │ Console Logs  │
└───────┬───────┘                           └───────┬───────┘
        │                                           │
        └─────────────────────┬─────────────────────┘
                              ▼
                  ┌────────────────────────┐
                  │    report.tex (LaTeX)  │ ◄─── (Pulls code & outputs inline)
                  └───────────┬────────────┘
                              ▼
                  ┌────────────────────────┐
                  │    report.pdf (Output) │ ◄─── (Simple compact student layout)
                  └────────────────────────┘
```

---

## ✨ Features

*   **Beginner-Style Code Generation**: Octave scripts are written with simple, clear variables (e.g., `x1`, `yval`) without underscores, matching typical student coding styles.
*   **One-Click Compilation**: The `generate_report.py` script executes all laboratory tasks sequentially, captures console logs, formats plots side-by-side, and compiles the final LaTeX report.
*   **LaTeX Report Template**: A simple, compact `report.tex` template designed to look like a student's basic work:
    *   Uses narrow margins (`geometry`) to keep the page count minimal.
    *   Stamps name and roll number in a simple block at the top of the report.
    *   Positions plot images side-by-side using `minipage` elements with minimal labels/captions to save maximum space.
    *   Uses `listings` to import and highlight `.m` script files directly from the disk.
    *   Uses `graphicx` to embed plots.
*   **Clean Repository State**: A robust `.gitignore` isolates build logs, temporary auxiliary files, and plot images so that you can reuse the directory for subsequent labsheets without cluttering Git history.

---

## 📂 Project Structure

```bash
.
├── .env                # User config (ignored by git; holds STUDENT_NAME/ROLL/MATLAB_DIR)
├── .env.example        # Environment template file
├── .gitignore          # Keeps your Git repository clean
├── README.md           # This document
├── workflow.md         # Implementation steps & guidelines
├── generate_report.py  # Dynamically executes MATLAB scripts and generates LaTeX report
└── src/                # Folder containing all MATLAB/Octave scripts
    ├── parta1.m        # Task A1: Sinusoid Experiments
    ├── parta2.m        # Task A2: Impulse Train Construction
    └── ...             # Other lab tasks
```

---

## 🚀 How to Run

### Prerequisites
Make sure GNU Octave, Python 3, and pdfTeX are installed:
```bash
sudo apt install octave python3 texlive-latex-extra
```

### Execution
1. Place all your MATLAB/Octave `.m` scripts in the `src/` folder.
2. Run the automation generator script:
   ```bash
   python3 generate_report.py
   ```
This will run each script, record the output logs, find any generated plots (`src/taskname*.png`), create a `report.tex` file, and compile it into a compact `report.pdf`.

---

## 🔄 Reusing for Next Labsheets
To process a new lab sheet:
1. Clear old `.m` files in `src/` and paste the new ones.
2. Run `python3 generate_report.py`.
3. Your new `report.pdf` will be compiled immediately with your name and roll number.
