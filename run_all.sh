#!/bin/bash
echo "Running parta1.m..."
octave --no-gui --quiet parta1.m > parta1_output.txt 2>&1
echo "Running parta2.m..."
octave --no-gui --quiet parta2.m > parta2_output.txt 2>&1
echo "Running parta3.m..."
octave --no-gui --quiet parta3.m > parta3_output.txt 2>&1
echo "Running partb1.m..."
octave --no-gui --quiet partb1.m > partb1_output.txt 2>&1
echo "Running partc1.m..."
octave --no-gui --quiet partc1.m > partc1_output.txt 2>&1
echo "Running partc2.m..."
octave --no-gui --quiet partc2.m > partc2_output.txt 2>&1
echo "All scripts finished."
