#!/usr/bin/env python3
"""Exact cyclotomic checks of the forced R1768 nineteen-dimensional block."""
from pathlib import Path
import argparse, hashlib, itertools, json
import sympy as s

P=37
def need(ok,why):
    if not ok:raise ValueError(why)
def zero():return [0]*P
def add(*xs):return [sum(t) for t in zip(*xs)]
def scale(x,a):return [a*t for t in x]
def mon(k,a=1):
    x=zero();x[k%P]=a;return x
def mul(x,y):
    z=zero()
    for i,a in enumerate(x):
        if a:
            for j,b in enumerate(y):
                if b:z[(i+j)%P]+=a*b
    return z
def equal(x,y):
    d=[a-b for a,b in zip(x,y)]
    return len(set(d))==1 # quotient by Phi_37 = 1+...+X^36
def chi(x):
    if x%P==0:return 0
    return 1 if pow(x%P,(P-1)//2,P)==1 else -1

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    tau=[chi(i) for i in range(P)]
    need(equal(mul(tau,tau),mon(0,P)),'Quadratic Gauss norm')
    params=list(range(1,19));labels=[2*a*a%P for a in params]
    need(len(set(labels))==18 and all(chi(k)==-1 for k in labels),'Nonsquare labels')
    B=[[add(mon(4*a*b,-1),mon(-4*a*b,-1)) for b in params] for a in params]
    for i,k in enumerate(labels):
        need(equal(add(*B[i]),mon(0)),'Mixed unit/primitive S-square entry')
        for j,l in enumerate(labels):
            salie=zero()
            for u in range(1,P):salie[(k*u+l*pow(u,-1,P))%P]+=chi(u)
            need(equal(salie,mul(tau,B[i][j])),'Exact Salie sum')
            rowdot=add(mon(0,2),*(mul(B[i][m],B[m][j]) for m in range(18)))
            need(equal(rowdot,mon(0,P*int(i==j))),'Primitive block S-square entry')
    counts={3:0,4:0}
    # Direct cyclotomic multiplication on one representative of each
    # unordered triple is sufficient because the expression is symmetric.
    tested=0
    for i,j,k in itertools.combinations_with_replacement(range(18),3):
        a,b,c=params[i],params[j],params[k]
        eps=sum(x%P==0 for x in [a+b+c,a+b-c,a-b+c,-a+b+c])
        need(eps in (0,1),'More than one additive relation')
        actual=zero()
        for m in range(18):actual=add(actual,mul(mul(B[i][m],B[j][m]),B[k][m]))
        need(equal(actual,mon(0,4-P*eps)),'Primitive Verlinde cubic sum')
        multiplicity=1 if i==k else 3 if i==j or j==k else 6
        counts[4-eps]+=multiplicity;tested+=1
    need(sum(counts.values())==18**3,'Incomplete ordered triple count')
    root=s.sqrt(P);D=444+72*root;alpha=73+12*root;q=37+6*root
    need(s.simplify(q*(1+1/alpha)-74)==0,'Rational target coefficient')
    need(s.simplify(alpha+1/alpha+2-4*P)==0,'Alpha target coefficient')
    need(s.simplify(D*(1-1/alpha)/root-144)==0,'Primitive orbit contribution')
    proof=Path(__file__).with_name('R1768_WEIL_BLOCK.md')
    report={'status':'PASS','scope':'Necessary nineteen-dimensional block; no branch exclusion.',
            'prime':P,'cyclic_rank':19,'nonsquare_twist_exponents':labels,
            'exact_Salie_checks':18**2,'exact_primitive_S_square_entries':18**2,
            'unordered_exact_cubic_checks':tested,
            'ordered_primitive_coefficients':counts,
            'rational_target_coefficient':'2t','alpha_target_coefficient':'4-delta_kl',
            'proof_sha256':hashlib.sha256(proof.read_bytes()).hexdigest(),
            'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    text=json.dumps(report,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    print(text,end='')

if __name__=='__main__':main()
