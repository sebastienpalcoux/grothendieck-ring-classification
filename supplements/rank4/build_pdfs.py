#!/usr/bin/env python3
"""Build and check all three papers in an isolated directory, then publish PDFs.

Requires pdfLaTeX and the packages named in papers/preamble.tex. No network,
proprietary software, Python PDF library, or bibliography service is needed.
"""
from pathlib import Path
import argparse,json,re,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parent
PAPERS=ROOT/'papers'
NAMES=('finite','companion','verification_guide')
SUFFIXES=('.aux','.log','.out','.toc','.fls','.fdb_latexmk','.synctex.gz')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--keep-intermediates',action='store_true')
    args=parser.parse_args()
    engine=shutil.which('pdflatex')
    if engine is None:raise RuntimeError('pdfLaTeX is required; it was not found on PATH.')
    out=ROOT/'verification';out.mkdir(exist_ok=True);report=[]
    with tempfile.TemporaryDirectory(prefix='rank4-papers-') as temp:
        work=Path(temp)
        # Build from sources only; cross-document references are generated afresh.
        for source in PAPERS.rglob('*.tex'):
            dest=work/source.relative_to(PAPERS);dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(source,dest)
        for name in NAMES:
            for run in range(3):
                result=subprocess.run([engine,'-interaction=nonstopmode','-halt-on-error',name+'.tex'],cwd=work,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
                if result.returncode:
                    (out/f'{name}_build_failure.log').write_text(result.stdout)
                    raise RuntimeError(f'{name}: LaTeX failed; see verification/{name}_build_failure.log')
            log=(work/(name+'.log')).read_text(errors='replace')
            bad=[line for line in log.splitlines() if 'Overfull ' in line or 'Missing character:' in line or re.search(r'(undefined|multiply defined|Rerun to get|Citation .+ undefined)',line,re.I)]
            if bad:raise RuntimeError(f'{name}: unresolved layout/reference diagnostics: '+ '; '.join(bad))
            pages=re.search(r'Output written on .*?\((\d+) pages?',log,re.S)
            pdf=(work/(name+'.pdf')).read_bytes()
            if not pages or int(pages[1])==0 or not pdf.rstrip().endswith(b'%%EOF'):
                raise RuntimeError(f'{name}: incomplete PDF output')
            report.append({'document':name+'.pdf','pages':int(pages[1]),'compiled':True,'reference_and_overfull_checks':'passed','complete_pdf_trailer':True})
            print('PASS',name+'.pdf',report[-1]['pages'],'pages',flush=True)
        # Only complete PDFs enter the deliverable directory.
        for name in NAMES:
            dest=PAPERS/(name+'.pdf');staged=PAPERS/(name+'.pdf.tmp')
            shutil.copyfile(work/(name+'.pdf'),staged);staged.replace(dest)
            for suffix in SUFFIXES:
                source=work/(name+suffix);dest=PAPERS/(name+suffix)
                if args.keep_intermediates and source.exists():shutil.copyfile(source,dest)
                elif dest.exists():dest.unlink()
    (out/'pdf_build.json').write_text(json.dumps(report,indent=2)+'\n')
    return 0
if __name__=='__main__':
    try:sys.exit(main())
    except Exception as e:print('ERROR:',e,file=sys.stderr);sys.exit(1)
