"""Exact consequence of the stabilizer algebra of X, applied to X tensor X*."""
from pathlib import Path
import json, math, time
import sympy as s

HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]/'rank12-m1-offline-20261025'
t=s.Symbol('t')

def require(v,message):
    if not v:raise ValueError(message)

def perron_factor(R,z):
    p=s.Matrix(R[z]).charpoly(t).as_poly()
    lo,hi=p.intervals(eps=s.Rational(1,10**15))[-1][0]
    for f,m in p.factor_list()[1]:
        if (lo==hi and f.eval(lo)==0)or(lo<hi and f.count_roots(lo,hi)==1):return f
    raise ValueError('Perron factor missing')

def scan(R):
    n=len(R);du=[next(j for j in range(n)if R[i][j][0])for i in range(n)]
    G=[i for i in range(n)if sum(R[i][du[i]])==1]
    unit=lambda x:[int(i==x)for i in range(n)]
    cache={};out=[]
    for x in range(n):
        for z,m in enumerate(R[x][du[x]]):
            if not m:continue
            H=[g for g in G if R[g][x]==unit(x)and R[g][z]==R[z][g]==unit(z)]
            h=len(H)
            if h<=1:continue
            require(0 in H and all(R[g][k].index(1)in H for g in H for k in H),'subgroup')
            if z not in cache:cache[z]=perron_factor(R,z)
            f=cache[z];q=h//math.gcd(h,m)
            normalized=s.Poly(f.as_expr().subs(t,q*t)/q**f.degree(),t)
            if any(a.q!=1 for a in normalized.all_coeffs()):
                out.append(dict(kind='stabilizer_square_isotypic_integrality',X=x,Xdual=du[x],Z=z,
                                multiplicity=m,H=H,stabilizer_order=h,
                                dimension_polynomial=list(map(str,f.all_coeffs())),
                                normalized_dimension_polynomial=list(map(str,normalized.all_coeffs())),
                                scope='general_complex_fusion_category'))
    return out

if __name__=='__main__':
    start=time.monotonic();data=json.loads((BASE/'tensors.json').read_text())
    old={r['id']:r['status']for r in json.loads((BASE/'ledger.json').read_text())['records']}
    rows=[]
    for rid,R in data.items():
        cs=scan(R)
        if cs:rows.append(dict(id=rid,first_round_status=old[rid],certificates=cs))
    out=dict(records=rows,elapsed_seconds=time.monotonic()-start)
    (HERE/'stabilizer_square.json').write_text(json.dumps(out,indent=2)+'\n')
    from collections import Counter
    print(Counter(r['first_round_status']for r in rows))
    print('NEW',[(r['id'],len(r['certificates']))for r in rows if r['first_round_status']!='excluded'])
