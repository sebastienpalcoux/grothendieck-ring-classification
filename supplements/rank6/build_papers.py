#!/usr/bin/env python3
"""Rebuild the supplied LaTeX documents; fail on a TeX error."""
from pathlib import Path
import shutil
import subprocess
import sys
ROOT = Path(__file__).resolve().parent

def main() -> int:
    if shutil.which('pdflatex') is None:
        print('pdflatex is required to rebuild documents.', file=sys.stderr)
        return 2
    target = ROOT / 'papers'
    for name in ['manuscript', 'verification_guide']:
        for run in range(3):
            proc = subprocess.run(['pdflatex', '-interaction=nonstopmode',
                                   '-halt-on-error', f'{name}.tex'], cwd=target,
                                  text=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT)
            logdir=ROOT/'verification'/'document_build_logs'
            logdir.mkdir(parents=True,exist_ok=True)
            (logdir / f'{name}_pass{run+1}.log').write_text(proc.stdout)
            if proc.returncode:
                print(proc.stdout[-5000:], file=sys.stderr)
                return proc.returncode
        print(f'Built papers/{name}.pdf')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
