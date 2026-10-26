"""Exact positive gauge for both pseudo-PSU associator tables, and action replay.

No equivalence between an arbitrary pentagon solution and a published unitary
category is assumed. A positive diagonal fusion-space gauge proves unitarity
of these actual tables.
"""
from pathlib import Path
from itertools import product
import json,re,sys,time
import sympy as s
from sympy import QQ
from sympy.polys.matrices import DomainMatrix
from audit_liptrap import HERE,FIRST,need
PROJECT=HERE/'pseudo_source'
sys.path.insert(0,str(PROJECT/'software'))
import verify_r8_1_7_zesting as base
import verify_pseudo_psu_swap as swap

def unitary_gauge(category):
    R,receipt=base.check_base(category)
    x=s.Symbol('x');K=QQ.alg_field_from_poly(s.Poly(x**4+1,x));z=K([1,0]);D=K.one+z-z**3
    raw=(base.HERE/f'cat_4_1_2_4_{category}_0_1.jl').read_text()
    F={tuple(int(v)-1 for v in keys.split(',')):K([QQ(a.strip().replace('//','/')) for a in reversed(coeff.split(','))]) for keys,coeff in re.findall(r'\[([\d, ]+)\]\s*=>\s*QQFieldElem\[([^\]]+)\]',raw)}
    def conjugate(v):
        return sum((K(a)*z**(-i) for i,a in enumerate(reversed(v.to_list()))),K.zero)
    powers={(z-z**3)**a*D**b:(a,b) for a,b in product(range(-12,13),repeat=2)}
    channels=[(a,b,c) for a,b,c in product(range(4),repeat=3) if R[a][b][c] and a and b]
    index={v:i for i,v in enumerate(channels)};eqs=[];rhs=[];ratios=[]
    for a,b,c,d in product(range(4),repeat=4):
        left=[e for e in range(4) if R[a][b][e] and R[e][c][d]]
        right=[f for f in range(4) if R[b][c][f] and R[a][f][d]]
        if not left:continue
        M=DomainMatrix([[F[a,b,c,d,e,f] for f in right] for e in left],(len(left),len(right)),K)
        inv=M.inv().to_list()
        for i,e in enumerate(left):
            for j,f in enumerate(right):
                v=F[a,b,c,d,e,f];u=inv[j][i]
                if v==K.zero:need(u==K.zero,'inverse support at zero coefficient');continue
                ratio=u/conjugate(v)
                need(ratio in powers,'positive explicit algebraic inverse ratio '+str((category,a,b,c,d,e,f,ratio.to_list())))
                row=[0]*len(channels)
                for k,sgn in (((a,b,e),1),((e,c,d),1),((b,c,f),-1),((a,f,d),-1)):
                    if k in index:row[index[k]]+=sgn
                eqs.append(row);rhs.append(powers[ratio]);ratios.append(ratio)
    A=s.Matrix(eqs);solutions=[]
    for q in range(2):
        sol=s.linsolve((A,s.Matrix([v[q] for v in rhs])))
        need(sol is not s.EmptySet and len(sol)==1,'consistent positive diagonal gauge')
        v=list(next(iter(sol)));free=set().union(*(u.free_symbols for u in v))
        v=[u.subs({t:0 for t in free}) for u in v]
        need(A*s.Matrix(v)==s.Matrix([u[q] for u in rhs]),'exact rational exponent solution')
        solutions.append(v)
    # Each fusion-channel squared norm is 2^p*(1+sqrt2)^q>0.
    # The inverse identity F^-1=D_right^-1 F* D_left is equivalent to
    # unitarity after the positive diagonal gauge on fusion spaces.
    out=dict(category=category,status='PASS',source=receipt,unitary_inverse_ratio_equations=len(eqs),positive_gauge=[dict(channel=list(k),power_of_2=str(solutions[0][i]/2),power_of_one_plus_sqrt2=str(solutions[1][i])) for i,k in enumerate(channels)],unitary_proof='exact inverse/conjugate ratio identities with positive multiplicative fusion-channel squared norms')
    return R,out

def main():
    start=time.monotonic();bases=[unitary_gauge(a) for a in (1,2)];need(bases[0][0]==bases[1][0],'same base tensor')
    cert=json.loads((base.HERE/'r8_1_7_zesting_certificate.json').read_text());base.check_fusion(bases[0][0],cert)
    R,action=swap.check_action();records=json.loads((base.HERE/'pseudo_psu_swap_certificates.json').read_text())
    for r in records:swap.verify_record(r,R)
    lower={r['id']:r['tensor'] for r in json.loads((FIRST/'lower_rank8_models.json').read_text())}
    for r in [cert]+records:need(r['tensor']==lower[r['id']],'actual bound source used by rank12 pullbacks')
    rank4=next(r['tensor'] for r in json.loads((FIRST/'lower_rank45_models.json').read_text()) if r['name']=='pseudo-PSU(2)_6')
    # The lower-factor basis may differ; use a direct finite permutation witness.
    from itertools import permutations
    need(any(all(rank4[a][b][c]==R[p[a]][p[b]][p[c]] for a,b,c in product(range(4),repeat=3)) for q in permutations(range(1,4)) for p in [(0,)+q]),'actual rank4 product factor')
    # Receipt's rational data are normalized to strings for JSON only.
    out=dict(status='PASS',bases=[r[1] for r in bases],action=action,bound_lower_ids=[r['id'] for r in [cert]+records],seconds=time.monotonic()-start)
    (HERE/'pseudo_source_reaudit.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(dict(status='PASS',ids=out['bound_lower_ids'],seconds=out['seconds']))

if __name__=='__main__':main()
