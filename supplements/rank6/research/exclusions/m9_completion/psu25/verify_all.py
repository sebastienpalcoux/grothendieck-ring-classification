#!/usr/bin/env python3
"""Replay the complete R6_9_3748 arithmetic proof under Python optimization."""
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
for name in ['verify_sphericality.py','verify_relative_center.py','verify_center_exclusion.py']:
    subprocess.run([sys.executable,'-O',str(HERE/name),'--verify'],
                   cwd=HERE,check=True,timeout=120)
print('PASS: all three R6_9_3748 certificates replayed under python -O.')
