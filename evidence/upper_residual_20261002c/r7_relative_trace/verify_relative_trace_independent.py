#!/usr/bin/env python3
"""Independent gzip-source and matrix audit; no imports from census checkers."""
import gzip, hashlib, json
from pathlib import Path
import sympy as s
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'supplements/rank7/data/rank7_tables.txt.gz').exists())

def require(ok,msg):
    if not ok:raise ValueError(msg)

def main():
    packed=(ROOT/'supplements/rank7/data/rank7_tables.txt.gz').read_bytes()
    require(hashlib.sha256(packed).hexdigest()=='6ddea4c66de7fbe077e9552e71e8cf95ec3fec5bbd30a615e68e2d8fcb9ae9c9','source archive')
    rows=[json.loads(t.replace('{','[').replace('}',']')) for t in gzip.decompress(packed).decode().splitlines() if t.strip()]
    rings=[R for R in rows if max(v for A in R for b in A for v in b)==4]
    z=s.Symbol('z');q=s.sqrt(51);x,y=s.symbols('x y');f=510+70*q
    require(s.expand(f*(510-70*q))==10200,'quadratic norm')
    require(s.simplify(20*(x+y*q)/f-(x-7*y+(y-7*x/s.Integer(51))*q))==0,'ideal quotient')
    out=[]
    for ix,sha,bound,p in [(1417,'605b10a0fcc5d69475ad66de93308df1af4ee9a3e88f4d3412bbc7638830c38e',1086,(z-20)**3*(z-4)*(z-2)*(z*z-1020*z+10200)),(1420,'b8b9ab4076ea0be2f12d2f8ab92cd3c008cf370e73e68fa295180cbbe20e17b2',1070,(z-20)*(z-12)*(z-10)*(z-6)*(z-2)*(z*z-1020*z+10200))]:
        R=rings[ix-1]
        require(hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()==sha,'tensor hash')
        require([next(j for j in range(7) if R[i][j][0]) for i in range(7)]==list(range(7)),'self dual')
        Ns=[s.Matrix(A) for A in R];require(all(A==A.T for A in Ns),'symmetric matrices')
        C=s.zeros(7)
        for A in Ns:C+=A*A
        require(s.expand(C.charpoly(z).as_expr()-p)==0,'full Casimir polynomial')
        require(C.trace()==sum(v*v for A in R for b in A for v in b)==bound,'trace and sum squares')
        require(40*51>bound,'strict trace gap')
        out.append(dict(id='R7_4_'+str(ix),tensor_sha256=sha,casimir_polynomial=str(s.factor(p)),casimir_trace=bound,relative_trace_lower_bound=2040))
    print(json.dumps(dict(status='PASS',scope='independent_general_proof_audit',cases=out,source_imports='none',ledgers_changed=False),indent=2))
if __name__=='__main__':main()
