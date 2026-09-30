"""Exact light checks for the forced R155 spectrum; no existence claim."""
from pathlib import Path
import argparse,sys,runpy,contextlib,io,json,math,itertools,time
import numpy as np
import sympy as sp
from functools import lru_cache
HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--output',type=Path)
args=ap.parse_args()
def require(ok,message):
 if not ok:raise ValueError(message)
sys.argv=[str(HERE/'verify_forced_twists.py')]
with contextlib.redirect_stdout(io.StringIO()):
 ns=runpy.run_path(str(HERE/'verify_forced_twists.py'))
globals().update({k:ns[k] for k in ['C','M','dat','tab','lab','W','dims','DB','d','bd','Na','Nb','roots','exps','R']})
S=[]
for a in range(6):
 dl=sum((C(t)*dd for t,dd in zip(dat['lows'][6][a],dat['dims'])),C.zero)
 S.append([dl*tab.values[lab[a],v] for v in W])
idx=[1,23,25,24,18,19];dual=[0,1,2,3,5,4];tw=[0,0,0,18,18,18]
dualC=[next(j for j in range(6)if R[i][j][0])for i in range(6)]
for v in W:
 vd=tuple(v[dualC[j]]for j in range(6));tab.prepare(vd)
 require(tab.values[lab[4],vd]==tab.values[lab[5],v],'Character duality')
require(any(S[4][j]!=S[5][j]for j in range(26)),'Nonreal character rows distinct')
for name,N in [('a',Na),('b',Nb)]:
 for x in range(6):
  for y in range(6):
   vv=sum((C(N[i][j])*S[x][i]*S[y][j]/DB*roots[(exps[i]-exps[j])%24]for i in range(26)for j in range(26)if N[i][j]),C.zero)
   expected=C(N[idx[x]][idx[dual[y]]])*roots[(tw[y]-tw[x])%24]
   require(vv==expected,'Degree-one generalized indicator normalization')
@lru_cache(None)
def matpow(name,r):return np.linalg.matrix_power(np.array(Na if name=='a'else Nb,dtype=object),r)
weights={(x,y):[[S[x][i]*S[y][j]/DB for j in range(26)]for i in range(26)]for x in range(6)for y in range(6)}
@lru_cache(None)
def coeffs(name,r,x,y):
 N=matpow(name,r);out=[C.zero]*24
 for i in range(26):
  for j in range(26):
   if N[i,j]:out[(exps[i]-exps[j])%24]+=int(N[i,j])*weights[x,y][i][j]
 return out
@lru_cache(None)
def ind(name,r,q,x,y):return sum((v*roots[(q*k)%24] for k,v in enumerate(coeffs(name,r,x,y))),C.zero)
@lru_cache(None)
def extension(L):
 z=sp.Symbol('z');K=sp.QQ.alg_field_from_poly(sp.Poly(sp.cyclotomic_poly(L,z),z),alias='z');return K
@lru_cache(None)
def mapped(v,L):
 K=extension(L);return M.evaluate(v.to_list(),K.unit**(L//24),K)
@lru_cache(None)
def sigma(v,L,ell):
 K=extension(L);return M.evaluate(v.to_list(),K.unit**ell,K)
@lru_cache(None)
def unit_lift(kk,q,L):return next(j for j in range(1,L)if math.gcd(j,L)==1 and(j-kk)%q==0)
results=[]
for name in ['a','b']:
 for n in range(2,25):
  for x in range(6):
   for y in range(6):
    H=int(matpow(name,n)[idx[x],idx[dual[y]]]);Delta=tw[y]-tw[x]
    L=math.lcm(24,4*n if Delta else n);K=extension(L);zz=K.unit;tr=[K(H)]
    for k in range(1,n):
     g=math.gcd(n,k);q=n//g;kk=k//g
     v=mapped(ind(name,g,q,x,y),L)
     phase=(Delta*L)//(24*q)
     require((Delta*L)%(24*q)==0,'Exact phase denominator')
     v*=zz**((-phase)%L)
     tr.append(sigma(v,L,unit_lift(kk,q,L)))
    mult=[sum((tr[k]*zz**((-j*k*(L//n))%L)for k in range(n)),K.zero)/K(n)for j in range(n)]
    ok=all(len(z.to_list())<=1 and(not z or z.to_list()[0].denominator==1 and z.to_list()[0]>=0)for z in mult)
    row={'simple':name,'n':n,'insertion':[x,y],'dimension':H,'passed':ok}
    if not ok:row['trace1']=str(K.to_sympy(tr[1]));row['multiplicities']=[str(z)for z in mult]
    results.append(row)
    require(ok,'Generalized cyclic multiplicity '+str(row))
f=list(range(26))
for a,b in [(0,1),(2,3),(5,6),(8,9),(10,11),(12,13),(14,15),(16,18),(17,19),(22,23)]:f[a]=b;f[b]=a
Nf=np.zeros((26,26),dtype=object)
for a,b in enumerate(f):Nf[a,b]=1
AA=np.array(Na,dtype=object); BB=np.array(Nb,dtype=object)
require(np.array_equal(Nf@BB,BB),'Fermion action on L')
NN={1:np.eye(26,dtype=object),0:Nf,23:AA,22:Nf@AA,25:BB}
fail=[]
for a,b,c,e in itertools.product(NN,repeat=4):
 ab,ce,ac,be,ae,bc=[NN[x][y]for x,y in [(a,b),(c,e),(a,c),(b,e),(a,e),(b,c)]]
 H=sum(int(x*y)for x,y in zip(ab,ce))
 lhs=(exps[a]+exps[b]+exps[c]+exps[e])*H
 rhs=sum(exps[j]*int(ab[j]*ce[j]+ac[j]*be[j]+ae[j]*bc[j])for j in range(26))
 if (lhs-rhs)%24:fail.append([a,b,c,e,(lhs-rhs)%24])

require(not fail,'Low Vafa equations failed')
out={'passed':True,'scope':'necessary partial-data checks, not modular data or categorification','profile':296,'generalized_rotation_blocks':len(results),'low_vafa_equations':len(NN)**4,'degree_one_normalizations':72,'forced_dual_pairs_in_B':[[16,17],[18,19]],'remaining_duality_patterns':4,'possible_selfdual_counts_center':[20,24,28],'optimizer_used':False}
if args.output:args.output.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
