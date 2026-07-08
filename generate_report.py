#!/usr/bin/env python3
import os
import sys
import glob
import subprocess

def load_env():
    env_vars = {}
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split('=', 1)
                    if len(parts) == 2:
                        key = parts[0].strip()
                        val = parts[1].strip().strip('"').strip("'")
                        env_vars[key] = val
    return env_vars

def main():
    env = load_env()
    student_name = env.get('STUDENT_NAME', 'Student Name')
    student_roll = env.get('STUDENT_ROLL_NUMBER', 'Roll Number')
    matlab_dir = env.get('MATLAB_DIR', 'src')
    output_dir = env.get('OUTPUT_DIR', 'output')

    print(f"Loading files from: {matlab_dir}")
    print(f"Saving outputs to: {output_dir}")
    print(f"Student: {student_name} ({student_roll})")

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(matlab_dir):
        print(f"Error: Directory '{matlab_dir}' does not exist.")
        sys.exit(1)

    m_files = sorted(glob.glob(os.path.join(matlab_dir, "*.m")))
    if not m_files:
        print(f"No .m files found in '{matlab_dir}'.")
        sys.exit(1)

    sections_data = []

    for m_file in m_files:
        base_name = os.path.basename(m_file)
        name_no_ext = os.path.splitext(base_name)[0]
        print(f"\n--- Processing {base_name} ---")

        # Clean old output/plots in MATLAB_DIR for this task
        old_plots = glob.glob(os.path.join(matlab_dir, f"{name_no_ext}*.png"))
        for p in old_plots:
            try:
                os.remove(p)
            except Exception:
                pass
        
        old_output = os.path.join(matlab_dir, f"{name_no_ext}_output.txt")
        if os.path.exists(old_output):
            try:
                os.remove(old_output)
            except Exception:
                pass

        # Run script using Octave
        print(f"Running script via Octave...")
        cmd = ["octave", "--no-gui", "--quiet", base_name]
        try:
            result = subprocess.run(
                cmd,
                cwd=matlab_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=30
            )
            output_text = result.stdout.strip()
        except subprocess.TimeoutExpired:
            output_text = "Error: Script execution timed out (30s limit)."
        except Exception as e:
            output_text = f"Error running script: {str(e)}"

        # Save console output if any
        if output_text:
            with open(os.path.join(matlab_dir, f"{name_no_ext}_output.txt"), "w") as f:
                f.write(output_text)
            print("Captured console output.")
        else:
            print("No console output.")

        # Detect generated plots (PNGs starting with the script name)
        plots = sorted(glob.glob(os.path.join(matlab_dir, f"{name_no_ext}*.png")))
        print(f"Found {len(plots)} plot(s): {[os.path.basename(p) for p in plots]}")

        sections_data.append({
            "name": name_no_ext,
            "m_file": base_name,
            "has_output": bool(output_text),
            "output_file": f"{name_no_ext}_output.txt" if output_text else None,
            "plots": [os.path.basename(p) for p in plots]
        })

    # Generate LaTeX content
    print("\nGenerating report.tex...")
    
    # Escape LaTeX special chars for student name/roll
    def latex_escape(text):
        return text.replace('&', '\\&').replace('%', '\\%').replace('$', '\\$').replace('#', '\\#').replace('_', '\\_')

    esc_name = latex_escape(student_name)
    esc_roll = latex_escape(student_roll)

    tex_content = []
    tex_content.append(r"\documentclass[10pt]{article}")
    tex_content.append(r"\usepackage[margin=0.5in]{geometry}")
    tex_content.append(r"\usepackage{graphicx}")
    tex_content.append(r"\usepackage{listings}")
    tex_content.append(r"\usepackage{xcolor}")
    tex_content.append(r"\usepackage{float}")
    tex_content.append(r"\usepackage{microtype}")
    tex_content.append(r"\raggedbottom")
    
    # Simple lstlisting style for beginner student look
    tex_content.append(r"\lstset{")
    tex_content.append(r"    language=Octave,")
    tex_content.append(r"    basicstyle=\ttfamily\scriptsize,")
    tex_content.append(r"    breaklines=true,")
    tex_content.append(r"    frame=single,")
    tex_content.append(r"    commentstyle=\color{gray},")
    tex_content.append(r"    keywordstyle=\color{blue},")
    tex_content.append(r"    showstringspaces=false")
    tex_content.append(r"}")

    tex_content.append(r"\begin{document}")
    
    # Simple, compact BTech student style header
    tex_content.append(r"\noindent")
    tex_content.append(f"\\textbf{{Name:}} {esc_name} \\hfill \\textbf{{Roll No:}} {esc_roll}\\\\")
    tex_content.append(r"\noindent\rule{\textwidth}{0.4pt}")
    tex_content.append(r"\vspace{-0.2cm}")
    tex_content.append(r"\begin{center}")
    tex_content.append(r"    \subsection*{DSP Laboratory Report}")
    tex_content.append(r"\end{center}")
    tex_content.append(r"\vspace{-0.2cm}")

    for sec in sections_data:
        tex_content.append(f"\\subsection*{{Task: {latex_escape(sec['name'])}}}")
        tex_content.append(r"\vspace{-0.1cm}")
        
        # Include code
        tex_content.append(r"\noindent\textbf{Source Code:}")
        tex_content.append(f"\\lstinputlisting{{{matlab_dir}/{sec['m_file']}}}")
        tex_content.append(r"\vspace{-0.3cm}")

        # Code output and plots block
        if sec['has_output'] or sec['plots']:
            # If we have both output and plots, or multiple plots, we arrange them compactly.
            # Let's show console output if it exists
            if sec['has_output']:
                tex_content.append(r"\noindent\textbf{Console Output:}")
                tex_content.append(r"\begin{verbatim}")
                # Load output snippet (limit lines if extremely long to keep compact)
                output_path = os.path.join(matlab_dir, sec['output_file'])
                with open(output_path, 'r') as f:
                    lines = f.readlines()
                    # Keep only first 20 lines to save space, with warning if truncated
                    if len(lines) > 20:
                        tex_content.append("".join(lines[:20]) + "\n... [Output Truncated to Save Space] ...")
                    else:
                        tex_content.append("".join(lines))
                tex_content.append(r"\end{verbatim}")
                tex_content.append(r"\vspace{-0.2cm}")

            # Show plots side-by-side to save space
            if sec['plots']:
                tex_content.append(r"\noindent\textbf{Plots:}")
                tex_content.append(r"\begin{figure}[H]")
                tex_content.append(r"    \centering")
                
                num_plots = len(sec['plots'])
                if num_plots == 1:
                    # Single plot
                    tex_content.append(f"    \\includegraphics[width=0.65\\textwidth]{{{matlab_dir}/{sec['plots'][0]}}}")
                else:
                    # Side-by-side plots (2 per row)
                    for j, plot_file in enumerate(sec['plots']):
                        tex_content.append(f"    \\begin{{minipage}}[b]{{0.48\\textwidth}}")
                        tex_content.append(f"        \\centering")
                        tex_content.append(f"        \\includegraphics[width=\\textwidth]{{{matlab_dir}/{plot_file}}}")
                        tex_content.append(f"    \\end{{minipage}}")
                        if j % 2 == 1 and j < num_plots - 1:
                            tex_content.append(r"    \\")
                        elif j < num_plots - 1:
                            tex_content.append(r"\hfill")
                
                tex_content.append(r"\end{figure}")
        
        tex_content.append(r"\hrule")

    tex_content.append(r"\end{document}")

    tex_path = os.path.join(output_dir, "report.tex")
    with open(tex_path, "w") as f:
        f.write("\n".join(tex_content))
    print(f"Created {tex_path} successfully.")

    # Compile LaTeX report
    print(f"\nCompiling {tex_path} to PDF...")
    try:
        # Run pdflatex twice for reference resolving (if any)
        for _ in range(2):
            subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", f"-output-directory={output_dir}", tex_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
        print(f"Compiled report.pdf inside {output_dir} successfully!")
        
        # Clean build files in output directory
        for ext in ["aux", "log", "out"]:
            for f in glob.glob(os.path.join(output_dir, f"report.{ext}")):
                try:
                    os.remove(f)
                except Exception:
                    pass
    except Exception as e:
        print(f"Error compiling LaTeX report. Make sure pdflatex is installed. Details: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
