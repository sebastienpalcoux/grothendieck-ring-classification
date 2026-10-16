#!/usr/bin/env python3
"""Exact source and finite linear-algebra inputs for the C3/A4 reduction."""
import argparse,collections,gzip,hashlib,itertools,json,subprocess,sys
from pathlib import Path
import sympy as S

HERE=Path(__file__).resolve().parent
ROOT=next((p for p in HERE.parents if (p/'supplements/rank7/data/rank7_tables.txt.gz').exists()),Path('.'))

def require(x,m):
 if not x:raise RuntimeError(m)
def rank2(M):
 M=[row[:] for row in M];r=0
 for j in range(len(M[0])):
  p=next((i for i in range(r,len(M)) if M[i][j]),None)
  if p is None:continue
  M[r],M[p]=M[p],M[r]
  for i in range(len(M)):
   if i!=r and M[i][j]:M[i]=[a^b for a,b in zip(M[i],M[r])]
  r+=1
 return r

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=ROOT);ap.add_argument('--output',type=Path);args=ap.parse_args()
 targets={'R7_2_236':(4,6),'R7_4_2167':(4,12),'R7_4_2716':(5,12),'R7_3_1022':(5,8)}
 ct=collections.Counter();cases=[];z=S.Symbol('z')
 for line in gzip.open(args.repo/'supplements/rank7/data/rank7_tables.txt.gz','rt'):
  if not line.strip():continue
  N=json.loads(line.replace('{','[').replace('}',']'));mult=max(v for row in N for col in row for v in col);ct[mult]+=1;rid=f'R7_{mult}_{ct[mult]}'
  if rid not in targets:continue
  E,m=targets[rid];d=(m+S.sqrt(m*m+16))/2;rho=[i for i in range(7) if i not in [0,1,2,E]]
  dims=[S.Integer(1) if i<3 else S.Integer(3) if i==E else d for i in range(7)]
  require(all(S.expand(dims[i]*dims[j]-sum(N[i][j][k]*dims[k] for k in range(7)))==0 for i,j in itertools.product(range(7),repeat=2)),'Exact FP character')
  require(all(v.is_positive for v in dims),'Positive dimensions')
  require(N[E][E]==[1 if i<3 else 2 if i==E else 0 for i in range(7)],'Integral Rep(A4) square')
  require(N[0]==S.eye(7).tolist(),'Unit')
  du=[]
  for i in range(7):
   q=[j for j in range(7) if N[i][j][0]];require(len(q)==1 and N[i][q[0]][0]==1,'Dual');du.append(q[0])
  L=[S.Matrix(N[i]).T for i in range(7)]
  for i,j in itertools.product(range(7),repeat=2):
   require(L[i]*L[j]==sum((N[i][j][k]*L[k] for k in range(7)),S.zeros(7)),'Associativity')
   for k in range(7):require(N[i][j][k]==N[du[i]][k][j]==N[k][du[j]][i],'Frobenius reciprocity')
  require(L[1]**3==S.eye(7) and L[1]!=S.eye(7),'Order3 generator')
  require(N[1][E]==N[E][1]==[int(i==E) for i in range(7)],'Fixed X')
  require({next(k for k in range(7) if N[1][i][k]) for i in rho}==set(rho),'rho orbit invariant')
  require(all(N[1][i][i]==0 for i in rho),'rho orbit free')
  I=S.eye(5);ME=S.zeros(5);ME[:4,:4]=S.ones(4)-S.eye(4);ME[4,4]=3;MR=S.zeros(5)
  for i in range(4):MR[i,4]=MR[4,i]=1
  MR[4,4]=m;mats=[I if i<3 else ME if i==E else MR for i in range(7)]
  for i,j in itertools.product(range(7),repeat=2):require(mats[i]*mats[j]==sum((N[i][j][k]*mats[k] for k in range(7)),S.zeros(5)),'Module fusion products')
  mp=S.Poly(S.minpoly(d/4,z),z).monic();require(mp.TC()==-S.Rational(1,4),'d/4 nonintegrality')
  cases.append({'id':rid,'status':'reduction_verified','scope':'general_complex','tensor_sha256':hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest(),'C3_generator':1,'dimension_three_simple':E,'noninvertibles':rho,'m':m,'k':m//2,'FP_dimensions':list(map(str,dims)),'d_over_four_minpoly':str(mp.as_expr()),'conclusion':'excluded_by_two_dimension_divisibility_and_A4_field' if m==6 else 'excluded_by_A4_codegree_field' if m==12 else 'A4_reduction_only'})
 require(len(cases)==4,'Source coverage')
 forms=[];J=[[0,1],[1,0]]
 for a,b,c in itertools.product(range(2),repeat=3):
  C=[[a,b],[b,c]];ranks=[]
  for q in range(2):
   B=[[q*J[i][j] for j in range(2)]+C[i] for i in range(2)]+[C[i]+[q*J[i][j] for j in range(2)] for i in range(2)]
   ranks.append(rank2(B))
  require(set(ranks)=={2,4} or (C==[[0,0],[0,0]] and ranks==[0,4]),'Projective ranks')
  forms.append({'symmetric_cross_form':C,'ranks_for_two_algebra_twists':ranks})
 command=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(HERE/'verify_A4_quadratic.py'),'--repo',str(args.repo)]
 replay=subprocess.run(command,check=True,capture_output=True,text=True)
 a4=json.loads(replay.stdout);require(a4['status']=='PASS','A4 exact replay')
 result={'status':'PASS','cases':cases,'general_exclusion_inputs':3,'unresolved_reduction_inputs':1,'symmetric_V4_cross_forms':forms,'all_source_products':True,'all_module_products':True,'optimizer_used':False,'A4_classification_replay':a4}
 if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
