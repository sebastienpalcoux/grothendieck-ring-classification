#!/usr/bin/env python3
"""Source-bound exact arithmetic for the general relative-trace obstruction.

Categorical hypotheses and argument are in RELATIVE_TRACE_PROOF.md.
This does not promote incomplete signed searches or scoped pivotal evidence.
"""
import argparse,hashlib,json,math,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=next(p for p in HERE.parents if (p/'supplements/rank7/data/rank7_tables.txt.gz').exists())
sys.path.insert(0,str(ROOT/'evidence/upper_residual_20261002b/r7_nonintegral'))
from case_source import read_cases,SOFTWARE
sys.path.insert(0,str(SOFTWARE))
from rings import Characters,dual
from exact import pc
import sympy as s

def require(x,msg):
    if not x:raise ValueError(msg)

IDS={'R7_4_1417':('605b10a0fcc5d69475ad66de93308df1af4ee9a3e88f4d3412bbc7638830c38e',1086),
     'R7_4_1420':('b8b9ab4076ea0be2f12d2f8ab92cd3c008cf370e73e68fa295180cbbe20e17b2',1070)}

def verify():
    out=[];cases=read_cases(IDS)
    q=s.sqrt(51);x,y=s.symbols('x y');f=510+70*q
    z=s.symbols('z')
    require(s.minpoly(f,z)==z**2-1020*z+10200,'quadratic codegree identity')
    require(51%4==3 and s.factorint(51)=={3:1,17:1},'integer ring Z[sqrt51]')
    quotient=(x-7*y)+(y-s.Rational(7,51)*x)*q
    require(s.simplify(quotient*f-20*(x+y*q))==0,'relative-trace lattice identity')
    require(math.gcd(7,51)==1,'integrality forces51 divisibility')
    lower=40*51
    for id,(sha,bound) in IDS.items():
        c=cases[id];R=c['tensor'];a=Characters(R)
        require(c['tensor_sha256']==sha,'source tensor hash')
        require(dual(R)==list(range(7)),'all basis objects self-dual')
        require(all(R[i][j]==R[j][i]for i in range(7)for j in range(7)),'commutative source tensor')
        require(any(pc(p)==['1','-20']for p,m in a.cf),'integer formal codegree20')
        require(any(pc(p)==['1','-1020','10200']for p,m in a.cf),'quadratic formal codegree')
        squares=sum(v*v for M in R for row in M for v in row)
        require(squares==int(a.C.trace())==bound,'exact Casimir trace identity')
        require(lower>bound,'strict obstruction gap')
        out.append({'id':id,'scope':'general_complex','source_line':c['source_line'],'tensor_sha256':sha,
                    'formal_codegree':20,'quadratic_formal_codegree':['1','-1020','10200'],
                    'casimir_trace_bound':bound,'relative_trace_lower_bound':lower,'strict_gap':lower-bound})
    return {'status':'PASS','optimization_safe':True,'criterion':'relative_trace_lattice','cases':out,
            'proof_sha256':hashlib.sha256((HERE/'RELATIVE_TRACE_PROOF.md').read_bytes()).hexdigest(),
            'signed_enumeration_required':False,'ledgers_changed':False}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);args=p.parse_args();r=verify();text=json.dumps(r,indent=2)
    if args.output:args.output.write_text(text+'\n')
    print(text)
