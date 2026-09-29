"""Exploratory reconstruction of GI2022 Theorem6.8 m=2, Example6.10.
This creates a full modular datum; existence of target restriction functor is NOT asserted.
"""
from pathlib import Path
import numpy as np,json,itertools
ROOT=Path(__file__).resolve().parents[2]
r=np.sqrt(17);a=.25;b=1/r
labels=[('0',),('pi',),('sig',0,1),('sig',2,1),('phi',1),('phi',-1)]+[('sig',1,k) for k in range(4)]+[('xi',j) for j in range(1,9)]+[('psi',e,f) for e,f in itertools.product([1,-1],repeat=2)]
def sij(v,w):
 if labels.index(v)>labels.index(w):return sij(w,v)
 if v==('0',):
  return (a-b)/2 if w==('0',) else (a+b)/2 if w==('pi',) else a if w[0]=='sig' else b if w[0]=='xi' else a/2
 if v==('pi',):return (a-b)/2 if w==('pi',) else a if w[0]=='sig' else -b if w[0]=='xi' else a/2
 if v[0]=='sig':
  if w[0]=='sig':
   _,g,k=v;_,h,l=w;return 2*a*np.cos((g*h+g*l+h*k)*np.pi/2)
  if w[0]=='phi':return (-1)**v[1]*a
  if w[0]=='psi':return w[1]**v[1]*(-1)**v[2]*a
  return 0
 if v[0]=='phi':
  if w[0]=='phi':return (a+v[1]*w[1])/2
  if w[0]=='sig':return (-1)**w[1]*a
  if w[0]=='psi':return a/2
  return 0
 if v[0]=='xi':return -2*b*np.cos(12*np.pi*v[1]*w[1]/17) if w[0]=='xi' else 0
 if v[0]=='psi' and w[0]=='psi':return a/2-v[2]*w[2]*(v[1]==w[1])/2
 raise ValueError((v,w))
S=np.array([[sij(v,w) for w in labels] for v in labels]);T=np.array([1 if v[0] in ['0','pi','phi'] else np.exp(2j*np.pi*(v[1]**2+2*v[1]*v[2])/8) if v[0]=='sig' else np.exp(2j*np.pi*3*v[1]**2/17) if v[0]=='xi' else -1 for v in labels])
print('S2',abs(S@S-np.eye(22)).max(),'STS',abs((S*T)@S-(S/T).T/T).max())
NN=np.einsum('al,bl,cl,l->abc',S,S,S,1/S[0]);N=np.rint(NN).astype(int);print('Verlinde',abs(NN-N).max(),'min',N.min())
R=np.array(next(r for r in json.loads((ROOT/'data/census.json').read_text()) if r['id']=='R6_3_215')['N']);low=json.loads((ROOT/'systems/integral_frontier_215.json').read_text())['columns'];F=np.array(low+[[0,0,2,2,1,3]]*4+[[0,0,2,2,2,2]]*8+[[0,1,1,1,1,1]]*4)
err=np.einsum('abc,ck->abk',N,F)-np.einsum('ai,bj,ijk->abk',F,F,R);print('restriction',abs(err).max(),'mismatches',np.count_nonzero(err))
np.save(Path(__file__).with_name('cyclic8_S.npy'),S)
Path(__file__).with_name('cyclic8_center_tensor_exploratory.json').write_text(json.dumps({'labels':labels,'N':N.tolist(),'F':F.tolist(),'status':'numerical discovery, exact verification pending'})+'\n')
ds=S[0]/S[0,0];D=1/S[0,0]
FS2=np.einsum('ija,i,j,i,j->a',N,ds,ds,T**2,T**-2)/D**2
print('FS2',[(labels[a],complex(round(v.real,8),round(v.imag,8))) for a,v in enumerate(FS2)])
