#!/usr/bin/env python3
"""Force the HI(C5) Q-system dual tensor from its actual canonical module.

No center data, multiplicity bound, or census input enters reconstruction.
"""
from pathlib import Path
import hashlib,os
import itertools as it
import json
import sys
import sympy as s

HERE=Path(__file__).resolve().parent
REPO=Path(os.environ.get('FUSION_CLASSIFICATION_REPO',Path(__file__).resolve().parents[2])).resolve()

def require(ok,msg):
    if not ok: raise RuntimeError(msg)

def module(shifts, diagonal):
    A=s.zeros(6)
    for i in range(5):
        for t in shifts:A[i,(i+t)%5]+=1
        A[i,5]=A[5,i]=1
    A[5,5]=diagonal
    return A

M=[s.eye(6),module([0],4),module([],3),module([],3),module([1,-1],5),module([2,-2],5)]
require(all(A*B==B*A for A in M for B in M),'commuting canonical actions')
span=s.Matrix.hstack(*[s.Matrix(list(A)) for A in M]).rank()
require(span==4,'canonical image dimension four')
triples=list(it.combinations_with_replacement(range(1,6),3))
xs=s.symbols('x:'+str(len(triples))); index=dict(zip(triples,xs))
branches=[]
unique=None
for dual in [(0,1,2,3,4,5),(0,1,3,2,4,5)]:
    def T(i,j,k):
        q=sorted((i,j,k))
        return s.Integer(q[2]==dual[q[1]]) if q[0]==0 else index[tuple(q)]
    equations=[]
    for i,j in it.combinations_with_replacement(range(1,6),2):
        equations.extend(list(M[i]*M[j]-sum((T(i,j,dual[k])*M[k] for k in range(6)),s.zeros(6))))
    equations.extend(index[t]-T(*[dual[k] for k in t]) for t in triples)
    A,y=s.linear_eq_to_matrix(equations,xs)
    solution=list(s.linsolve((A,y),xs))
    require(len(solution)==1,'single affine solution space')
    row=solution[0]
    free=set().union(*(v.free_symbols for v in row))
    branch={'dual':list(dual),'equations':len(equations),'linear_rank':A.rank(),'free_parameters':sorted(map(str,free)),'trilinear_solution':[{ 'triple':list(t),'value':str(v)} for t,v in zip(triples,row)]}
    if dual[2]==3:
        require(not free and row[15]==s.Rational(-1,2),'paired duality has a negative forced coefficient')
        branch['result']='IMPOSSIBLE: T(b1,b1,b1)=-1/2'
    else:
        require(free=={xs[25]},'one free coefficient')
        t=xs[25]
        require(row[16]==t-1 and row[19]==1-t,'nonnegative coefficients force t=1')
        forced=[v.subs(t,1) for v in row]
        require(all(v.is_Integer and v>=0 for v in forced),'forced nonnegative integers')
        values=dict(zip(triples,map(int,forced)))
        def F(i,j,k):
            q=sorted((i,j,k))
            return int(q[1]==q[2]) if q[0]==0 else values[tuple(q)]
        unique=[[[F(i,j,k) for k in range(6)] for j in range(6)] for i in range(6)]
        require(all(M[i]*M[j]==sum((unique[i][j][k]*M[k] for k in range(6)),s.zeros(6)) for i,j in it.product(range(6),repeat=2)),'all module products')
        require(all(sum(unique[i][j][z]*unique[z][k][l] for z in range(6))==sum(unique[j][k][z]*unique[i][z][l] for z in range(6)) for i,j,k,l in it.product(range(6),repeat=4)),'all associativity identities')
        branch['result']='UNIQUE: t=1 from T(b1,b1,b2)>=0 and T(b1,b2,b2)>=0'
    branches.append(branch)

# Source and pre-existing constructor are read only after the unique tensor exists.
sys.path.insert(0,str(REPO/'supplements/rank6/software'))
from additional_models import izumi_dual
require(unique==izumi_dual(),'all216 coefficients match existing independently encoded EGformula')
census=json.loads((REPO/'supplements/rank6/data/census.json').read_text())
case=next(r for r in census if r['id']=='R6_2_143')
maps=[(0,)+tail for tail in it.permutations(range(1,6)) if all(unique[i][j][k]==case['N'][((0,)+tail)[i]][((0,)+tail)[j]][((0,)+tail)[k]] for i,j,k in it.product(range(6),repeat=3))]
require(maps,'full216 unital census tensor match')
out={'status':'PASS','repository_commit':'8014c749c17ddd2ad3d1b99a4359d49a8be921c5','source_theorem':'Izumi, QuantumTopol9(2018), pp527–529, Eq7.1 and sum_j n_j^2=2 preceding Proposition7.4; actual canonical module of Qsystem1+rho in HI(C5)','source_pdf_sha256':'f9c1a7ac47e83ca6b41677efceda3d2bc218d3ae9cca76c6775d6b9b137a6b1f','basis':['1','a','b1','b2','c1','c2'],'module_basis':['i0','i1','i2','i3','i4','tau'],'module_matrices':[[list(map(int,A.row(i))) for i in range(6)] for A in M],'image_rank':span,'kernel_dimension':6-span,'commutativity_argument':'Semisimple complex fusion algebra; every noncommutative simple block has dimension>=4 and must lie in kernel of the commutative image, whose dimension is2.','duality_branches':branches,'forced_tensor':unique,'tensor_maximum':max(it.chain.from_iterable(it.chain.from_iterable(unique))),'source_id':'R6_2_143','census_tensor_sha256':hashlib.sha256(json.dumps(case['N'],separators=(',',':')).encode()).hexdigest(),'all_model_to_census_maps':[list(p) for p in maps],'verified_tensor_entries':216,'associativity_checks':1296,'candidate_center_data_used':False,'multiplicity_bound_assumed':False,'census_used_for_reconstruction':False,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['module_matrices','forced_tensor','duality_branches']},indent=2))
