#!/usr/bin/env python3
"""Independent direct-index and Smith-form audit of the R982 lattice step."""
from pathlib import Path
import hashlib,json,itertools,argparse
import sympy as s
from sympy.matrices.normalforms import smith_normal_form

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]

def need(ok,why):
    if not ok:raise ValueError(why)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);a=parser.parse_args()
    prior=ROOT/'evidence/rank8_research_20261022/r982/module_types.json'
    data=json.loads(prior.read_text());rows=[]
    for typ in data['based_module_types']:
        M=typ['actions']
        # Check the two different index contractions directly, without the
        # producer's 64x64 reshuffling construction.
        for i,j,k,l in itertools.product(range(8),repeat=4):
            left=sum(m[i][j]*m[k][l] for m in M)
            right=sum(m[i][k]*m[j][l] for m in M)
            need(left==right,'Reshuffled bimodule Gram equality')
        U=s.Matrix([[m[i][j] for m in M] for i in range(8) for j in range(8)])
        smith=smith_normal_form(U.T,domain=s.ZZ)
        diagonal=[abs(int(smith[i,i])) for i in range(8)]
        expected=[1]*8 if typ['class']==0 else [1]*7+[2]
        need(diagonal==expected,'Wrong independent Smith invariant factors')
        if typ['class']:
            need(all(sum(row)%2==0 for row in U.tolist()),'Not contained in D8')
        need(all(all(v>=0 for v in m) and any(v>0 for v in m) for m in U.T.tolist()),
             'A source action column has negative entries or is zero')
        rows.append({'class':typ['class'],'Gram_entries_checked':4096,
                     'Smith_invariant_factors':diagonal,
                     'row_lattice':'Z8' if typ['class']==0 else 'D8'})
    proof=HERE/'R982_MORITA_REVIEW.md'
    report={'status':'PASS','scope':'Independent arithmetic and mathematical review; no category existence claim.',
            'input_sha256':hashlib.sha256(prior.read_bytes()).hexdigest(),
            'module_classes':rows,'review_sha256':hashlib.sha256(proof.read_bytes()).hexdigest()}
    text=json.dumps(report,indent=2)+'\n'
    if a.output:a.output.write_text(text)
    print(text,end='')

if __name__=='__main__':main()
