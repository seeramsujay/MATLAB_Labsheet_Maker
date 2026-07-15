---
name: matlab-labsheet
description: Use this skill when requested to process MATLAB/Octave labsheets, write beginner-style MATLAB/Octave code, convert PDF or DOCX inputs to markdown using markitdown, compile reports using generate_report.py, or run tasks via opencode or claude code.
---

# MATLAB Labsheet Maker Workflow

This skill guides the AI model in processing labsheets, writing beginner-style MATLAB/Octave scripts, running them, and compiling a PDF report using the automation script.

---

## 1. Input Collection & Parsing with MarkItDown

Raw labsheets and questions should be placed in the `input/` directory. If the user provides an input labsheet in a binary or rich text format (e.g., `.pdf`, `.docx`, `.pptx`, `.xlsx`, `.png`), you **must** convert it to Markdown first using `markitdown` inside the `input/` folder to easily parse the structure, formulas, and questions.

### CLI Conversion
Run the following terminal command to convert the input file:
```bash
markitdown input/<input_file> -o input/labsheet.md
```

### Python Conversion (Alternative)
If you need programmatic conversion or custom parsing within a script:
```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("input/labsheet.pdf")
with open("input/labsheet.md", "w") as f:
    f.write(result.text_content)
```

Once converted, read `input/labsheet.md` to identify:
- Each individual question or task (e.g., Task 1, Task 2).
- Mathematical formulas, parameters, inputs, and expected outputs.
- Specific plots requested by the labsheet.

---

## 2. Beginner-Style MATLAB/Octave Coding Guidelines

When generating the MATLAB/Octave `.m` scripts, you must adopt a **beginner/lazy student coding style**. Avoid writing overly polished, expert-level MATLAB code.

### Guidelines:
1. **Variable Naming**:
   - **DO NOT** use underscores in variable names (e.g., use `x1`, `yval`, `totalval`, `num`, `time` instead of `x_1`, `y_val`, `total_val`, `num_elements`, `time_vector`).
   - Keep variable names simple and short, similar to what a student who is coding in a hurry would write.
2. **Control Flow**:
   - Prefer simple, straightforward control flows and basic loops (`for` and `while`) where a beginner would write them. Avoid using highly optimized vector expressions when a loop is simpler to understand or write for a novice.
   - Simple matrix and vector operations (like `x = 0:0.1:10` or `y = sin(x)`) are encouraged and expected.
3. **Commenting**:
   - Keep comments simple, short, and explanatory. Do not write excessively verbose docstrings.
4. **Plot Exporting**:
   - Every script must save its generated figure(s) using the `print` command.
   - Use high-resolution PNG (`-dpng`, `-r300`).
   - The file name of the plot **MUST** start with the script's base name (e.g., script `parta.m` should save plots as `parta_plot1.png`, `parta_plot2.png`, etc.).
   ```octave
   % Save plot as PNG
   print('parta_plot1.png', '-dpng', '-r300');
   ```

Store all `.m` scripts inside the MATLAB source directory (configured as `MATLAB_DIR` in `.env`, defaults to `src`).

---

## 3. Configuration & Automated Compilation (Delegating to Python)

### IMPORTANT: Delegate Execution & Compilation
The AI agent's sole responsibility for code execution and reporting is to generate the appropriate `.m` files. 
- **DO NOT** manually run the Octave scripts.
- **DO NOT** manually parse outputs or plots.
- **DO NOT** write or modify LaTeX templates (`report.tex`).
- **DO NOT** manually run `pdflatex`.

All parsing, execution, output capture, plot discovery, LaTeX formatting, and PDF compilation are automatically handled by the `generate_report.py` python script. Simply write the scripts to `src/` and run the automation command.

### Step A: Configure `.env`
Ensure that a `.env` file exists at the root of the project. If it is missing, create it using `.env.example` as a template:
```env
STUDENT_NAME="Student Name"
STUDENT_ROLL_NUMBER="Roll Number"
MATLAB_DIR="src"
INPUT_DIR="input"
OUTPUT_DIR="output"
PICS_DIR="pics"
```

### Step B: Run Compilation Script
Execute the compilation script to compile the PDF into the `output/` directory:
```bash
python3 generate_report.py [options]
```

#### Available CLI Options:
*   `--skip-run`, `-s`: Skips executing the MATLAB/Octave scripts. Instead, it reads existing manual output text files and links manually provided screenshots directly.
*   `--inference <path>`, `-i <path>`: Specifies a custom path to the inference text file (defaults to looking for `inference.txt` in the root, `src/`, or `input/` directory).

*   **Pics directory override**: If matching screenshots are found in the `pics/` directory (or configured `PICS_DIR`), execution of the corresponding `.m` script is automatically skipped, and those screenshots are used directly.
*   **Standard matching**: Files starting with the script name (e.g. `LS1_01_plot.png` for `LS1_01.m`).
*   **Numbered matching**: For scripts matching the pattern `LS<labsheet>_<question>` (e.g. `LS1_01.m`), screenshots can be named like `<labsheet>.<question>.png` (e.g. `1.1.png`, `1.1_2.png`, etc.) or `<labsheet>_<question>.png` and can be placed in `pics/`, `input/`, or `src/` directory.

#### Inferences Integration (`inference.txt`):
You can place an `inference.txt` file in the root, `src/`, or `input/` directory. 
*   **Task-Specific Inferences**: Define task-specific inferences using headers matching the task name (e.g. `[LS1_01]`, `LS1_01:`, `[1.1]`, `1.1:`, `Task 1:`). These are placed directly at the bottom of the corresponding task inside the report. Alternatively, you can use separate files named like `<task>_inference.txt` (e.g., `LS1_01_inference.txt`).
*   **Global Inference**: Text at the top of the file (before any headers) or under headers like `[Overall]`, `[General]`, or `[Global]` will be appended as a main "Inference" section at the end of the entire report.

### What the compiler does behind the scenes:
1. Scans the configured `MATLAB_DIR` (default: `src`) directory for `.m` files, sorted naturally.
2. For each task, checks for existing screenshots in `pics/`. If found, skips execution for this task and loads existing console outputs.
3. If no screenshots are found in `pics/` and `--skip-run` is not enabled, runs the script via GNU Octave in quiet, non-GUI mode, piping output to `<file>_output.txt`. If `--skip-run` is enabled, checks for existing outputs.
4. Detects plots/screenshots from `pics/` (if skipped/overridden) or `src/`/`input/` (checking both standard base names and `<labsheet>.<question>` formats).
4. Matches and reads task-specific and overall inferences from `inference.txt` or dedicated files.
5. Auto-generates `report.tex` inside the configured `OUTPUT_DIR` (default: `output`) using narrow margins, embedding the source code, output snippets, plots side-by-side, and formatting inferences.
6. Compiles the document to `report.pdf` inside `output/` using `pdflatex` (runs twice) and cleans up auxiliary files.

---

## 4. Usage in Terminal AI Platforms (OpenCode / Claude Code)

When operating inside AI platforms like **OpenCode** (`opencode`) or **Claude Code** (`claude` CLI):

### Direct Commands
You can run task prompts or commands directly:
- **Analyze and compile report**:
  ```bash
  opencode run "Convert input/labsheet.pdf to markdown using markitdown, create beginner octave scripts in src, and run generate_report.py to compile the PDF in output"
  ```
- **Run in Background**: Use background commands with terminal execution features to save time during compiler runs.
- **Verification**: Always inspect the terminal output from `python3 generate_report.py` and verify `output/report.pdf` has been created successfully.

### Workflow Verification Checklist
- [ ] Converted input labsheet to `input/labsheet.md` via `markitdown`.
- [ ] Created all `.m` files in `src/` (or configured directory).
- [ ] Verified variable names contain no underscores and loops are simple.
- [ ] Ensured `print('scriptname_plot*.png', '-dpng', '-r300')` is included in plotting scripts.
- [ ] Staged student credentials in `.env`.
- [ ] Ran `python3 generate_report.py` successfully.
- [ ] Verified creation of `output/report.pdf`.
