#!/usr/bin/env python3
"""Exact source-bound R820/R869 centralizer construction replay.

Categorical existence is supplied by Evans--Gannon's actual C*-near-group
categories and their established n=5 center data; see NEARGROUP_CENTRALIZER_PROOF.md.
This checks the full algebraic identification, not just dimensions or indicators.
Uses the Python standard library only. All checks survive python -O.
"""
from fractions import Fraction as F
import argparse,gzip,itertools,json,hashlib
from pathlib import Path
# Q[sqrt5,z], z^3-3z+1=0; coordinate order 1,z,z^2,q,qz,qz^2.
def scalar(x):return (F(x),F(0),F(0),F(0),F(0),F(0))
ZERO=scalar(0);ONE=scalar(1);Q=(F(0),F(0),F(0),F(1),F(0),F(0));Z=(F(0),F(1),F(0),F(0),F(0),F(0))
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def neg(x):return tuple(-a for a in x)
def sub(x,y):return add(x,neg(y))
def mul(x,y):
 p=[[F(0)]*5 for _ in range(3)]
 for i,a in enumerate(x):
  for j,b in enumerate(y):p[i//3+j//3][i%3+j%3]+=a*b
 for k in range(5):p[0][k]+=5*p[2][k]
 for h in range(2):
  for k in [4,3]:p[h][k-2]+=3*p[h][k];p[h][k-3]-=p[h][k]
 return tuple(p[h][k] for h in range(2) for k in range(3))
def scale(x,c):return tuple(a*F(c) for a in x)
def total(xs):
 r=ZERO
 for x in xs:r=add(r,x)
 return r
a=scale(add(scalar(5),scale(Q,3)),F(1,2));b=add(a,ONE);c=add(a,scalar(2));D=scale(b,45)
inv_a=scale(sub(scale(Q,3),scalar(5)),F(1,10));inv_b=scale(sub(scalar(7),scale(Q,3)),F(1,2));inv_c=scale(sub(scalar(9),scale(Q,3)),F(1,18));invD=scale(inv_b,F(1,45))
P=[scalar(2),Z,sub(mul(Z,Z),scalar(2))]
for i in range(3,9):P.append(sub(mul(Z,P[-1]),P[-2]))
def cos5(k):
 k%=5
 return scalar(2) if k==0 else scale(add(scalar(-1),scale(Q,1 if k in [1,4] else -1)),F(1,2))
def matrix(which):
 m=1 if which==820 else 2;g=[(1,0),(0,1),(1,1),(1,2)] if which==820 else [1,2,3,4]
 M=[[ZERO for j in range(8)] for i in range(8)];dims=[ONE,b,c,c,a,a,a,a]
 for j in range(8):M[0][j]=M[j][0]=dims[j]
 M[1][1]=ONE
 for j in [2,3]:M[1][j]=M[j][1]=c
 for j in range(4,8):M[1][j]=M[j][1]=neg(a)
 for i,k in enumerate([1,2]):
  for j,l in enumerate([1,2]):M[2+i][2+j]=mul(c,cos5(2*m*k*l))
 for i,x in enumerate(g):
  for j,y in enumerate(g):
   if which==820:co=scalar(2 if (x[0]*y[0]+x[1]*y[1])%3==0 else -1)
   else:co=P[(2*x*y)%9]
   M[4+i][4+j]=neg(mul(a,co))
 return M

def tensor(M):
 invdims=[ONE,inv_b,inv_c,inv_c,inv_a,inv_a,inv_a,inv_a]
 N=[]
 for i in range(8):
  row=[]
  for j in range(8):
   rr=[]
   for k in range(8):
    x=mul(invD,total(mul(mul(mul(M[i][l],M[j][l]),M[k][l]),invdims[l]) for l in range(8)))
    if any(x[1:]) or x[0].denominator!=1 or x[0]<0:raise ValueError(('not fusion',i,j,k,x))
    rr.append(int(x[0]))
   row.append(rr)
  N.append(row)
 return N

SOURCE_SHA256='35a8d69e9af8c873b3003890218a35b38b792abb89c19066f6705bf9c1c1d1ed'
HASHES={820:'88d4e0d03d1f45b727bb5d973ee4c47ef114ff4870f397d9f08342d5db1d0373',869:'6fd67687c6a4590e43cf539442042092ebc28973b626127f40d6f27fb66de112'}
MAPS={820:(0,2,6,7,1,3,4,5),869:(0,3,6,7,1,2,5,4)}

def require(ok,message):
    if not ok:
        raise ValueError(message)

def flat(R):
    return tuple(c for a in R for b in a for c in b)

def model(which):
    """Return the exact 8x8x8 tensor in the displayed centralizer basis."""
    require(which in MAPS,'unknown model')
    return tensor(matrix(which))

def verify(R,which):
    require(len(R)==8 and all(len(row)==8 and all(len(v)==8 for v in row) for row in R),'source rank')
    digest=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
    require(digest==HASHES[which],'immutable census tensor digest')
    M=matrix(which)
    for x,y in [(a,inv_a),(b,inv_b),(c,inv_c),(D,invD)]:
        require(mul(x,y)==ONE,'exact dimension inverse')
    for i,j in itertools.product(range(8),repeat=2):
        require(M[i][j]==M[j][i],'S symmetry')
        require(total(mul(M[i][k],M[k][j]) for k in range(8))==(D if i==j else ZERO),'S orthogonality')
    N=tensor(M);p=MAPS[which]
    require(sorted(p)==list(range(8)) and p[0]==0,'unital basis permutation')
    for i,j,k in itertools.product(range(8),repeat=3):
        require(N[i][j][k]==R[p[i]][p[j]][p[k]],'full tensor correspondence')
        require(N[0][i][j]==int(i==j) and N[i][j][0]==int(i==j),'unit and self-duality')
    for i,j,k,l in itertools.product(range(8),repeat=4):
        require(sum(N[i][j][x]*N[x][k][l] for x in range(8))==sum(N[j][k][x]*N[i][x][l] for x in range(8)),'associativity')
    return {'id':f'R8_2_{which}','status':'PASS','tensor_sha256':digest,
      'construction':'nonpointed Mueger factor of Z(NG(C5,5))',
      'group_prime':'C3 x C3' if which==820 else 'C9',
      'quadratic_form_prime':'(x^2+y^2)/3' if which==820 else '2*x^2/9',
      'model_basis':['a_0','b_0','c_{1,-1}','c_{2,-2}']+(['d_{0,(1,0)}','d_{0,(0,1)}','d_{0,(1,1)}','d_{0,(1,2)}'] if which==820 else ['d_{0,1}','d_{0,2}','d_{0,3}','d_{0,4}']),
      'permutation_model_to_source':list(p),'permutation_source_to_model':[p.index(i) for i in range(8)],
      'verified_tensor_entries':512,'exact_field':'Q[q,z]/(q^2-5,z^3-3*z+1)',
      'categorical_status':'unitary modular realization',
      'existence_reference':'Evans--Gannon 1208.1500 Proposition 6, Table 2, and finite n<=13 verification after Conjecture 2'}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[3])
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    source=args.repo/'supplements/rank8/data/rank8_tables.txt.gz'
    digest=hashlib.sha256(source.read_bytes()).hexdigest()
    require(digest==SOURCE_SHA256,'immutable census archive digest')
    with gzip.open(source,'rt') as f:
        tensors=[json.loads(line.replace('{','[').replace('}',']')) for line in f]
    tensors=sorted((R for R in tensors if max(flat(R))==2),key=flat)
    report={'status':'PASS','source_sha256':digest,
        'scope':'exact full-tensor identification of two existing unitary modular centralizers',
        'cases':[verify(tensors[which-1],which) for which in MAPS]}
    out=json.dumps(report,indent=2)+'\n'
    if args.output:
        args.output.write_text(out)
    print(out,end='')

if __name__=='__main__':
    main()
