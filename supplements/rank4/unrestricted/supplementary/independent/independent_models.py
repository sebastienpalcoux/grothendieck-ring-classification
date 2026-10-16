#!/usr/bin/env python3
"""Reconstruct the fifteen model tensors independently of the supplied software.
Uses standard group/product/truncated SU(2) rules and explicit published
rules for H_1, Ad(E8), Z/2-quadratic and near-group models. This checks
based-ring identifications, not associators or the original existence proofs.
All isomorphisms and dimension comparisons are exact; decimals are display only.
"""

def require(test, message='independent check failed'):
    if not test:
        raise RuntimeError(message)

import argparse,itertools,json
from pathlib import Path
import sympy as s

def ring(n):
    R=[[[0]*n for _ in range(n)]for _ in range(n)]
    for i in range(n):R[0][i][i]=R[i][0][i]=1
    return R

def put(R,i,j,v):R[i][j]=list(v);R[j][i]=list(v)
def group(n,mult):
    R=ring(n)
    for i,j in itertools.product(range(n),repeat=2):R[i][j][mult(i,j)]=1
    return R

def product(A,B):
    n,m=len(A),len(B)
    return [[[A[i//m][j//m][k//m]*B[i%m][j%m][k%m] for k in range(n*m)] for j in range(n*m)] for i in range(n*m)]

def su2even(level):
    labels=list(range(0,level+1,2));R=ring(len(labels))
    for i,a in enumerate(labels):
        for j,b in enumerate(labels):
            R[i][j]=[int(abs(a-b)<=c<=min(a+b,2*level-a-b) and (a+b+c)%2==0)for c in labels]
    return R

def near(m):
    R=ring(4)
    for i,j in itertools.product(range(3),repeat=2):R[i][j][(i+j)%3]=1
    for i in range(3):put(R,i,3,[0,0,0,1])
    put(R,3,3,[1,1,1,m]);return R

def quadratic(m,nonself=False):
    R=ring(4);put(R,1,1,[1,0,0,0]);put(R,1,2,[0,0,0,1]);put(R,1,3,[0,0,1,0])
    sq=[0,1,m,m] if nonself else [1,0,m,m]
    cross=[1,0,m,m] if nonself else [0,1,m,m]
    put(R,2,2,sq);put(R,3,3,sq);put(R,2,3,cross);return R

def d10():
    R=ring(4);put(R,1,1,[1,0,0,0]);put(R,1,2,[0,0,1,0]);put(R,1,3,[0,0,0,1])
    put(R,2,2,[1,1,0,1]);put(R,2,3,[0,0,1,1]);put(R,3,3,[1,1,1,0]);return R

def h1():
    # Grossman--Snyder, Table 2, order 1, nu, eta, mu.
    R=ring(4)
    for i,j,v in [(1,1,[1,2,2,1]),(1,2,[0,2,1,1]),(1,3,[0,1,1,1]),(2,2,[1,1,1,1]),(2,3,[0,1,1,0]),(3,3,[1,1,0,0])]:put(R,i,j,v)
    return R

def e8():
    # Evans--Jones, Section 3.3, order 1,A,B,tau.
    R=ring(4)
    for i,j,v in [(1,1,[1,1,1,0]),(1,2,[0,1,2,1]),(1,3,[0,0,1,0]),(2,2,[1,2,3,1]),(2,3,[0,1,1,0]),(3,3,[1,0,0,1])]:put(R,i,j,v)
    return R

def permutations(A,B):
    return [(0,)+p for p in itertools.permutations(range(1,4)) if all(A[i][j][k]==B[((0,)+p)[i]][((0,)+p)[j]][((0,)+p)[k]]for i,j,k in itertools.product(range(4),repeat=3))]

p=argparse.ArgumentParser(description=__doc__);p.add_argument('archive',type=Path);p.add_argument('--output',type=Path);a=p.parse_args()
models=json.loads((a.archive/'supplementary/classification/data/models.json').read_text())
print('Archive labels:',[m['model']for m in models])
C2=group(2,lambda i,j:(i+j)%2);Fib=ring(2);put(Fib,1,1,[1,1])
constructions=[group(4,lambda i,j:i^j),product(Fib,C2),d10(),su2even(6),product(Fib,Fib),su2even(7),group(4,lambda i,j:(i+j)%4),near(0),quadratic(1,True),quadratic(2),h1(),near(2),e8(),near(3),near(6)]
expected_names=['Vec_C2xC2','Fib_x_Vec_C2','Rep_D10','Ad_SU2_6','Fib_x_Fib','Ad_SU2_7','Vec_C4','TY_C3','S_prime','2D2','Haagerup_H1','Rep_A4','Ad_E8','Near_C3_3','Near_C3_6']
# Match through tensors, not fragile spelling of the archive's model labels.
rows=[];matched=set()
for label,R in zip(expected_names,constructions):
    hits=[(m,permutations(R,m['matrices']))for m in models];hits=[(m,pp)for m,pp in hits if pp]
    require(len(hits) == 1, label)
    model,pp=hits[0];require(model['model'] not in matched, 'check failed (independent_models.py:76)');matched.add(model['model'])
    N=list(map(s.Matrix,R));B=sum((n*n.T for n in N),s.zeros(4));cp=B.charpoly().as_poly()
    below44=all((44*s.eye(4)-B)[:k,:k].det()>0 for k in range(1,5))
    if label=='Near_C3_6':
        D=24+12*s.sqrt(3);ds=s.Matrix([1,1,1,3+2*s.sqrt(3)]);require(s.simplify(B * ds - D * ds) == s.zeros(4, 1), 'check failed (independent_models.py:80)')
        require(not below44, 'check failed (independent_models.py:81)')
    else:require(below44, 'check failed (independent_models.py:82)')
    largest=max(cp.intervals(eps=s.Rational(1,10**10)),key=lambda t:t[0][1])[0]
    rows.append({'independent_model':label,'archive_model':model['model'],'archive_label':model['label'],
                 'source_to_archive_permutation':list(pp[0]),'multiplicity':max(v for mat in R for row in mat for v in row),
                 'casimir_polynomial':list(map(int,cp.all_coeffs())),
                 'FP_dimension_isolating_interval':list(map(str,largest)),
                 'dimension_strictly_less_than_44':below44})
result={'passed':True,'models':len(rows),'maximum_multiplicity':max(r['multiplicity']for r in rows),
        'maximum_FP_dimension':'24 + 12*sqrt(3)','unique_maximum_model':'Near_C3_6',
        'scope':'Exact independent fusion-rule reconstruction and based-ring isomorphisms; no new verification of external associators.',
        'rows':rows}
print(json.dumps(result,indent=2))
if a.output:a.output.write_text(json.dumps(result,indent=2)+'\n')
