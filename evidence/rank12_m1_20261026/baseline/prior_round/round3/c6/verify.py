#!/usr/bin/env python3
"""Portable exact replay: no repository imports, optimizer, or asserts.

Dependencies: Python standard library and SymPy. Works under python -O.
R350 is the sole accepted general-complex exclusion in this family.
"""
import hashlib,itertools,json,runpy
from pathlib import Path
import sympy as S
from fractions import Fraction as F
P=Path(__file__).resolve().parent

def need(condition,message):
    if not condition:raise ValueError(message)
def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
frozen=json.loads((P/'frozen_inputs.json').read_text());T=frozen['tensors']
for rid,R in T.items():
    n=len(R);need(n==12,'rank')
    need(all(type(x) is int and x in (0,1) for a in R for b in a for x in b),'multiplicity')
    need(all(R[0][i][j]==R[i][0][j]==int(i==j) for i in range(n) for j in range(n)),'unit')
    need(all(sum(R[i][j][0] for j in range(n))==1 for i in range(n)),'duality uniqueness')
    du=[next(j for j in range(n) if R[i][j][0]) for i in range(n)]
    need(all(du[du[i]]==i for i in range(n)),'involutive duality')
    for i,j,k in itertools.product(range(n),repeat=3):
        need(R[i][j][k]==R[du[j]][du[i]][du[k]]==R[du[i]][k][j]==R[k][du[j]][i],'duality/reciprocity')
        for l in range(n):
            need(sum(R[i][j][a]*R[a][k][l] for a in range(n))==sum(R[j][k][a]*R[i][a][l] for a in range(n)),'associativity')
    if rid in frozen['bindings']:need(digest(R)==frozen['bindings'][rid]['tensor_sha256'],'tensor binding')

# Independently frozen optimizer-free proof. Its functions are reused below;
# it imports only standard modules and SymPy.
ns=runpy.run_path(str(P/'verify_R350.py'))
need(ns['report']['status']=='PASS','R350 proof')

# Conditional orbit quotients, independently recognized as the exact two
# rank-four families. Their exclusion is the theorem documented in theory.md;
# no categorical central lift is inferred from an orbit map.
for rid,rec in frozen['quotients'].items():
    R=T[rid];q=rec['orbit_map'];Q=rec['quotient_tensor']
    need(len(q)==12 and sorted(set(q))==list(range(4)),'quotient basis')
    for i,j,k in itertools.product(range(12),range(12),range(4)):
        need(sum(R[i][j][x] for x in range(12) if q[x]==k)==Q[q[i]][q[j]][k],'orbit quotient multiplication')
    z=0 if rid=='R12_1_561' else 1
    need(Q[1][1]==[1,0,0,0] and Q[1][2]==Q[2][1]==[0,0,0,1],'quotient invertible action')
    need(Q[2][2]==[int(z==0),int(z==1),3,3],'quotient quadratic relation')

# Independently replay the nonselfdual rank-four induction contradiction.
Q4=frozen['quotients']['R12_1_628']['quotient_tensor'];du4=[next(j for j in range(4) if Q4[i][j][0]) for i in range(4)]
B4=S.Matrix(4,4,lambda i,j:sum(Q4[a][i][k]*Q4[k][du4[a]][j] for a in range(4) for k in range(4)))
d4=3+S.sqrt(10);D4=4+12*d4;rank4_branches=0
for a,b,c in itertools.product(range(7),range(4),range(4)):
    L=S.Matrix.hstack(S.Matrix([1,0,0,0]),S.Matrix([1,0,a,6-a]),S.Matrix([1,0,b,3-b]),S.Matrix([1,0,c,3-c]))
    if L*S.ones(4,1)!=B4[:,0]:continue
    rank4_branches+=1;res=B4-L*L.T
    if not all(x>=0 for x in (-res).charpoly().all_coeffs()):continue
    low=L*L.T;gaps=[S.expand(3*sum(low[i,j]*[1,1,d4,d4][j] for j in range(4))-D4*d4) for i in [2,3]]
    def positive10(x):
        aa=S.expand(x).coeff(S.sqrt(10),0);bb=S.expand(x).coeff(S.sqrt(10),1)
        need(aa.is_Rational and bb.is_Rational,'quadratic sign domain')
        if bb==0:return aa>0
        if aa>=0 and bb>0:return True
        if aa<=0 and bb<0:return False
        return aa*aa>10*bb*bb if aa>0 else 10*bb*bb>aa*aa
    need(any(positive10(gap) for gap in gaps),'nonselfdual quotient moment contradiction')
need(rank4_branches==16,'nonselfdual quotient low completeness')
# The diagonal selfdual m=3 theorem reduces its two indicator alternatives to
# the strictly positive gaps 58+334d and 952+5896d.
need(S.expand(d4*d4-1-6*d4)==0 and 58>0 and 334>0 and 952>0 and 5896>0,'diagonal quotient polynomial gaps')

control_report=[]
for name,rid in [('R623','R12_1_623'),('R326','R12_1_326')]:
    R=T[rid];du=[next(j for j in range(12) if R[i][j][0]) for i in range(12)];G=[i for i in range(12) if sum(R[i][du[i]])==1]
    B=S.Matrix(12,12,lambda i,j:sum(R[a][i][k]*R[k][du[a]][j] for a in range(12) for k in range(12)))
    need(B==B.T,'control Gram symmetry')
    low=frozen['controls'][name]['low'];cases=frozen['controls'][name]['higher']
    pc=low['pointed_classes'];nc=low['nonpointed_classes'];tailclasses=pc+nc
    C=S.Matrix([[R[j][i][k]-R[i][j][k] for i in range(12)] for j in range(12) for k in range(12)])
    need(len(C.nullspace())==6,'control center dimension')
    for cl in [[0]]+tailclasses:need(C*S.Matrix([int(i in cl) for i in range(12)])==S.zeros(144,1),'central coefficient class')
    def columns(total,u):
        out=[]
        for v in itertools.product(*(range(total//len(cl)+1) for cl in nc)):
            if sum(len(cl)*k for cl,k in zip(nc,v))!=total:continue
            x=[0]*12;x[0]=u
            for cl,k in zip(nc,v):
                for j in cl:x[j]=k
            out.append(x)
        return out
    ls=[]
    for vv in itertools.product(columns(6,1),columns(3,1),columns(3,1),columns(6,2),columns(6,2)):
        L=S.Matrix.hstack(S.eye(12)[:,0],*map(S.Matrix,vv))
        if L*S.Matrix([1,1,1,1,2,2])==B[:,0]:ls.append(L)
    need(len(ls)==len(low['branches'])==16,'control low completeness')
    survivors=[]
    for L,rec in zip(ls,low['branches']):
        need(L.T.tolist()==rec['columns'],'control low binding')
        psd=all(x>=0 for x in (-(B-L*L.T)).charpoly().all_coeffs())
        need(psd==rec['psd'],'control PSD decision')
        if psd:survivors.append(L)
    need(len(survivors)==4 and len(cases)==8,'control domain')
    opts=[]
    for i in range(1,12):opts.append([0] if du[i]!=i else [1] if any(R[j][du[j]][i]%2 for j in range(12)) else [-1,1])
    eps=list(itertools.product(*opts));need(len(eps)==2,'control indicators')
    # Functions use their original globals dictionary; update that dictionary,
    # rather than assuming runpy's returned mapping is the function namespace.
    env=ns['system'].__globals__
    env.update(R=R,du=du,G=G,O=[i for i in range(12) if i not in G],B=B,tailclasses=tailclasses,ds=[(F(1),F(0)) if i in G else (F(3),F(1)) for i in range(12)])
    checked=0
    for bi,L in enumerate(survivors):
        for ei,ep in enumerate(eps):
            rec=cases[2*bi+ei];need(rec['branch']==bi and rec['indicators']==list(ep),'control case binding')
            if not rec['separated']:continue
            A,b,nc0=ns['system'](L,ep);y=rec['farkas']
            need(nc0==rec['column_count'] and len(A)==rec['rows'] and len(y)==len(b),'control system metadata')
            need(all(type(x) is int for x in y),'control ray integers')
            need(all(sum(a*c for a,c in zip(row,y))>=0 for row in zip(*A)),'control dual nonnegativity')
            dot=sum(a*c for a,c in zip(b,y));need(dot==rec['bTy'] and dot<0,'control negative pairing');checked+=1
    need(checked==4,'four restricted-indicator exclusions')
    rejected_sign=1 if name=='R623' else -1
    need(all((rec['indicators'][-1]==rejected_sign)==rec['separated'] for rec in cases),'control indicator distinction')
    control_report.append({'id':rid,'exact_restricted_exclusions':checked,'rejected_pointed_involution_indicator':rejected_sign,'other_indicator_status':'no exclusion certificate obtained; no model inferred'})
report={'status':'PASS','valid_frozen_tensors':6,'new_general_exclusions':['R12_1_350'],'new_models':[],'unresolved':['R12_1_332','R12_1_561','R12_1_623','R12_1_628'],'R350_exact_farkas_cases':32,'controls':control_report,'conditional_rank4_quotient_bindings':2,'nonselfdual_rank4_low_branches':rank4_branches,'optimizer_used':False,'parent_repository_imports':False,'assertions_used':False}
(P/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
