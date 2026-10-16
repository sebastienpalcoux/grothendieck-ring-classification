#!/usr/bin/env python3
"""Replay the independent rank-four algebra checks and verify their manifest."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
MANIFEST=ROOT/'MANIFEST.json'
CHECKS=[
    ('structural_algebra.py','structural_algebra.json',False,False),
    ('check_quadratic.py','quadratic_receipt.json',False,True),
    ('check_quadratic_inequalities.py','quadratic_inequalities_receipt.json',False,True),
    ('cubic_pivotal_checks.py','cubic_pivotal_checks.json',True,False),
    ('independent_quartic_chart.py','independent_quartic_chart.json',True,False),
    ('independent_quartic_identities.py','independent_quartic_identities.json',True,False),
]
INPUTS=[
    'manuscripts/rank4/papers/companion_sections/09_cubic.tex',
    'manuscripts/rank4/papers/companion_sections/10_pivotal_bound.tex',
    'supplements/rank4/unrestricted/audit/quartic_trace13_exact_resolvent_chart.json',
]


def require(condition,message):
    if not condition:raise RuntimeError(message)


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def semantic(value):
    if isinstance(value,dict):return {k:semantic(v) for k,v in value.items() if k!='elapsed_seconds'}
    if isinstance(value,list):return [semantic(v) for v in value]
    return value


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository-root',type=Path,default=ROOT.parents[1])
    parser.add_argument('--write-manifest',action='store_true',help='maintainer: bind a successfully replayed set')
    args=parser.parse_args();repo=args.repository_root.resolve()
    sources={p.name:sha(p) for p in sorted(ROOT.iterdir()) if p.suffix in ('.py','.md')}
    inputs={name:sha(repo/name) for name in INPUTS}
    if not args.write_manifest:
        old=json.loads(MANIFEST.read_text())
        require(old['sources']==sources,'independent-check source or audit differs from manifest')
        require(old['canonical_inputs']==inputs,'canonical manuscript/chart differs from manifest')
    receipts={}
    for script,output,needs_root,stdout_json in CHECKS:
        command=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(ROOT/script)]
        if needs_root:command+=['--repository-root',str(repo)]
        completed=subprocess.run(command,cwd=ROOT,text=True,capture_output=True)
        require(completed.returncode==0,script+' failed:\n'+completed.stdout+completed.stderr)
        if stdout_json:(ROOT/output).write_text(json.dumps(json.loads(completed.stdout),indent=2)+'\n')
        report=json.loads((ROOT/output).read_text())
        require(report['status']=='PASS',script+' receipt is not PASS')
        data=json.dumps(semantic(report),sort_keys=True,separators=(',',':')).encode()
        receipts[output]=hashlib.sha256(data).hexdigest()
        print('PASS:',script,flush=True)
    if args.write_manifest:
        MANIFEST.write_text(json.dumps({'schema':1,'sources':sources,'canonical_inputs':inputs,
            'receipt_semantic_sha256':receipts,'scope':'Independent exact algebra and finite charts supporting five AI mathematical audits; no categorical proof formalization or independent human verification.'},indent=2)+'\n')
    else:require(old['receipt_semantic_sha256']==receipts,'independent arithmetic result differs from manifest')
    print('PASS: six independent rank-four checkers and canonical source bindings.')


if __name__=='__main__':main()
