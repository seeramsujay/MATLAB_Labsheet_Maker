# Workflow

## 1. Convert Input to Markdown

Convert the labsheet PDF to markdown for easy reading:

```bash
markitdown input/labsheet.pdf -o input/labsheet.md
```

Read `input/labsheet.md` to understand each task, its formulas, parameters, and required plots.

## 2. Write Beginner Octave Scripts

Create one `.m` file per task in `src/` following these rules:

- **No underscores** in variable names (use `x1`, `yval`, not `x_1`, `y_val`)
- Simple loops and control flow (student style)
- Save plots with `print('taskname_plot1.png', '-dpng', '-r300')` — filenames must start with the script base name
- Keep comments short

## 3. Configure and Run

Ensure `.env` exists (copy from `.env.example` and fill in):

```env
STUDENT_NAME="Your Name"
STUDENT_ROLL_NUMBER="Roll Number"
MATLAB_DIR=src
INPUT_DIR=input
OUTPUT_DIR=output
```

Run the automation script:

```bash
python3 generate_report.py
```

*Note: If manually providing screenshots (e.g. `1.1.png` for `LS1_01.m`) and using an `inference.txt` file, run with skip-run enabled:*

```bash
python3 generate_report.py --skip-run
```

This compiles all MATLAB source files in `src/`, maps manual/generated screenshots, parses inferences, generates `output/report.tex`, and compiles the final report PDF.

---

## Quick Reference

| Step | Command |
|------|---------|
| Convert PDF | `markitdown input/labsheet.pdf -o input/labsheet.md` |
| Generate report | `python3 generate_report.py` |
| Output | `output/report.pdf` |

## Verification Checklist

- [ ] `input/labsheet.md` created
- [ ] `.m` files written to `src/` (no underscores in variable names)
- [ ] `print('scriptname_*.png', '-dpng', '-r300')` in every plotting script
- [ ] `.env` configured with name, roll number, and paths
- [ ] `python3 generate_report.py` runs without errors
- [ ] `output/report.pdf` generated and viewable
