# Labsheet Processing Workflow

This document outlines the systematic workflow for processing your markdown labsheet, executing the octave code, capturing output, and compiling the final document with your roll number.

## Step 1: Input Collection
*   **User Action**: Upload or paste the markdown labsheet and provide the student Roll Number.
*   **System Action**: Verify the labsheet contents and store the roll number as an environment variable or config parameter.

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
*   Write a LaTeX document (`labsheet_report.tex`) using standard packages:
    *   `fancyhdr`: For placing the Roll Number in the header of every page.
    *   `listings`: For syntax highlighting the GNU Octave source code.
    *   `graphicx`: For embedding generated plots.
    *   `geometry`: For page layouts and margins.
*   **Header Configuration**:
    ```latex
    \usepackage{fancyhdr}
    \pagestyle{fancy}
    \fancyhf{}
    \rhead{Roll Number: [YOUR_ROLL_NUMBER]}
    \lhead{Lab Report}
    \cfoot{\thepage}
    ```

## Step 6: LaTeX Compilation
*   Compile the LaTeX report using `pdflatex`:
    ```bash
    pdflatex -interaction=nonstopmode labsheet_report.tex
    ```
*   Verify pagination, code wrapping, image alignment, and header formatting in the generated PDF.

## Step 7: Delivery
*   Provide the final compiled PDF.
*   Provide the individual `.m` source files for backup.
