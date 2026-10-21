"""Exact rational LP-dual certificates force every dual coefficient <=3.

Discovery uses scipy, but verification consists solely of rational arithmetic.
Run --discover once to save certificates; otherwise independently reconstruct
the complete necessary equation system and check every saved inequality.
"""
from pathlib import Path
from fractions import Fraction
import hashlib,json,sys
import sympy as s
from r721_dual_fusion import prepare,need
HERE=Path(__file__).resolve().parent
PATH=HERE/'r721_dual_multiplicity_bound.json'

def certificate(rec):
    import numpy as np
    from scipy.optimize import linprog
    R=s.Matrix([[s.Rational(t)for t in row]for row in rec['rref']])
    A=R[:,:-1];b=R[:,-1];m,n=A.shape
    aa=np.array(A,dtype=float);bb=np.array(b,dtype=float).reshape(-1)
    certs=[]
    for j in range(n):
        obj=np.zeros(n);obj[j]=-1
        ans=linprog(obj,A_eq=aa,b_eq=bb,bounds=(0,None),method='highs')
        need(ans.success,'LP proposal')
        y=[s.Rational(Fraction(-float(t)).limit_denominator(100000))for t in ans.eqlin.marginals]
        need(all(sum(y[i]*A[i,k]for i in range(m))>=int(k==j)for k in range(n)),'exact nonnegative coefficient domination')
        rhs=sum(y[i]*b[i]for i in range(m));need(rhs<=3,'exact multiplicity bound')
        certs.append(dict(variable=j,upper_bound=str(rhs),covector=[[i,str(t)]for i,t in enumerate(y)if t]))
    return dict(dual_a=rec['dual_a'],dual_b=rec['dual_b'],certificates=certs,
                rref_sha256=hashlib.sha256(json.dumps(rec['rref'],separators=(',',':')).encode()).hexdigest())

def verify(rec,proof):
    R=s.Matrix([[s.Rational(t)for t in row]for row in rec['rref']]);A=R[:,:-1];b=R[:,-1];m,n=A.shape
    need(proof['rref_sha256']==hashlib.sha256(json.dumps(rec['rref'],separators=(',',':')).encode()).hexdigest(),'reconstructed exact equation identity')
    need([z['variable']for z in proof['certificates']]==list(range(n)),'all coefficient orbits covered')
    for cert in proof['certificates']:
        y=[s.Rational(0)]*m
        for i,t in cert['covector']:y[i]=s.Rational(t)
        need(all(sum(y[i]*A[i,k]for i in range(m))>=int(k==cert['variable'])for k in range(n)),'exact covector domination')
        rhs=sum(y[i]*b[i]for i in range(m));need(rhs==s.Rational(cert['upper_bound'])and rhs<=3,'exact RHS bound')
    return dict(dual_a=rec['dual_a'],dual_b=rec['dual_b'],coefficient_orbits=n,
                fusion_coefficients_covered=sum(len(o)for o in rec['orbits']),maximum_upper_bound=3,passed=True)

def main():
    records=[prepare(da,db)for da in(0,1)for db in(0,1)]
    if '--discover' in sys.argv:
        proof=[certificate(r)for r in records]
        PATH.write_text(json.dumps(proof,indent=2)+'\n')
    else:proof=json.loads(PATH.read_text())
    result=[]
    for rec,pr in zip(records,proof):
        need((rec['dual_a'],rec['dual_b'])==(pr['dual_a'],pr['dual_b']),'duality case coverage')
        result.append(verify(rec,pr))
    need(len(proof)==4,'all four dualities')
    receipt=dict(scope='Every nonnegative fusion tensor of the mandatory rank8 dual, with its exact induction columns and dimensions, has maximum coefficient at most3.',
       cases=result,files={p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in [Path(__file__),HERE/'r721_dual_fusion.py',PATH]})
    (HERE/'r721_dual_multiplicity_verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()
