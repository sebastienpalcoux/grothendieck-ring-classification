#!/usr/bin/env python3
import json,itertools
from pathlib import Path
import sympy as s
ROOT=Path('/workspace/scratch/90f37cc83103/online_revision/grothendieck-ring-classification')
OUT=Path(__file__).parent
R=json.load(open(OUT.parent/'inputs/R8_3_1768.json'))['fusion_tensor']
Ns=[s.Matrix(8,8,lambda k,j:R[i][j][k])for i in range(8)]
f=next(f for f in json.load(open(ROOT/'evidence/rank8_next_20261021/quadratic/profile_closure.json'))['R8_3_1768']['surviving_factors']if f['candidate_index']==7)
B=s.Matrix(f['B']);U=s.zeros(8,3)
for a,(i,j)in enumerate([(1,2),(3,4),(5,6)]):U[i,a]=1;U[j,a]=-1
P=s.eye(8)-U*U.T/2
Bp=B.pinv();A=[B*N*Bp for N in Ns]
for i in range(8):
 assert A[i].T==A[i]and A[i]*B==B*Ns[i]and A[i]*U==s.zeros(8,3)
G=s.Matrix([[0,1,0],[1,0,0],[0,0,-1]])
assert A[1]+U*G*U.T/2==s.eye(8)[:,[7,3,4,1,2,6,5,0]]
# Ordinary rational characters; the two irrational dimension characters
# cannot occur on the one-dimensional g=+1 kernel eigenspace.
chars=[[1,-1,1,-1,0,0,1,-1],[1,-1,0,1,1,-1,-1,0],[1,-1,0,1,-2,2,-1,0],[1,1,0,1,-1,-1,1,0],[1,1,1,-1,0,0,-1,1],[1,-1,-2,-1,0,0,1,2]]

def possible(i):
 bound=max(abs(c[i])for c in chars);vals=[]
 # H_ab=2(N_ab-A_ab), and |H_ab| <= spectral radius bound.
 pos=[(1,1),(1,3),(1,5),(5,5)]
 domains=[]
 for r,t in pos:
  domains.append([2*(n-A[i][r,t])for n in range(max(0,int(s.ceiling(A[i][r,t]-s.Rational(bound,2)))),int(s.floor(A[i][r,t]+s.Rational(bound,2)))+1)])
 for a,b,c,d in itertools.product(*domains):
  H=s.Matrix([[a,b,c],[b,a,-c],[c,-c,d]])
  T=A[i]+U*H*U.T/2
  if not all(x.is_Integer and x>=0 for x in T):continue
  # Source characteristic polynomial restricted to rational chars.
  prod=s.eye(3)
  for q in sorted(set(c[i]for c in chars)):prod=prod*(H-q*s.eye(3))
  if prod!=s.zeros(3):continue
  vals.append((H,T))
 return vals
opts={i:possible(i)for i in [2,3,4]}
print('independent possibilities',{i:len(v)for i,v in opts.items()})
outs=[]
for h2,h3,h4 in itertools.product(*(opts[i]for i in [2,3,4])):
 Hs=[s.eye(3),G,h2[0],h3[0],h4[0],G*h4[0],G*h3[0],G*h2[0]]
 if any(Hs[i]*Hs[j]!=Hs[j]*Hs[i]for i in [2,3,4]for j in [2,3,4]):continue
 if any(Hs[i]*Hs[j]!=sum((R[i][j][k]*Hs[k]for k in range(8)),s.zeros(3))for i in range(8)for j in range(8)):continue
 Ts=[A[i]+U*Hs[i]*U.T/2 for i in range(8)]
 assert all(all(t.is_Integer and t>=0 for t in T)for T in Ts)
 assert all(T.T==T for T in Ts)
 assert all(Ts[i]*Ts[j]==sum((R[i][j][k]*Ts[k]for k in range(8)),s.zeros(8))for i in range(8)for j in range(8))
 out={'kernel_action':[T.tolist()for T in Hs],'full_action':[[list(map(int,row))for row in T.tolist()]for T in Ts]}
 outs.append(out)
print('completions',len(outs))
(OUT/'gh6_m2_module_probe.json').write_text(json.dumps({'scope':'Exact based-module action completions for R1768 candidate algebra 1+X3; no categorical algebra asserted','B':B.tolist(),'completions':outs},default=str,indent=2)+'\n')
