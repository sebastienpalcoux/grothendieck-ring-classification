#!/usr/bin/env python3
"""Build the manuscript and verification guide from current TeX sources."""
from pathlib import Path
import shutil,subprocess,tempfile
P=Path(__file__).resolve().parent

def main():
    logs=P/'verification/typesetting';logs.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        td=Path(td)
        for source in (P/'papers').glob('*.tex'):shutil.copy2(source,td/source.name)
        for name in ('manuscript','verification_guide'):
            for i in range(3):
                p=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error',name+'.tex'],cwd=td,text=True,capture_output=True)
                (logs/(name+f'_pass{i+1}.txt')).write_text(p.stdout+p.stderr)
                if p.returncode:raise RuntimeError(f'{name} failed; see {logs}')
            shutil.copy2(td/(name+'.pdf'),P/'papers'/(name+'.pdf'))
            shutil.copy2(td/(name+'.log'),logs/(name+'.log'))
            text=(td/(name+'.log')).read_text()
            if any(q in text for q in ['There were undefined references','There were undefined citations']):raise RuntimeError(f'unresolved references in {name}')
            print('BUILT',name,flush=True)
if __name__=='__main__':main()
