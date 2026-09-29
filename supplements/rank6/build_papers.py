#!/usr/bin/env python3
"""Rebuild the supplied LaTeX documents; fail on a TeX error."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
ROOT = Path(__file__).resolve().parent

def main() -> int:
    if shutil.which('pdflatex') is None:
        print('pdflatex is required to rebuild documents.', file=sys.stderr)
        return 2
    target = ROOT / 'papers'
    # Publish only complete PDFs, after every TeX pass has finished.
    # Interrupted compilation must not truncate the last usable artifact.
    with tempfile.TemporaryDirectory(prefix='rank6_papers_') as tmp:
        build = Path(tmp) / 'papers'
        shutil.copytree(target, build, ignore=shutil.ignore_patterns(
            '*.pdf', '*.aux', '*.out', '*.toc', '*.log'))
        for name in ['manuscript', 'verification_guide']:
            for run in range(3):
                proc = subprocess.run(['pdflatex', '-interaction=nonstopmode',
                                       '-halt-on-error', f'{name}.tex'], cwd=build,
                                      text=True, stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT)
                logdir=ROOT/'verification'/'document_build_logs'
                logdir.mkdir(parents=True,exist_ok=True)
                (logdir / f'{name}_pass{run+1}.log').write_text(proc.stdout)
                if proc.returncode:
                    print(proc.stdout[-5000:], file=sys.stderr)
                    return proc.returncode
            content = (build / f'{name}.pdf').read_bytes()
            if not content.startswith(b'%PDF-') or b'%%EOF' not in content[-1024:]:
                raise RuntimeError(f'Incomplete PDF: {name}')
            output = target / f'{name}.pdf.new'
            output.write_bytes(content)
            output.replace(target / f'{name}.pdf')
            print(f'Built papers/{name}.pdf ({len(content)} bytes)', flush=True)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
