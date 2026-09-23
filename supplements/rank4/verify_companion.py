#!/usr/bin/env python3
"""Check the finite algebraic certificates used in the companion paper.

These checks do not replace the companion's proofs of the uniform bounds.
The complete finite-classification verifier is verify.py.
"""
from pathlib import Path
import subprocess,sys,json
ROOT=Path(__file__).resolve().parent
if sys.flags.optimize:raise SystemExit('Run without -O: the companion source checks use assertions.')
logs=ROOT/'verification';logs.mkdir(exist_ok=True);report=[]
for name in ['verify_unbounded_fibonacci.py','verify_unbounded_quadratic_branch.py']:
    p=subprocess.run([sys.executable,str(ROOT/'companion_software'/name)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,cwd=ROOT)
    (logs/(name.removesuffix('.py')+'.log')).write_text(p.stdout)
    if p.returncode:raise SystemExit(p.stdout)
    print('PASS',name);report.append({'script':name,'passed':True})
(logs/'companion.json').write_text(json.dumps(report,indent=2)+'\n')
