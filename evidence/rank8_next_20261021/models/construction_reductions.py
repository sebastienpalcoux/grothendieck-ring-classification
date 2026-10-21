"""Exact new construction reductions, not categorification certificates.

Run normally or with -O. All checks use explicit exceptions.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
from types import SimpleNamespace
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE_CENSUS = ROOT/'evidence/rank8_m3_20261021/pipeline/census_m3.json'
DATA = SimpleNamespace(**{row['id']: row['tensor'] for row in json.loads(SOURCE_CENSUS.read_text())})
IDS = ['R8_3_'+str(n) for n in (65,721,928,941,982,1154,1768,1795,3472)]

def need(ok, label):
    if not ok:
        raise ValueError(label)

def digest(value):
    return hashlib.sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()

def duals(N):
    return [next(j for j in range(len(N)) if N[i][j][0]) for i in range(len(N))]

def validate(N):
    n=len(N); du=duals(N)
    need(all(N[0][i][j]==N[i][0][j]==int(i==j) for i in range(n) for j in range(n)), 'unit')
    need(all(N[i][j][k]>=0 and isinstance(N[i][j][k],int) for i in range(n) for j in range(n) for k in range(n)), 'positive integer tensor')
    need(all(N[i][j][0]==int(du[i]==j) for i in range(n) for j in range(n)), 'duality')
    need(all(N[i][j][k]==N[du[j]][du[i]][du[k]]==N[du[i]][k][j] for i in range(n) for j in range(n) for k in range(n)), 'involution and Frobenius reciprocity')
    need(all(sum(N[i][j][h]*N[h][k][l] for h in range(n))==sum(N[j][k][h]*N[i][h][l] for h in range(n)) for i in range(n) for j in range(n) for k in range(n) for l in range(n)), 'associativity')
    return du

def closure(N, start):
    out=set(start)
    while True:
        old=out.copy()
        for i in old:
            for j in old:
                out.update(k for k,v in enumerate(N[i][j]) if v)
        if old==out:
            return sorted(out)

def casimir(N):
    du=duals(N); n=len(N)
    C=sum((s.Matrix(N[i])*s.Matrix(N[du[i]]) for i in range(n)),s.zeros(n))
    return C

def quotient(N,g):
    n=len(N);left=[N[g][i].index(1) for i in range(n)]
    right=[N[i][g].index(1) for i in range(n)]
    need(left==right,'quotient requires central g')
    orbits=[]
    for i in range(n):
        o=sorted({i,left[i]})
        if o not in orbits:
            orbits.append(o)
    need(all(len(o)==2 for o in orbits),'free g action')
    Q=[[[sum(N[a[0]][b[0]][k] for k in c) for c in orbits] for b in orbits] for a in orbits]
    validate(Q)
    return orbits,Q

def rank5(m, nonselfdual=False):
    N=[[[0]*5 for _ in range(5)] for _ in range(5)]
    for i in range(5):
        N[0][i][i]=N[i][0][i]=1
    N[1][1][0]=1
    N[1][2][3]=N[2][1][3]=1
    N[1][3][2]=N[3][1][2]=1
    N[1][4][4]=N[4][1][4]=1
    e=0 if nonselfdual else 1
    N[2][2]=N[3][3]=[e,1-e,m,4-m,4]
    N[2][3]=N[3][2]=[1-e,e,4-m,m,4]
    for i in (2,3):
        N[i][4]=N[4][i]=[0,0,4,4,9]
    N[4][4]=[1,1,9,9,19]
    return N

def run():
    records=[]
    for rid in IDS:
        N=getattr(DATA,rid);du=validate(N)
        ad=closure(N,[0]+[k for i in range(8) for k in range(8) if N[i][du[i]][k]])
        need(ad==list(range(8)),'full adjoint closure')
        records.append({'id':rid,'tensor_sha256':digest(N),'adjoint_closure':ad,
          'ordinary_faithful_group_graded_zesting':'no nontrivial grading available; this does not address arbitrary super/para associator reconstruction'})
    quartic=[]
    reference=None
    for rid,g in [('R8_3_928',7),('R8_3_941',3),('R8_3_982',6)]:
        N=getattr(DATA,rid);orbits,Q=quotient(N,g)
        if reference is None:
            reference=Q
        maps=[(0,)+p for p in itertools.permutations(range(1,4))]
        maps=[p for p in maps if all(Q[i][j][k]==reference[p[i]][p[j]][p[k]] for i in range(4) for j in range(4) for k in range(4))]
        need(maps,'common quartic quotient')
        quartic.append({'id':rid,'orbits':orbits,'quotient_tensor':Q,'maps_to_R928_quotient':[list(p) for p in maps]})
    r5=[]
    a=6+3*s.sqrt(5);dims=[1,1,a,a,2*a+2];D=s.expand(sum(t*t for t in dims))
    need(D==540+240*s.sqrt(5),'rank5 dimension')
    for m,ns in [(m,False) for m in range(5)]+[(2,True)]:
        N=rank5(m,ns);du=validate(N)
        need(all(s.expand(dims[i]*dims[j]-sum(N[i][j][k]*dims[k] for k in range(5)))==0 for i in range(5) for j in range(5)),'rank5 exact positive dimension character')
        C=casimir(N);eig=C.eigenvals()
        cd=[{'formal_codegree':str(f),'multiplicity':int(n),'distinguished_center_dimension':str(s.radsimp(D/f))} for f,n in sorted(eig.items(),key=lambda kv:str(kv[0]))]
        r5.append({'m':m,'nonselfdual_pair':ns,'tensor':N,'duals':du,'casimir_polynomial':str(s.factor(C.charpoly().as_expr())),
          'formal_codegrees':cd,'branch':'excluded_by_dimension_field' if m in (1,3) else 'necessary_Morita_dual_ring_only'})
    source=getattr(DATA,'R8_3_1154');g=3
    L=[source[g][i].index(1) for i in range(8)];R=[source[i][g].index(1) for i in range(8)]
    double=[]
    for i in range(8):
        o=sorted({i,L[i],R[i],L[R[i]]})
        if o not in double:
            double.append(o)
    need(sorted(map(len,double))==[2,2,4],'C2 double orbit sizes')
    sourceD=[1,7+3*s.sqrt(5),7+3*s.sqrt(5),1,a,a,7+3*s.sqrt(5),7+3*s.sqrt(5)]
    need(all(s.expand(sourceD[i]*sourceD[j]-sum(source[i][j][k]*sourceD[k] for k in range(8)))==0 for i in range(8) for j in range(8)),'source dimensions')
    gram=json.loads((ROOT/'evidence/rank8_frontier_20261021/central_integrality/integer_gram_1154.json').read_text())
    highdim=[s.expand(sum(v[i]*sourceD[i+1] for i in range(7))) for v in gram['high_columns']]
    conditions={3:15+6*s.sqrt(5),14:255+114*s.sqrt(5),10:135+60*s.sqrt(5),2:54+24*s.sqrt(5)}
    need(all(highdim[i]==d for i,d in conditions.items()),'specified high-column dimensions')
    need(all([j for j,d in enumerate(highdim) if d==wanted]==[i] for i,wanted in conditions.items()),'unique high-column dimensions')
    return {'kind':'new_exact_construction_reductions','status':'no model and no ring exclusion claimed',
      'all_nine':records,'quartic_common_quotient':quartic,
      'R1154_C2_Morita_dual':{'hypothesis':'pointed C2 associator cohomology class is trivial, so A=1+g has its regular separable algebra',
       'double_orbits':double,'dual_rank':5,'dual_dimensions':list(map(str,dims)),
       'six_labelled_branches':r5,'center_presence_necessary_condition':'high[10]>=1 OR (high[3]>=1 AND high[14]>=1)',
       'pseudo_unitary_twist_condition':'the additional distinguished center simples in this condition have twist 1',
       'source_Gram_receipt_sha256':hashlib.sha256((ROOT/'evidence/rank8_frontier_20261021/central_integrality/integer_gram_1154.json').read_bytes()).hexdigest()},
      'R1154_R1795_Morita_compatibility':{'same_Casimir_polynomial':str(s.factor(casimir(source).charpoly().as_expr())),
       'equality_verified':casimir(source).charpoly().all_coeffs()==casimir(getattr(DATA,'R8_3_1795')).charpoly().all_coeffs(),
       'necessary_condition':'R1154 center has at least four high-column-2 simples of dimension D/10, each twist 1 in the pseudo-unitary setting',
       'scope':'necessary compatibility only; no common center or Morita equivalence constructed'}}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');args=p.parse_args()
    result=run();path=HERE/'construction_reductions.json'
    if args.write:
        path.write_text(json.dumps(result,indent=2)+'\n')
    else:
        need(result==json.loads(path.read_text()),'receipt replay')
    print('PASS: nine adjoint closures, common quartic quotient, six rank5 C2-Morita dual branches, exact center-dimension conditions. No categorification claim.')
