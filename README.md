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
*   **One-Click Compilation**: The `run_all.sh` script executes all laboratory tasks sequentially and pipes outputs to log files.
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
├── .gitignore          # Keeps your Git repository clean
├── README.md           # This document
├── workflow.md         # Implementation steps & guidelines
├── run_all.sh          # Orchestrates Octave runs
├── parta1.m            # Task A1: Sinusoid Experiments
├── parta2.m            # Task A2: Impulse Train Construction
├── parta3.m            # Task A3: Sinc Function Properties
├── partb1.m            # Task B1: Convolution Lowpass Filter
├── partc1.m            # Task C1: DTFT of a Sinusoid
├── partc2.m            # Task C2: DTFT of a Rectangular Window
├── report.tex          # LaTeX source template
└── report.pdf          # Compiled final submission report
```

---

## 🚀 How to Run

### Prerequisites
Make sure GNU Octave and pdfTeX are installed:
```bash
sudo apt install octave texlive-latex-extra
```

### Execution
1. Run the simulation script to execute all tasks and generate plots:
   ```bash
   bash run_all.sh
   ```
2. Compile the report document:
   ```bash
   pdflatex report.tex && pdflatex report.tex
   ```

---

## 🔄 Reusing for Next Labsheets
To process a new lab sheet:
1. Replace the `.m` files with the new scripts (keeping variable naming conventions simple).
2. Update the filenames and paths inside `run_all.sh` and `report.tex`.
3. Re-run the scripts and compile to get your new PDF report with the header intact!
