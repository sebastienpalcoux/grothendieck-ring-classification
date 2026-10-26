"""Consolidate all 24 inherited exclusions with fresh source/embedding replay.

Calls reviewed independent Laurent and signed-table implementations, and
uses fresh exact polynomial-quotient arithmetic for the two rank-six gates.
No old artifact is modified and all checks survive python -O.
"""
from pathlib import Path
import sys,json,hashlib,itertools,math
sys.dont_write_bytecode=True
import sympy as s
HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]/'prior_round'
FIRST=BASE/'prior_round/evidence/rank12-m1-offline-20261025'
AUDIT=BASE/'prior_round/evidence/rank12-m1-round2-20261025/audit_exclusions'
sys.path.insert(0,str(AUDIT))
import independent_audit as a
from audit_all_exclusions import rank8_spherical
from liptrap_independent import check as liptrap
t=s.Symbol('t')
def need(x,m):
    if not x:raise ValueError(m)
def read(p):return json.loads(p.read_text())
def sha(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
def poly(v):return s.Poly.from_list(list(map(s.Rational,v)),t)
subs=read(FIRST/'subrings.json');data=read(FIRST/'tensors.json')
proofs={};source_receipts=[]
for r in read(FIRST/'lower_known.json')['class_proofs']:
    j=r['class_index'];R=subs['classes'][j]['tensor'];c=r['certificate'];kind=c['kind'];n=len(R)
    need(sha(R)==subs['classes'][j]['tensor_sha256'],'lower source tensor digest')
    if kind=='liptrap_complex_obstruction':details=liptrap(R,c)
    elif kind.startswith('central_dimension'):
        du=a.dual(R);G=[i for i in range(n) if sum(R[i][du[i]])==1];X=[i for i in range(n) if i not in G]
        f=poly(c['field_polynomial']);need(f.degree()==2 and f.is_irreducible and f.LC()==1,'quadratic source')
        lo,hi=f.intervals(eps=s.Rational(1,10**9))[-1][0]
        d=poly([s.Rational(1,len(X)),-s.Rational(len(G),len(X))])
        ds=[poly([1]) if i in G else d for i in range(n)]
        need(len(set(v.as_expr() for v in ds))==2 and ds[0]==poly([1]),'exactly two FP values')
        need(all(min(v.eval(lo),v.eval(hi))>0 for v in ds),'strict rational positivity')
        need(all((ds[i]*ds[j]-sum((R[i][j][k]*ds[k] for k in range(n)),poly([0]))).rem(f).is_zero for i,j in itertools.product(range(n),repeat=2)),'all positive dimension products')
        q=poly(c['casimir_factor']);need(q.LC()==1 and q.is_irreducible and a.cp(R).rem(q).is_zero,'actual Casimir factor')
        need(c['gate']=='two_FP_values_Galois_PU','published general-complex gate')
        details={'two_positive_FP_values':True,'exact_root_interval':[str(lo),str(hi)],'field_polynomial':list(map(str,f.all_coeffs())),'casimir_factor':list(map(str,q.all_coeffs()))}
        if kind=='central_dimension_field':
            need(q.degree()==2,'quadratic obstruction')
            ratio=s.Rational(s.discriminant(q),s.discriminant(f))
            need(ratio>0 and (math.isqrt(int(ratio.p))**2!=ratio.p or math.isqrt(int(ratio.q))**2!=ratio.q),'distinct quadratic fields')
            details['discriminant_ratio']=str(ratio)
        else:
            need(q.degree()==1 and all(R[i][j]==R[j][i] for i,j in itertools.product(range(n),repeat=2)),'commutative degree-one codegrees')
            D=sum((v*v for v in ds),poly([0])).rem(f);beta=D.mul_ground(1/(-q.TC()))
            col=lambda v:s.Matrix([v.nth(0),v.nth(1)])
            coords=s.Matrix.hstack(col(poly([1])),col(d)).inv()*col(beta)
            need(any(v.q!=1 for v in coords),'center dimension outside integer dimension span')
            details['order_coordinates']=list(map(str,coords))
    elif kind=='frozen_rank8_signed_proof':
        need(read(FIRST/'lower_rank8_signed.json')['source_record']['tensor']==R,'signed source bound to subring class')
        details={'signed_descent':a.rank8_signed(),'all_spherical_characters':rank8_spherical(R)}
    else:raise ValueError(kind)
    proofs[j]=r['known_source_id']
    source_receipts.append({'class_index':j,'source_id':r['known_source_id'],'tensor_sha256':sha(R),'route':kind,'status':'PASS','details':details})
ledger=read(BASE/'ledger.json')['records'];wanted={r['id'] for r in ledger if r['status']=='excluded' and r['exclusion_route']=='Replayed lower-rank exclusions'}
need(len(wanted)==24,'exact inherited route cardinality')
records=[]
for row in subs['records']:
    if row['id'] not in wanted:continue
    R=data[row['id']];du=a.dual(R);witnesses=[]
    for e in row['subrings']:
        if e['class_index'] not in proofs:continue
        J=e['subset'];p=e['source_to_class_basis_map'];T=subs['classes'][e['class_index']]['tensor'];n=len(J)
        need(J[0]==0 and p[0]==0 and len(set(J))==n and sorted(p)==list(range(n)),'proper unit preserving basis map')
        need(all(du[j] in J for j in J),'dual closure')
        need(all(not R[i][j][k] for i,j in itertools.product(J,repeat=2) for k in range(12) if k not in J),'product closure')
        need(all(R[J[i]][J[j]][J[k]]==T[p[i]][p[j]][p[k]] for i,j,k in itertools.product(range(n),repeat=3)),'every embedded coefficient')
        witnesses.append(dict(e,source_id=proofs[e['class_index']]))
    need(witnesses,'at least one freshly verified excluded full tensor subcategory')
    records.append({'id':row['id'],'tensor_sha256':sha(R),'status':'retained_after_fresh_categorical_and_exact_replay_audit','witnesses':witnesses})
need({r['id'] for r in records}==wanted,'all and only 24 inherited exclusion IDs')
out={'status':'PASS','inherited_exclusions':24,'source_proofs':source_receipts,'records':records,'scope':'Arbitrary complex fusion categorification; see lower_transfers.md.','floating_point_used':False}
(HERE/'lower_transfers.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: all 24 inherited exclusions, six complete source proofs, exact full tensor embeddings')
