"""Unit tests for MATLAB Labsheet Maker report generation utilities."""

import os
import tempfile
import unittest
from generate_report import (
    natural_key,
    latex_escape,
    extract_task_title,
    parse_inference_file,
)


class TestReportGenerator(unittest.TestCase):
    def test_natural_key_numeric_ordering(self):
        filenames = ["task10.m", "task1.m", "task2.m", "task20.m", "task3.m"]
        sorted_files = sorted(filenames, key=natural_key)
        self.assertEqual(sorted_files, ["task1.m", "task2.m", "task3.m", "task10.m", "task20.m"])

    def test_latex_escape(self):
        raw = "Cost is $100 & 50% of #items _value_ {test} \\path^2 ~approx"
        escaped = latex_escape(raw)
        self.assertIn(r"\$100", escaped)
        self.assertIn(r"\&", escaped)
        self.assertIn(r"\%", escaped)
        self.assertIn(r"\#items", escaped)
        self.assertIn(r"\_value\_", escaped)
        self.assertIn(r"\{test\}", escaped)
        self.assertIn(r"\textbackslash{}", escaped)
        self.assertIn(r"\textasciicircum{}", escaped)
        self.assertIn(r"\textasciitilde{}", escaped)

    def test_latex_escape_empty(self):
        self.assertEqual(latex_escape(""), "")
        self.assertEqual(latex_escape(None), "")

    def test_extract_task_title(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            m_path = os.path.join(tmpdir, "task1.m")
            with open(m_path, "w", encoding="utf-8") as f:
                f.write("% Task 1: Frequency Response Analysis\n% Secondary Line\n\nx = 1:10;\n")

            title = extract_task_title(tmpdir, "task1.m")
            self.assertEqual(title, "Task 1: Frequency Response Analysis Secondary Line")

    def test_extract_task_title_fallback(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            title = extract_task_title(tmpdir, "nonexistent.m", default_title="Default Task")
            self.assertEqual(title, "Default Task")

    def test_parse_inference_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            inf_path = os.path.join(tmpdir, "inference.txt")
            with open(inf_path, "w", encoding="utf-8") as f:
                f.write("Global notes about experiments.\n\n")
                f.write("[task1]\n")
                f.write("Task 1 output demonstrates stable damping.\n\n")
                f.write("Task 2:\n")
                f.write("Task 2 indicates resonance at 50Hz.\n")

            sections, global_text = parse_inference_file(inf_path)
            self.assertIn("task1", sections)
            self.assertIn("2", sections)
            self.assertIn("stable damping", sections["task1"])
            self.assertIn("resonance at 50Hz", sections["2"])
            self.assertIn("Global notes", global_text)


if __name__ == "__main__":
    unittest.main()
