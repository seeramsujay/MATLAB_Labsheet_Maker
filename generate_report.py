#!/usr/bin/env python3
import os
import sys
import glob
import subprocess
import re
import argparse
import unicodedata

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

def extract_task_title(matlab_dir, m_file, default_title=None):
    path = os.path.join(matlab_dir, m_file)
    if os.path.exists(path):
        try:
            lines = []
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    stripped = line.strip()
                    if not stripped:
                        if lines:
                            break  # Empty line ends the title comment block
                        continue
                    if stripped.startswith('%'):
                        content = stripped.lstrip('%').strip()
                        if content:
                            lines.append(content)
                    else:
                        break
            if lines:
                return " ".join(lines)
        except Exception:
            pass
    return default_title

def latex_escape(text):
    if not text:
        return ""
    text = unicodedata.normalize('NFKC', text)
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

def find_screenshots(dirs, name_no_ext):
    import re
    regexes = []
    
    # 1. Standard pattern based on name_no_ext
    escaped_base = re.escape(name_no_ext)
    regexes.append(re.compile(rf"^{escaped_base}(?:[._-][a-zA-Z0-9_-]+|[a-zA-Z])?\.(?:png|jpg|jpeg|PNG|JPG|JPEG)$", re.IGNORECASE))
    
    # 2. Numbered representation pattern
    m = re.match(r"(?i)LS(?:_)?(\d+)[_\-\s\.]*(\d+)", name_no_ext)
    if m:
        l_str, q_str = m.groups()
        l_val = int(l_str)
        q_val = int(q_str)
        
        q_representations = sorted(list(set([q_str, str(q_val)])))
        l_representations = sorted(list(set([l_str, str(l_val)])))
        
        for l_repr in l_representations:
            for q_repr in q_representations:
                l_esc = re.escape(l_repr)
                q_esc = re.escape(q_repr)
                regexes.append(re.compile(rf"^{l_esc}[._-]{q_esc}(?:[._-][a-zA-Z0-9_-]+|[a-zA-Z])?\.(?:png|jpg|jpeg|PNG|JPG|JPEG)$", re.IGNORECASE))

    found_files = []
    seen = set()
    for folder in dirs:
        if not os.path.exists(folder):
            continue
        for filename in os.listdir(folder):
            filepath = os.path.join(folder, filename)
            if not os.path.isfile(filepath):
                continue
            for rx in regexes:
                if rx.match(filename):
                    abs_p = os.path.abspath(filepath)
                    if abs_p not in seen:
                        seen.add(abs_p)
                        found_files.append(filepath)
                    break
                    
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
    pics_dir = env.get('PICS_DIR', 'pics')
    
    skip_run = args.skip_run or (env.get('SKIP_RUN', 'false').lower() in ('true', '1', 'yes'))

    print(f"Loading files from: {matlab_dir}")
    print(f"Pics Directory: {pics_dir}")
    print(f"Saving outputs to: {output_dir}")
    print(f"Student: {student_name} ({student_roll})")
    print(f"Skip Run: {skip_run}")

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(pics_dir, exist_ok=True)

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

        # Check pics/ first
        pics_plots = find_screenshots([pics_dir], name_no_ext)
        task_skip_run = skip_run or bool(pics_plots)

        if not task_skip_run:
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
        if pics_plots:
            plots = pics_plots
            print(f"Using screenshots from pics/: {[os.path.basename(p) for p in plots]}")
        else:
            plots = find_screenshots([matlab_dir, input_dir], name_no_ext)
            print(f"Found {len(plots)} plot(s)/screenshot(s): {[os.path.basename(p) for p in plots]}")

        # Find task-specific inference
        task_inference = find_task_inference(name_no_ext, sections_inference, matlab_dir, input_dir)
        task_inference_escaped = latex_escape(task_inference) if task_inference else None

        task_title = extract_task_title(matlab_dir, base_name, None)
        if task_title:
            task_title_escaped = latex_escape(task_title)
        else:
            task_title_escaped = f"Task: {latex_escape(name_no_ext)}"

        sections_data.append({
            "name": name_no_ext,
            "m_file": base_name,
            "title": task_title_escaped,
            "has_output": bool(output_text),
            "output_path_rel": os.path.relpath(output_path, os.getcwd()) if (output_text and os.path.exists(output_path)) else None,
            "plots": [os.path.relpath(p, output_dir) for p in plots],
            "inference": task_inference_escaped
        })

    # Generate LaTeX content
    esc_name = latex_escape(student_name)
    esc_roll = latex_escape(student_roll)

    def generate_tex_code(scale_factor, layout_style):
        # scale_factor can be a list of floats (one per section) or a single float
        if isinstance(scale_factor, (int, float)):
            scales = [scale_factor] * len(sections_data)
        else:
            scales = scale_factor

        tex_content = []
        tex_content.append(r"\documentclass[10pt]{article}")
        tex_content.append(r"\usepackage[margin=0.35in]{geometry}")
        tex_content.append(r"\usepackage{graphicx}")
        tex_content.append(r"\usepackage{listings}")
        tex_content.append(r"\usepackage{xcolor}")
        tex_content.append(r"\usepackage{float}")
        tex_content.append(r"\usepackage{microtype}")
        tex_content.append(r"\raggedbottom")
        
        tex_content.append(r"\lstset{")
        tex_content.append(r"    language=Octave,")
        tex_content.append(r"    basicstyle=\ttfamily\tiny,")  # default fallback
        tex_content.append(r"    breaklines=true,")
        tex_content.append(r"    frame=single,")
        tex_content.append(r"    commentstyle=\color{gray},")
        tex_content.append(r"    keywordstyle=\color{blue},")
        tex_content.append(r"    showstringspaces=false,")
        tex_content.append(r"    aboveskip=4pt,")
        tex_content.append(r"    belowskip=4pt")
        tex_content.append(r"}")

        tex_content.append(r"\begin{document}")
        
        tex_content.append(r"\noindent")
        tex_content.append(f"\\textbf{{Name:}} {esc_name} \\hfill \\textbf{{Roll No:}} {esc_roll}\\\\")
        tex_content.append(r"\noindent\rule{\textwidth}{0.4pt}")
        tex_content.append(r"\vspace{-0.3cm}")
        tex_content.append(r"\begin{center}")
        tex_content.append(r"    \subsection*{DSP Laboratory Report}")
        tex_content.append(r"\end{center}")
        tex_content.append(r"\vspace{-0.3cm}")

        for sec_idx, sec in enumerate(sections_data):
            sec_scale = scales[sec_idx]
            tex_content.append(f"\\subsection*{{{sec['title']}}}")
            tex_content.append(r"\vspace{-0.1cm}")
            
            # Include code with dynamic listing basicstyle font size based on scale
            tex_content.append(r"\noindent\textbf{Source Code:}")
            m_file_path = os.path.join(matlab_dir, sec['m_file'])
            rel_m_file = os.path.relpath(m_file_path, output_dir)
            sec_font_size = r"\scriptsize" if sec_scale >= 0.9 else r"\tiny"
            tex_content.append(f"\\lstinputlisting[basicstyle=\\ttfamily{sec_font_size}]{{{rel_m_file}}}")
            tex_content.append(r"\vspace{0.05cm}")

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
                    
                    if layout_style == "vertical":
                        # Stack all plots vertically
                        width = min(0.95, round(0.65 * sec_scale, 2))
                        for p_idx, plot_path in enumerate(sec['plots']):
                            tex_content.append(f"    \\includegraphics[width={width}\\textwidth]{{{{{plot_path}}}}}")
                            if p_idx + 1 < num_plots:
                                tex_content.append(r"    \\")
                                tex_content.append(r"    \vspace{0.1cm}")
                    else:
                        # Grid layout
                        single_width = min(0.95, round(0.65 * sec_scale, 2))
                        minipage_width = min(0.49, round(0.48 * sec_scale, 2))
                        if num_plots == 1:
                            tex_content.append(f"    \\includegraphics[width={single_width}\\textwidth]{{{{{sec['plots'][0]}}}}}")
                        else:
                            for idx in range(0, num_plots, 2):
                                if idx + 1 < num_plots:
                                    tex_content.append(f"    \\begin{{minipage}}[b]{{{minipage_width}\\textwidth}}")
                                    tex_content.append(r"        \centering")
                                    tex_content.append(f"        \\includegraphics[width=\\textwidth]{{{{{sec['plots'][idx]}}}}}")
                                    tex_content.append(r"    \end{minipage}")
                                    tex_content.append(r"    \hfill")
                                    tex_content.append(f"    \\begin{{minipage}}[b]{{{minipage_width}\\textwidth}}")
                                    tex_content.append(r"        \centering")
                                    tex_content.append(f"        \\includegraphics[width=\\textwidth]{{{{{sec['plots'][idx+1]}}}}}")
                                    tex_content.append(r"    \end{minipage}")
                                else:
                                    tex_content.append(f"    \\includegraphics[width={single_width}\\textwidth]{{{{{sec['plots'][idx]}}}}}")
                                
                                if idx + 2 < num_plots:
                                    tex_content.append(r"    \\")
                                    tex_content.append(r"    \vspace{0.2cm}")
                    
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
        return "\n".join(tex_content)

    def get_pdf_page_count():
        log_path = os.path.join(output_dir, "report.log")
        if os.path.exists(log_path):
            try:
                with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                    log_text = f.read()
                    m = re.search(r"Output written on .*? \((\d+) page", log_text)
                    if m:
                        return int(m.group(1))
            except Exception:
                pass
        return 1

    tex_path = os.path.join(output_dir, "report.tex")

    print("\nOptimizing document layout and page fit...")
    
    # 1. Determine baseline page count for vertical layout (at scale 0.5)
    print("Testing vertical layout baseline (scale 0.5)...")
    baseline_vertical_tex = generate_tex_code(0.5, "vertical")
    with open(tex_path, "w", encoding='utf-8') as f:
        f.write(baseline_vertical_tex)
    v_target_pages = 999
    try:
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "report.tex"], cwd=output_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        v_target_pages = get_pdf_page_count()
        print(f"Vertical baseline pages: {v_target_pages}")
    except Exception as e:
        print(f"Vertical baseline compile failed: {e}")

    # 2. Determine baseline page count for grid layout (at scale 0.5)
    print("Testing grid layout baseline (scale 0.5)...")
    baseline_grid_tex = generate_tex_code(0.5, "grid")
    with open(tex_path, "w", encoding='utf-8') as f:
        f.write(baseline_grid_tex)
    g_target_pages = 999
    try:
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "report.tex"], cwd=output_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        g_target_pages = get_pdf_page_count()
        print(f"Grid baseline pages: {g_target_pages}")
    except Exception as e:
        print(f"Grid baseline compile failed: {e}")

    # Now, run binary search for Vertical layout
    print("\nOptimizing scale for vertical layout...")
    v_low = 0.5
    v_high = 1.8
    v_opt_scale = 0.5
    
    for i in range(6):  # 6 iterations gives 0.02 precision
        mid = round((v_low + v_high) / 2, 2)
        print(f"Testing vertical scale {mid}...", end="", flush=True)
        tex_code = generate_tex_code(mid, "vertical")
        with open(tex_path, "w", encoding='utf-8') as f:
            f.write(tex_code)
        try:
            subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "report.tex"],
                cwd=output_dir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
            pages = get_pdf_page_count()
            print(f" resulting page count: {pages}")
            if pages <= v_target_pages:
                v_opt_scale = mid
                v_low = mid + 0.05
            else:
                v_high = mid - 0.05
        except Exception:
            v_high = mid - 0.05
    print(f"Vertical optimal: scale {v_opt_scale}, pages {v_target_pages}")

    # Run binary search for Grid layout
    print("\nOptimizing scale for grid layout...")
    g_low = 0.5
    g_high = 1.8
    g_opt_scale = 0.5
    
    for i in range(6):
        mid = round((g_low + g_high) / 2, 2)
        print(f"Testing grid scale {mid}...", end="", flush=True)
        tex_code = generate_tex_code(mid, "grid")
        with open(tex_path, "w", encoding='utf-8') as f:
            f.write(tex_code)
        try:
            subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "report.tex"],
                cwd=output_dir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
            pages = get_pdf_page_count()
            print(f" resulting page count: {pages}")
            if pages <= g_target_pages:
                g_opt_scale = mid
                g_low = mid + 0.05
            else:
                g_high = mid - 0.05
        except Exception:
            g_high = mid - 0.05
    print(f"Grid optimal: scale {g_opt_scale}, pages {g_target_pages}")

    # Now make the final selection
    v_metric = 0.65 * v_opt_scale
    g_metric = 0.48 * g_opt_scale

    if v_target_pages < g_target_pages:
        selected_layout = "vertical"
        optimal_scale = v_opt_scale
        print(f"Selected Vertical layout: page count {v_target_pages} is lower than Grid page count {g_target_pages}.")
    elif g_target_pages < v_target_pages:
        selected_layout = "grid"
        optimal_scale = g_opt_scale
        print(f"Selected Grid layout: page count {g_target_pages} is lower than Vertical page count {v_target_pages}.")
    else:
        # Page counts are equal, compare image metrics to maximize screen coverage
        if v_metric >= g_metric:
            selected_layout = "vertical"
            optimal_scale = v_opt_scale
            print(f"Selected Vertical layout: both take {v_target_pages} pages, but Vertical offers larger average plot width ({round(v_metric, 2)} vs {round(g_metric, 2)}).")
        else:
            selected_layout = "grid"
            optimal_scale = g_opt_scale
            print(f"Selected Grid layout: both take {g_target_pages} pages, but Grid offers larger average plot width ({round(g_metric, 2)} vs {round(v_metric, 2)}).")

    target_pages = v_target_pages if selected_layout == "vertical" else g_target_pages
    section_scales = [optimal_scale] * len(sections_data)
    
    print(f"\nRefining section scales individually (Page-Fill Optimization) for target count of {target_pages} pages...")
    for idx in range(len(sections_data)):
        print(f"Optimizing Section {idx+1} ({sections_data[idx]['m_file']})...", end="", flush=True)
        # Binary search the optimal scale for this specific section in the range [optimal_scale, 1.8]
        low_s = optimal_scale
        high_s = 1.8
        best_s = optimal_scale
        
        for step in range(5):  # 5 steps gives 0.04 precision, fast enough
            mid_s = round((low_s + high_s) / 2, 2)
            # Create a copy and update the scale for this section
            test_scales = list(section_scales)
            test_scales[idx] = mid_s
            
            tex_code = generate_tex_code(test_scales, selected_layout)
            with open(tex_path, "w", encoding='utf-8') as f:
                f.write(tex_code)
                
            try:
                subprocess.run(
                    ["pdflatex", "-interaction=nonstopmode", "report.tex"],
                    cwd=output_dir,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=True
                )
                pages = get_pdf_page_count()
                if pages <= target_pages:
                    best_s = mid_s
                    low_s = mid_s + 0.04
                else:
                    high_s = mid_s - 0.04
            except Exception:
                high_s = mid_s - 0.04
        
        # Save the best scale found for this section
        section_scales[idx] = best_s
        print(f" optimal scale: {best_s}")
    
    print(f"Final refined section scales: {section_scales}")
    
    # Generate final optimized LaTeX content
    optimal_tex = generate_tex_code(section_scales, selected_layout)
    with open(tex_path, "w", encoding='utf-8') as f:
        f.write(optimal_tex)

    print("\nCompiling final optimized PDF report...")
    try:
        for _ in range(2):
            subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "report.tex"],
                cwd=output_dir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
        print(f"Compiled report.pdf inside {output_dir} successfully!")
        
        # Clean up LaTeX temp files
        for ext in ["aux", "log", "out"]:
            for f in glob.glob(os.path.join(output_dir, f"report.{ext}")):
                try:
                    os.remove(f)
                except Exception:
                    pass
    except Exception as e:
        print(f"Error compiling final LaTeX report: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
