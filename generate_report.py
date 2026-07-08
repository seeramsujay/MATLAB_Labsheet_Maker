#!/usr/bin/env python3
import os
import sys
import glob
import subprocess
import re
import argparse

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

def natural_key(string):
    return [int(s) if s.isdigit() else s.lower() for s in re.split(r'(\d+)', string)]

def latex_escape(text):
    if not text:
        return ""
    lines = []
    for line in text.splitlines():
        escaped_line = ""
        for char in line:
            if char == '\\':
                escaped_line += r'\textbackslash{}'
            elif char in ('&', '%', '$', '#', '_', '{', '}'):
                escaped_line += '\\' + char
            elif char == '~':
                escaped_line += r'\textasciitilde{}'
            elif char == '^':
                escaped_line += r'\textasciicircum{}'
            else:
                escaped_line += char
        lines.append(escaped_line)
    return "\n".join(lines)

def parse_inference_file(file_path):
    sections = {}
    global_lines = []
    current_section = None
    current_lines = []
    
    # Header pattern to match:
    # 1. [LS1_01] or [1.1]
    # 2. LS1_01: or 1.1: or LS1_01 -
    # 3. Task LS1_01 or Task 1.1: or Task 1:
    header_pat = re.compile(
        r"^(?:"
        r"\[([\w\.]+)\]"
        r"|([\w\.]+)\s*[:\-]+"
        r"|Task\s+([\w\.]+)\s*[:\-]*"
        r")$",
        re.IGNORECASE
    )
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            stripped = line.strip()
            if not stripped:
                if current_section or global_lines or current_lines:
                    current_lines.append(line)
                continue
                
            match = header_pat.match(stripped)
            if match:
                # Save previous section
                if current_section:
                    sections[current_section] = "".join(current_lines).strip()
                else:
                    global_lines.extend(current_lines)
                
                # Extract and normalize section key
                current_section = next(g for g in match.groups() if g is not None).strip().lower()
                current_lines = []
            else:
                current_lines.append(line)
                
    if current_section:
        sections[current_section] = "".join(current_lines).strip()
    else:
        global_lines.extend(current_lines)
        
    return sections, "".join(global_lines).strip()

def load_inference(inference_file, matlab_dir, input_dir):
    target_files = []
    if inference_file:
        target_files.append(inference_file)
    else:
        # Default search order for inference.txt
        target_files.extend([
            "inference.txt",
            os.path.join(matlab_dir, "inference.txt"),
            os.path.join(input_dir, "inference.txt")
        ])
        
    for path in target_files:
        if os.path.exists(path):
            print(f"Found inference file at: {path}")
            sections, global_inference = parse_inference_file(path)
            
            # Merge general/overall sections into global_inference
            global_keys = ['global', 'overall', 'inference', 'general']
            for gk in global_keys:
                if gk in sections:
                    if global_inference:
                        global_inference += "\n\n" + sections[gk]
                    else:
                        global_inference = sections[gk]
                    del sections[gk]
            return sections, global_inference
            
    return {}, ""

def find_task_inference(task_name, sections, matlab_dir, input_dir):
    task_lower = task_name.lower()
    
    # 1. Search for task-specific separate files
    file_patterns = [
        f"{task_name}_inference.txt",
        f"{task_name}_inf.txt",
        f"{task_lower}_inference.txt",
        f"{task_lower}_inf.txt",
    ]
    
    m = re.match(r"(?i)LS(?:_)?(\d+)[_\-\s\.]*(\d+)", task_name)
    if m:
        l_str, q_str = m.groups()
        l_val = int(l_str)
        q_val = int(q_str)
        file_patterns.extend([
            f"{l_val}.{q_val}_inference.txt",
            f"{l_val}.{q_val}_inf.txt",
            f"{l_val}_{q_val}_inference.txt",
        ])
        
    for fn in file_patterns:
        for folder in [matlab_dir, input_dir]:
            path = os.path.join(folder, fn)
            if os.path.exists(path):
                print(f"Found task-specific inference file for {task_name} at: {path}")
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read().strip()
                    
    # 2. Search in parsed section dict keys
    keys_to_check = [task_lower]
    if m:
        l_str, q_str = m.groups()
        l_val = int(l_str)
        q_val = int(q_str)
        keys_to_check.extend([
            f"{l_val}.{q_val}",
            f"{l_val}.{q_str}",
            f"{l_str}.{q_str}",
            f"{l_val}_{q_val}",
            f"task {l_val}",
            f"task {task_lower}",
            f"task {l_val}.{q_val}",
        ])
        
    for k in keys_to_check:
        if k in sections:
            print(f"Found inference for {task_name} in section: '{k}'")
            return sections[k]
            
    return None

def find_screenshots(matlab_dir, input_dir, name_no_ext):
    patterns = [
        os.path.join(matlab_dir, f"{name_no_ext}*.png"),
        os.path.join(matlab_dir, f"{name_no_ext}*.jpg"),
        os.path.join(matlab_dir, f"{name_no_ext}*.jpeg"),
        os.path.join(input_dir, f"{name_no_ext}*.png"),
        os.path.join(input_dir, f"{name_no_ext}*.jpg"),
        os.path.join(input_dir, f"{name_no_ext}*.jpeg"),
    ]
    
    m = re.match(r"(?i)LS(?:_)?(\d+)[_\-\s\.]*(\d+)", name_no_ext)
    if m:
        l_str, q_str = m.groups()
        l_val = int(l_str)
        q_val = int(q_str)
        
        q_representations = [q_str, str(q_val)]
        l_representations = [l_str, str(l_val)]
        
        for l_repr in l_representations:
            for q_repr in q_representations:
                prefix_dot = f"{l_repr}.{q_repr}"
                prefix_underscore = f"{l_repr}_{q_repr}"
                prefix_dash = f"{l_repr}-{q_repr}"
                
                for pref in [prefix_dot, prefix_underscore, prefix_dash]:
                    for folder in [matlab_dir, input_dir]:
                        for ext in ["png", "jpg", "jpeg", "PNG", "JPG", "JPEG"]:
                            patterns.append(os.path.join(folder, f"{pref}.{ext}"))
                            patterns.append(os.path.join(folder, f"{pref}_*.{ext}"))
                            patterns.append(os.path.join(folder, f"{pref}-*.{ext}"))

    found_files = []
    seen = set()
    for pat in patterns:
        for p in glob.glob(pat):
            abs_p = os.path.abspath(p)
            if abs_p not in seen:
                seen.add(abs_p)
                found_files.append(p)
                
    return sorted(found_files, key=natural_key)

def main():
    parser = argparse.ArgumentParser(description="DSP Lab Automation Engine - LaTeX Report Generator")
    parser.add_argument("--skip-run", "-s", action="store_true", help="Skip executing the MATLAB/Octave scripts and just use existing outputs/plots")
    parser.add_argument("--inference", "-i", type=str, default=None, help="Path to the inference text file (default: looks for inference.txt)")
    args = parser.parse_args()

    env = load_env()
    student_name = env.get('STUDENT_NAME', 'Student Name')
    student_roll = env.get('STUDENT_ROLL_NUMBER', 'Roll Number')
    matlab_dir = env.get('MATLAB_DIR', 'src')
    output_dir = env.get('OUTPUT_DIR', 'output')
    input_dir = env.get('INPUT_DIR', 'input')
    
    skip_run = args.skip_run or (env.get('SKIP_RUN', 'false').lower() in ('true', '1', 'yes'))

    print(f"Loading files from: {matlab_dir}")
    print(f"Saving outputs to: {output_dir}")
    print(f"Student: {student_name} ({student_roll})")
    print(f"Skip Run: {skip_run}")

    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(matlab_dir):
        print(f"Error: Directory '{matlab_dir}' does not exist.")
        sys.exit(1)

    m_files = sorted(glob.glob(os.path.join(matlab_dir, "*.m")), key=natural_key)
    if not m_files:
        print(f"No .m files found in '{matlab_dir}'.")
        sys.exit(1)

    sections_inference, global_inference = load_inference(args.inference, matlab_dir, input_dir)

    sections_data = []

    for m_file in m_files:
        base_name = os.path.basename(m_file)
        name_no_ext = os.path.splitext(base_name)[0]
        print(f"\n--- Processing {base_name} ---")

        output_path = os.path.join(matlab_dir, f"{name_no_ext}_output.txt")
        output_text = ""

        if not skip_run:
            # Clean old output/plots in MATLAB_DIR for this task
            old_plots = glob.glob(os.path.join(matlab_dir, f"{name_no_ext}*.png"))
            for p in old_plots:
                try:
                    os.remove(p)
                except Exception:
                    pass
            
            if os.path.exists(output_path):
                try:
                    os.remove(output_path)
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
                with open(output_path, "w", encoding='utf-8') as f:
                    f.write(output_text)
                print("Captured console output.")
            else:
                print("No console output.")
        else:
            # Checking for existing output files in skip_run mode
            print("Skipping execution. Checking for existing output file...")
            if not os.path.exists(output_path):
                # Try finding alternative output files if matching L.Q
                m = re.match(r"(?i)LS(?:_)?(\d+)[_\-\s\.]*(\d+)", name_no_ext)
                if m:
                    l_str, q_str = m.groups()
                    l_val = int(l_str)
                    q_val = int(q_str)
                    for folder in [matlab_dir, input_dir]:
                        p = os.path.join(folder, f"{l_val}.{q_val}_output.txt")
                        if os.path.exists(p):
                            output_path = p
                            break
            
            if os.path.exists(output_path):
                with open(output_path, "r", encoding='utf-8', errors='ignore') as f:
                    output_text = f.read().strip()
                print("Found and loaded existing console output.")
            else:
                print("No existing console output found.")

        # Detect generated/manual plots & screenshots
        plots = find_screenshots(matlab_dir, input_dir, name_no_ext)
        print(f"Found {len(plots)} plot(s)/screenshot(s): {[os.path.basename(p) for p in plots]}")

        # Find task-specific inference
        task_inference = find_task_inference(name_no_ext, sections_inference, matlab_dir, input_dir)
        task_inference_escaped = latex_escape(task_inference) if task_inference else None

        sections_data.append({
            "name": name_no_ext,
            "m_file": base_name,
            "has_output": bool(output_text),
            "output_path_rel": os.path.relpath(output_path, os.getcwd()) if (output_text and os.path.exists(output_path)) else None,
            "plots": [os.path.relpath(p, os.getcwd()) for p in plots],
            "inference": task_inference_escaped
        })

    # Generate LaTeX content
    print("\nGenerating report.tex...")
    
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
            if sec['has_output']:
                tex_content.append(r"\noindent\textbf{Console Output:}")
                tex_content.append(r"\begin{verbatim}")
                output_path_to_read = sec['output_path_rel']
                with open(output_path_to_read, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    if len(lines) > 20:
                        tex_content.append("".join(lines[:20]) + "\n... [Output Truncated to Save Space] ...")
                    else:
                        tex_content.append("".join(lines))
                tex_content.append(r"\end{verbatim}")
                tex_content.append(r"\vspace{-0.2cm}")

            # Show plots/screenshots side-by-side to save space
            if sec['plots']:
                tex_content.append(r"\noindent\textbf{Plots:}")
                tex_content.append(r"\begin{figure}[H]")
                tex_content.append(r"    \centering")
                
                num_plots = len(sec['plots'])
                if num_plots == 1:
                    tex_content.append(f"    \\includegraphics[width=0.65\\textwidth]{{{sec['plots'][0]}}}")
                else:
                    for j, plot_file in enumerate(sec['plots']):
                        tex_content.append(f"    \\begin{{minipage}}[b]{{0.48\\textwidth}}")
                        tex_content.append(f"        \\centering")
                        tex_content.append(f"        \\includegraphics[width=\\textwidth]{{{plot_file}}}")
                        tex_content.append(f"    \\end{{minipage}}")
                        if j % 2 == 1 and j < num_plots - 1:
                            tex_content.append(r"    \\")
                        elif j < num_plots - 1:
                            tex_content.append(r"\hfill")
                
                tex_content.append(r"\end{figure}")
        
        # Show task-specific inference
        if sec['inference']:
            tex_content.append(r"\vspace{0.2cm}")
            tex_content.append(r"\noindent\textbf{Inference:}")
            tex_content.append(f"\n{sec['inference']}")
            tex_content.append(r"\vspace{0.2cm}")

        tex_content.append(r"\hrule")

    # Add global inference at the end if present
    if global_inference:
        global_inference_escaped = latex_escape(global_inference)
        tex_content.append(r"\vspace{0.3cm}")
        tex_content.append(r"\subsection*{Inference}")
        tex_content.append(global_inference_escaped)
        tex_content.append(r"\vspace{0.2cm}")

    tex_content.append(r"\end{document}")

    tex_path = os.path.join(output_dir, "report.tex")
    with open(tex_path, "w", encoding='utf-8') as f:
        f.write("\n".join(tex_content))
    print(f"Created {tex_path} successfully.")

    # Compile LaTeX report
    print(f"\nCompiling {tex_path} to PDF...")
    try:
        for _ in range(2):
            subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", f"-output-directory={output_dir}", tex_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
        print(f"Compiled report.pdf inside {output_dir} successfully!")
        
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
