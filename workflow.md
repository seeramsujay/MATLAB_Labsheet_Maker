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

## Step 4: Octave Execution & Verification
*   Execute each script programmatically:
    ```bash
    octave --no-gui --quiet task_1.m > task_1_output.txt
    ```
*   Verify output logs and ensure plots are rendered correctly without GUI popup requirements.

## Step 5: LaTeX Formatting & Styling
*   Write a simple LaTeX document (`labsheet_report.tex`) designed to look like a basic, space-efficient 1st-year BTech student report:
    *   **Compact Margins**: Use `geometry` with narrow margins (e.g., `margin=0.5in`) to minimize page usage and pack code/plots tightly.
    *   **Simple Identification**: Avoid professional page headers/footers. Instead, use a basic text block at the top of the report with the student's name and roll number.
    *   **Side-by-Side Plots**: Put plot images side-by-side using `minipage` blocks to save space.
    *   **Minimal Labeling**: Do not add figure numbers or verbose captions unless absolutely necessary; keep them simple or unlabelled to look like a student's quick output.
    *   `listings`: For syntax highlighting the GNU Octave source code.
    *   `graphicx`: For embedding generated plots.
*   **Student Details Block**:
    ```latex
    \noindent \textbf{Name:} \studentname \hfill \textbf{Roll No:} \studentroll
    \hrule
    \vspace{0.2cm}
    ```
    *(Note: The name and roll number macro variables `\studentname` and `\studentroll` are defined by reading the `.env` variables dynamically during the document generation or compilation step.)*

## Step 6: LaTeX Compilation
*   Load environment variables from `.env` and compile the LaTeX report:
    ```bash
    # Load .env variables
    export $(grep -v '^#' .env | xargs)
    
    # Compile the document (incorporating env vars)
    pdflatex -interaction=nonstopmode labsheet_report.tex
    ```
*   Verify pagination, code wrapping, image alignment, and header formatting in the generated PDF.

## Step 7: Delivery
*   Provide the final compiled PDF.
*   Provide the individual `.m` source files for backup.
