# Labsheet Processing Workflow

This document outlines the systematic workflow for processing your markdown labsheet, executing the octave code, capturing output, and compiling the final document with your credentials loaded from `.env`.

## Step 1: Input Collection & Configuration
*   **User Action**: Upload or paste the markdown labsheet, and ensure the `.env` file is populated with the student's `STUDENT_NAME` and `STUDENT_ROLL_NUMBER` (using `.env.example` as a template).
*   **System Action**: Verify the labsheet contents and load the student credentials from the `.env` file to be used as environment variables.

## Step 2: Analysis & Parsing
*   Analyze the labsheet to break it down into separate questions/tasks.
*   Identify required mathematical models, inputs, formulas, and expected plots.

## Step 3: Octave Code Development
*   Write self-contained GNU Octave scripts (`.m` files) for each question.
*   **Beginner Coding Style**:
    *   Avoid using underscores in variable names (e.g., use `x1`, `yval`, `totalval`, `num`, `time` instead of `x_1`, `y_val`, `total_val`, `num_elements`, `time_vector`).
    *   Write variables in a simple style that looks like it was written by a lazy beginner (e.g., basic indices, short descriptive but simple names).
    *   Use simple, straightforward control flows and loops rather than overly advanced or optimized vector expressions when a beginner would write a basic loop. Use simple matrix and vector operations where possible. and keep it as lazy as possible like a lazy student made it.
*   Implement clean comments, simple and clear variables, and code that outputs results.
*   Add logic to export figures directly to vector format (PDF/EPS) or high-resolution PNG using the `print` command:
    ```octave
    % Save plot as PNG
    print('outputplot1.png', '-dpng', '-r300');
    ```

## Step 4: Automated Compilation & Execution
*   Instead of running individual steps manually, the Python script `generate_report.py` handles execution, capturing outputs, generating LaTeX, and compiling the PDF in one command:
    ```bash
    python3 generate_report.py
    ```

## Step 5: How the Automation Works
1.  **Reads Configuration**: Loads the `.env` file to fetch `STUDENT_NAME`, `STUDENT_ROLL_NUMBER`, and `MATLAB_DIR` (default: `src`).
2.  **Scans Matlab Files**: Scans the MATLAB directory for `.m` files, sorting them alphabetically.
3.  **Executes in Octave**: For each `.m` file:
    *   Runs `octave --no-gui --quiet <file.m>` inside the folder.
    *   Pipes console outputs to `<file>_output.txt`.
    *   Detects generated plots (any PNG files starting with the script's name, e.g., `parta1*.png`).
4.  **Generates LaTeX (`report.tex`)**: 
    *   Stamps Name and Roll Number in a simple block at the top of the report.
    *   Uses narrow margins (`geometry` with `margin=0.5in`) to keep page usage minimal.
    *   Includes source code using `listings` with small fonts (`\ttfamily\scriptsize`).
    *   Embeds console outputs in a `verbatim` environment.
    *   Positions plot images side-by-side using `minipage` blocks to save space, omitting verbose labels.
5.  **Compiles Report**: Automatically compiles the report via `pdflatex` to output `report.pdf`.

## Step 6: Verification & Delivery
*   Check the generated `report.pdf` to verify that all MATLAB scripts ran successfully and that plots are formatted side-by-side.
*   Deliver the compiled `report.pdf` and the individual MATLAB source files in the configured folder.
