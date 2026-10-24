"""Joint integer-center-column relaxation, avoiding separate low-frame enumeration.

Exact integral input and output ray validation. SciPy only proposes separators.
The trace set is exhaustive in orders, by the established Ramanujan-sum theorem.
"""
import sys,json,math,itertools,time,subprocess,hashlib
from pathlib import Path
from collections import Counter
from fractions import Fraction as Q
import sympy as s
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csc_matrix,hstack,vstack
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'sources'))
from rings import Characters
from higher_traces import trace_types,indicator_choices

def inputs(rid):
 C=json.load(open(ROOT/'work/verification_corpus.json'))['tensors'];return C[rid]
def columns(R,ds,D,B):
 inv=B.inv();den=int(s.ilcm(*[a.q for a in inv]));A=[int(a*den)for a in inv]
 assert len(R)**2*max(map(abs,A))*max(map(int,B.diagonal()))<2**120
 assert max(map(abs,A+[den]))<2**60
 src=Path(__file__).with_name('center_vectors.cpp');exe=src.with_suffix('')
 if not exe.exists() or exe.stat().st_mtime<src.stat().st_mtime:subprocess.run(['g++','-O3','-std=c++17',str(src),'-o',str(exe)],check=True)
 vals=[len(R),D]+ds+list(map(int,B))+A+[den]
 p=subprocess.run([str(exe)],input=' '.join(map(str,vals)),text=True,capture_output=True,check=True,timeout=90)
 return [tuple(map(int,line.split()))for line in p.stdout.splitlines()]
def modular_integral_columns(cs,a,D):
 """Spectrum of (D/dim(v))*C^{-1}*N_v must consist of algebraic integers."""
 import flint
 inv=a.C.inv();den=int(s.ilcm(*[x.q for x in inv]));J=inv*den
 ops=[list(map(int,J*N))for N in a.N];n=len(a.N);keep=[]
 for x in cs:
  v,z=x[:-1],x[-1];num=[sum(v[i]*ops[i][j]for i in range(n))*D for j in range(n*n)];dd=den*z
  M=flint.fmpq_mat(n,n,[flint.fmpq(t,dd)for t in num]);p=M.charpoly()
  if all(c.denominator==1 for c in p):keep.append(x)
 return keep
def data(R,height=6,modular=False):
 n=len(R);assert all(R[i][j]==R[j][i]for i in range(n)for j in range(n));a=Characters(R);f,K,ds0,D0,pD,emb=a.fp();assert f.degree()==1
 ds=[int(s.Rational(str(x.to_list()[0])))for x in ds0];D=sum(x*x for x in ds);B=a.C
 roots=a.C.eigenvals();assert all(x.is_Integer for x in roots)
 counts=Counter({D//int(r):int(m)for r,m in roots.items()});assert all(D%int(r)==0 for r in roots)
 cs=columns(R,ds,D,B);cs=[x for x in cs if x[0]==0 or x[-1]in counts];unpruned=len(cs)
 if modular:cs=modular_integral_columns(cs,a,D)
 ts,bound=trace_types(1,list(map(int,s.factorint(D))),height);ts=[tuple(x[0]for x in t)for t in ts]
 ij=list(itertools.combinations_with_replacement(range(n),2));rows=[('gram',i,j)for i,j in ij]
 rhs=[Q(int(B[i,j]))for i,j in ij]
 for z,num in sorted(counts.items()):rows.append(('low',z));rhs.append(Q(num))
 for i in range(1,n):rows.append(('moment1',i));rhs.append(Q(0))
 # Indicator +1 is forced by odd occurrences in any X X*.
 known={i:(0 if a.du[i]!=i else 1 if any(R[j][a.du[j]][i]%2 for j in range(n))else None)for i in range(1,n)}
 slacks=[]
 for i in range(1,n):
  if known[i] is not None:rows.append(('moment2',i));rhs.append(Q(D*known[i]))
  else:
   for sign in [1,-1]:rows.append(('moment2bound',i,sign));rhs.append(Q(D));slacks.append(len(rows)-1)
 H={}
 for i in range(1,n):
  pow=[int(k==0)for k in range(n)]
  for j in range(1,height+1):
   pow=[sum(pow[a]*R[a][i][b]for a in range(n))for b in range(n)];H[i,j]=pow[0]
 for j in range(3,height+1):
  for i in range(1,n):
   for sign in [1,-1]:
    rows.append(('higher',i,j,sign));rhs.append(Q(D*H[i,j],1 if sign==1 else min(map(int,s.factorint(j)))-1));slacks.append(len(rows)-1)
 trace_den=math.lcm(*(x.denominator for t in ts for x in t),*(r.denominator for r in rhs))
 mats=[];labels=[]
 for x in cs:
  v,z=x[:-1],x[-1]
  for ti,t in ([(-1,(Q(1),)*height)]if v[0]else enumerate(ts)):
   out=[]
   for row in rows:
    if row[0]=='gram':val=v[row[1]]*v[row[2]]
    elif row[0]=='low':val=int(v[0]and z==row[1])
    elif row[0]=='moment1':val=z*v[row[1]]*t[0]
    elif row[0]=='moment2':val=z*v[row[1]]*t[1]
    elif row[0]=='moment2bound':val=row[2]*z*v[row[1]]*t[1]
    else:val=row[3]*z*v[row[1]]*t[row[2]-1]
    out.append(int(val)if row[0]in ('gram','low')else int(val*trace_den))
   mats.append(out);labels.append([list(v),z,ti])
 for row in slacks:
  out=[0]*len(rows);out[row]=1;mats.append(out);labels.append(['slack',row])
 A=[];b=[]
 for i in range(len(rows)):
  den=1 if rows[i][0]in ('gram','low')else trace_den;line=[v[i]for v in mats];bb=int(rhs[i]*den);g=math.gcd(bb,*line)or 1;A.append([x//g for x in line]);b.append(bb//g)
 return A,b,{'dimensions':ds,'D':D,'rows':rows,'candidate_columns':len(cs),'unpruned_columns':unpruned,'modular_integrality':modular,'variables':len(mats),'trace_types':len(ts),'trace_order_bound':bound,'height':height,'labels':labels,'known_second_indicators':known}

def exact_separator(A,b,timeout=60):
 aa=np.array(A,dtype=float);bb=np.array(b,dtype=float);m=len(b)
 scale=np.maximum(1,np.maximum(np.max(abs(aa),axis=1),abs(bb)));mat=csc_matrix(aa/scale[:,None]);rhs=bb/scale
 sol=linprog(np.ones(2*m),A_ub=vstack([hstack([-mat.T,mat.T]),csc_matrix(np.r_[rhs,-rhs][None,:])]),b_ub=np.r_[np.zeros(aa.shape[1]),-1.],bounds=(0,None),method='highs',options={'time_limit':timeout})
 if not sol.success:return None,{'status':int(sol.status),'message':sol.message}
 y=(sol.x[:m]-sol.x[m:])/scale;y/=max(abs(y));support=np.flatnonzero(abs(y)>1e-9).tolist()
 # Rationalize directly first; exact verification is mandatory.
 for bound in [1000,10000,1000000,10**9]:
  vals=[Q(float(x)).limit_denominator(bound)for x in y];den=math.lcm(*(x.denominator for x in vals));out=[int(x*den)for x in vals]
  if verify_ray(A,b,out):return out,{'status':0,'rationalization':bound}
 for threshold in (1e-8,1e-7,1e-6):
  active=np.flatnonzero(abs(aa.T@y)<threshold).tolist();C=s.Matrix([[A[i][j]for i in support]for j in active]+[[b[i]for i in support]])
  target=s.zeros(C.rows,1);target[-1]=-1;rr,piv=C.row_join(target).rref()
  if len(piv)!=len(support)or(piv and piv[-1]>=len(support)):continue
  vv=[rr[i,-1]for i in range(len(support))];den=math.lcm(*(int(z.q)for z in vv));out=[0]*m
  for i,z in zip(support,vv):out[i]=int(z*den)
  g=math.gcd(*out);out=[z//g for z in out]
  if verify_ray(A,b,out):return out,{'status':0,'exact_rref':True}
 return None,{'status':'no_exact_ray'}
def verify_ray(A,b,y):
 return len(y)==len(b)and all(type(x)is int for x in y)and sum(x*z for x,z in zip(b,y))<0 and all(sum(row[j]*yi for row,yi in zip(A,y))>=0 for j in range(len(A[0])))
def run(rid,height=4,modular=False):
 start=time.time();R=inputs(rid);A,b,meta=data(R,height,modular);print(rid,'system',len(b),len(A[0]),meta['candidate_columns'],flush=True)
 y,why=exact_separator(A,b);meta.pop('labels');out={'id':rid,'outcome':'excluded'if y else 'no_conclusion','kind':'joint_integral_center_columns','metadata':meta,'ray':y,'solver_report':why,'seconds':time.time()-start}
 out['tensor_sha256']=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
 Path(__file__).with_name(rid+(''if height==4 else f'_h{height}')+('_modular_center.json'if modular else'_center.json')).write_text(json.dumps(out,indent=2)+'\n');print(rid,out['outcome'],out['seconds'],flush=True)
if __name__=='__main__':run(sys.argv[1],int(sys.argv[2])if len(sys.argv)>2 else 4,'--modular'in sys.argv)
