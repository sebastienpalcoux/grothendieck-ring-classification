"""Fresh rational-interval audit of every first-round center field/order gate.

Uses polynomial quotients only; no floating-point positivity or first-round
number-field/Hermite-normal-form implementation is imported.
"""
from pathlib import Path
import itertools,json,math
import sympy as S
HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]/'prior_round'
FIRST=BASE/'prior_round/evidence/rank12-m1-offline-20261025'
t=S.Symbol('t')
def need(x,m):
    if not x:raise ValueError(m)
def poly(v):return S.Poly.from_list(list(map(S.Rational,v)),t)
data=json.loads((FIRST/'tensors.json').read_text())
def casimir(R):
    n=len(R);du=[next(j for j in range(n) if R[i][j][0]) for i in range(n)]
    c=[sum(R[i][du[i]][k] for i in range(n)) for k in range(n)]
    return S.Matrix(n,n,lambda i,j:sum(c[k]*R[k][i][j] for k in range(n))).charpoly(t).as_poly()
out=[]
for r in json.loads((FIRST/'field_checks.json').read_text())['records']:
    if not r['certificates']:continue
    R=data[r['id']];n=len(R);f=poly(r['field_polynomial'])
    need(f.degree()==2 and f.is_irreducible and f.LC()==1,'quadratic field')
    intervals=f.intervals(eps=S.Rational(1,10**8));need(len(intervals)==2,'two real embeddings')
    lo,hi=intervals[-1][0]
    ds=[poly(v).rem(f) for v in r['dimensions_in_field']]
    need(ds[0]==poly([1]) and len(set(p.as_expr() for p in ds))==2,'two distinct dimensions')
    for p in ds:
        need(p.degree()<=1 and min(p.eval(lo),p.eval(hi))>0,'exact positive character using rational bounds')
    for i,j in itertools.product(range(n),repeat=2):
        need((ds[i]*ds[j]-sum((R[i][j][k]*ds[k] for k in range(n)),poly([0]))).rem(f).is_zero,'exact dimension product')
    D=sum((p*p for p in ds),poly([0])).rem(f)
    for c in r['certificates']:
        need(c['gate']=='two_FP_values_Galois_PU','published two-value gate')
        q=poly(c['casimir_factor']);need(q.is_irreducible and q.LC()==1 and casimir(R).rem(q).is_zero,'actual Casimir factor')
        entry={'id':r['id'],'kind':c['kind'],'exact_root_interval':[str(lo),str(hi)],'two_positive_FP_values':True}
        if c['kind']=='central_dimension_field':
            need(q.degree()==2,'quadratic comparison')
            ratio=S.Rational(S.discriminant(q),S.discriminant(f));num=int(ratio.p);den=int(ratio.q)
            need(ratio>0 and (math.isqrt(num)**2!=num or math.isqrt(den)**2!=den),'quadratic fields differ')
            entry['discriminant_ratio']=str(ratio)
        else:
            need(c['kind']=='central_dimension_order' and q.degree()==1,'dimension-order route')
            need(all(R[i][j]==R[j][i] for i,j in itertools.product(range(n),repeat=2)),'all irreducibles one dimensional')
            d=next(p for p in ds if p!=poly([1]));beta=D.mul_ground(1/(-q.TC()))
            vec=lambda p:S.Matrix([p.nth(0),p.nth(1)])
            coordinates=S.Matrix.hstack(vec(poly([1])),vec(d)).inv()*vec(beta)
            need(any(v.q!=1 for v in coordinates),'central dimension outside Z+Z*d')
            entry['dimension_order_coordinates']=list(map(str,coordinates))
        out.append(entry)
need(len(out)==12,'all twelve accepted center routes')
monic_count=0
for r in json.loads((FIRST/'arithmetic.json').read_text()):
    for c in r['certificates']:
        key='factor' if c['kind']=='casimir_dnumber' else 'failed_factor' if c['kind'] in ('integral_drinfeld','noncomm_integral_drinfeld') else None
        if key:
            p=poly(c[key]);need(p.LC()==1 and all(a.q==1 for a in p.all_coeffs()),'stored minimal factor genuinely monic integral')
            monic_count+=1
report={'status':'PASS','field_order_records':out,'monic_integral_Casimir_factors_checked':monic_count,'floating_point_used':False}
(HERE/'exact_field_gates.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS twelve exact positive field/order gates;',monic_count,'monic integral Casimir factors')
