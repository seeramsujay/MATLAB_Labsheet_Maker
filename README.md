# ⚡ DSP Lab Automation Engine

A clean, reproducible workspace designed to automate the process of executing Digital Signal Processing (DSP) lab sheets, capturing graphical results, and compiling a simple, compact 1st-year BTech student style LaTeX report with student credentials.

---

## 🛠️ System Architecture & Workflow

The workspace is structured to parse lab requirements, run simulations, and compile reports with zero manual formatting residue:

```
                      ┌────────────────────────┐
                      │  input/labsheet.pdf    │ (Raw Input)
                      └───────────┬────────────┘
                                  ▼ [markitdown]
                      ┌────────────────────────┐
                      │  input/labsheet.md     │ (Converted)
                      └───────────┬────────────┘
                                  ▼
                      ┌────────────────────────┐
                      │    Octave Scripts      │ ◄─── (Written inside src/)
                      └───────────┬────────────┘
                                  ▼
            ┌─────────────────────┴─────────────────────┐
            ▼                                           ▼
    ┌───────────────┐                           ┌───────────────┐
    │  src/*.png    │ (Plots)                   │  src/*.txt    │ (Console Logs)
    └───────┬───────┘                           └───────┬───────┘
            │                                           │
            └─────────────────────┬─────────────────────┘
                                  ▼
                      ┌────────────────────────┐
                      │  output/report.tex     │ ◄─── (LaTeX)
                      └───────────┬────────────┘
                                  ▼
                      ┌────────────────────────┐
                      │  output/report.pdf     │ ◄─── (Compiled PDF)
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
├── .env                # User config (STUDENT_NAME/ROLL/MATLAB_DIR/INPUT_DIR/OUTPUT_DIR)
├── .env.example        # Environment template file
├── .gitignore          # Keeps your Git repository clean
├── README.md           # This document
├── workflow.md         # Implementation steps & guidelines
├── SKILL.md            # LLM assistant instructions and rules
├── generate_report.py  # Dynamically executes MATLAB scripts and generates LaTeX report
├── input/              # Raw labsheet inputs and converted markdown files
│   └── .gitkeep        # Tracks directory in git
├── output/             # Output LaTeX reports and compiled PDFs
│   └── .gitkeep        # Tracks directory in git
└── src/                # Folder containing all MATLAB/Octave scripts
    ├── example.m       # Example task script
    └── ...             # Other lab tasks
```

---

## 🚀 How to Run

### Prerequisites
Make sure GNU Octave, Python 3, pdfTeX, and Microsoft MarkItDown are installed:
```bash
sudo apt install octave python3 texlive-latex-extra
pip install markitdown
```

### Execution
1. Place your raw labsheet file (e.g. `labsheet.pdf`) inside the `input/` folder.
2. Convert it to markdown using `markitdown`:
   ```bash
   markitdown input/labsheet.pdf -o input/labsheet.md
   ```
3. Read the converted `input/labsheet.md` and write the corresponding MATLAB/Octave `.m` scripts in the `src/` folder.
4. Run the automation generator script:
   ```bash
   python3 generate_report.py
   ```
   *Note: If you have already executed the scripts and manually placed screenshots (e.g. `1.1.png` for `LS1_01.m` and an optional `inference.txt`), run with the `--skip-run` (or `-s`) flag to compile the report directly without running Octave:*
   ```bash
   python3 generate_report.py --skip-run
   ```
This will run/skip scripts in `src/`, compile console logs, associate manual/generated screenshots, attach inferences from `inference.txt`, create `output/report.tex`, and compile the final PDF.

---

## 🔄 Reusing for Next Labsheets
To process a new lab sheet:
1. Place the new labsheet in `input/` and convert it using `markitdown`.
2. Clear old `.m` files in `src/` and paste/write the new ones.
3. Run `python3 generate_report.py`.
4. Your new `output/report.pdf` will be compiled immediately with your name and roll number.

