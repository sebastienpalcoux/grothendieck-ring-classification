"""Construct generalized TY categories via Liptrap Theorem 4, root-of-unity phase witnesses.
All indices in original input basis. χ, υ, τ per arXiv:1002.3166v2 Def 4.3.
Only affirmative witnesses are claimed: failed finite-order searches do not exclude.
"""
from pathlib import Path
import json,itertools,collections,time
import numpy as np
ROOT=Path(__file__).resolve().parents[2]

def solve_mod_batch(A,B,q=16):
 A=A.copy()%q;B=B.copy()%q;m,n=A.shape;T=np.eye(n,dtype=np.int64);r=0
 while r<min(m,n):
  W=A[r:,r:];nz=np.argwhere(W)
  if not len(nz):break
  vals=W[W!=0];vs=(vals&-vals);v=vs.min();p=nz[np.flatnonzero(vs==v)[0]];i,j=map(int,p+np.array([r,r]));d=int(v)
  if i!=r:A[[r,i]]=A[[i,r]];B[[r,i]]=B[[i,r]]
  if j!=r:A[:,[r,j]]=A[:,[j,r]];T[:,[r,j]]=T[:,[j,r]]
  inv=pow(int(A[r,r])//d,-1,q)
  A[r]=(A[r]*inv)%q;B[r]=(B[r]*inv)%q
  assert A[r,r]==d
  ids=np.flatnonzero(A[r+1:,r])+r+1
  for i in ids:
   coeff=int(A[i,r])//d;A[i]=(A[i]-coeff*A[r])%q;B[i]=(B[i]-coeff*B[r])%q
  ids=np.flatnonzero(A[r,r+1:])+r+1
  for j in ids:
   coeff=int(A[r,j])//d;A[:,j]=(A[:,j]-coeff*A[:,r])%q;T[:,j]=(T[:,j]-coeff*T[:,r])%q
  r+=1
 good=np.all(B[r:]==0,axis=0)
 for i in range(r):good&=(B[i]%A[i,i]==0)
 sols=[]
 for c in np.flatnonzero(good):
  y=np.zeros(n,dtype=np.int64)
  for i in range(r):y[i]=B[i,c]//A[i,i]
  sols.append((int(c),(T@y)%q))
 return sols

def character_forms(mult,inds,q):
 h=len(inds);idx={a:i for i,a in enumerate(inds)};T=[[idx[mult[a,b]] for b in inds] for a in inds]
 chars=[]
 for vals in itertools.product(range(0,q,q//h),repeat=h-1):
  c=(0,)+vals
  if all(c[T[i][j]]==(c[i]+c[j])%q for i in range(h) for j in range(h)):chars.append(c)
 assert len(chars)==h
 forms=[]
 for rows in itertools.product(chars,repeat=h-1):
  B=((0,)*h,)+rows
  if len(set(B))<h:continue
  if not all(B[i][j]==B[j][i] for i in range(h) for j in range(h)):continue
  if not all(B[T[i][j]][k]==(B[i][k]+B[j][k])%q for i in range(h) for j in range(h) for k in range(h)):continue
  forms.append(B)
 return forms

def construct(N,q=16):
 n=len(N);dual=np.argmax(N[:,:,0],axis=1).tolist();S=[i for i in range(n) if N[i,dual[i]].sum()==1];M=[i for i in range(n) if i not in S]
 if len(M)!=2:return None
 if any(N[m,l,k] for m in M for l in M for k in M):return None
 mul={(a,b):int(np.argmax(N[a,b])) for a in S for b in range(n)}
 mul.update({(a,b):int(np.argmax(N[a,b])) for a in range(n) for b in S})
 H=[a for a in S if mul[a,M[0]]==M[0]]
 if len(H)!=4:return None
 if any(mul[a,b]!=mul[b,a] for a in H for b in H):return None
 # Normalize χ and υ at identity arguments; all other phases variables.
 keys=[(f,a,b,m) for f in ('chi','upsilon') for a in S if a!=0 for b in S if b!=0 for m in M];ki={k:i for i,k in enumerate(keys)}
 eqs=[]
 def row(terms):
  r=np.zeros(len(keys),dtype=np.int64)
  for coeff,key in terms:
   if key in ki:r[ki[key]]+=coeff
  return r
 # barχ(b,a)(m)=χ(a,b)(a m b), since τ chosen constant.
 for a,b,m in itertools.product(S,S,M):
  eqs.append(row([(1,('chi',b,a,dual[m])),(-1,('chi',a,b,mul[mul[a,m],b]))]))
 # υ(a,b)(m)/υ(a,b)(m c^-1) χ(ab,c)(m) = χ(a,c)(m) χ(b,c)(a^-1 m)
 for a,b,c,m in itertools.product(S,S,S,M):
  eqs.append(row([(1,('upsilon',a,b,m)),(-1,('upsilon',a,b,mul[m,dual[c]])),(1,('chi',mul[a,b],c,m)),(-1,('chi',a,c,m)),(-1,('chi',b,c,mul[dual[a],m]))]))
 base=len(eqs);forms=character_forms(mul,H,q);pairs=list(itertools.product(forms,repeat=2));B=np.zeros((len(eqs)+2*len(H)**2,len(pairs)),dtype=np.int64)
 for im,m in enumerate(M):
  for ia,a in enumerate(H):
   for ib,b in enumerate(H):
    eqs.append(row([(1,('chi',a,b,m))]));B[len(eqs)-1]=[pair[im][ia][ib] for pair in pairs]
 A=np.array(eqs,dtype=np.int64);keep=np.any(A,axis=1)|np.any(B,axis=1);A=A[keep];B=B[keep]
 sol=solve_mod_batch(A,B,q)
 if not sol:return {'found':False,'modulus':q,'rows':len(A),'variables':len(keys),'forms':len(forms)}
 j,x=sol[0];assert np.all((A@x-B[:,j])%q==0)
 return {'found':True,'modulus':q,'serfs':S,'lords':M,'stabilizer':H,'tau_squared':'1/4','tau':'1/2','phase_values':[list(k)+[int(x[i])] for i,k in enumerate(keys)],'forms':pairs[j],'reference':'Liptrap arXiv:1002.3166v2 Definition 4.3 and Theorem 4'}

def main():
 D=json.load(open(ROOT/'work/input_audit/tensors.json'));results={};start=time.time()
 for id,t in D.items():
  if not id.startswith('R10'):continue
  r=construct(np.array(t,dtype=np.int64))
  if r is not None:
   results[id]=r;print(id,{k:v for k,v in r.items() if k not in ['phase_values','forms']},flush=True)
 (ROOT/'work/literature/gty_liptrap_certificates.json').write_text(json.dumps(results,indent=2)+'\n');print('Elapsed',time.time()-start)
if __name__=='__main__':main()
