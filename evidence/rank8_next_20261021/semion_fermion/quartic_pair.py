"""Exact fourth-moment coupled restriction screen for R928 and R941.

Read-only with respect to all frozen inputs; stdout is the reproducible result.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations_with_replacement as cwr,product
import argparse,hashlib,json,math
import sympy as s
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
OLD=ROOT/'evidence/rank8_frontier_20261021';P=OLD/'quartic_integer_center'
Z=(F(0),)*4;ONE=(F(1),F(0),F(0),F(0))
def need(x,msg):
 if not x:raise ValueError(msg)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def scale(a,b):return tuple(x*b for x in a)
def mul(a,b):
 out=[F(0)]*4
 for i,x in enumerate(a):
  for j,y in enumerate(b):out[i^j]+=x*y*(2 if i&j&1 else 1)*(3 if i&j&2 else 1)
 return tuple(out)
def conj(a,u,v):return tuple(x*((-1)**((bool(i&1)*u+bool(i&2)*v)%2)) for i,x in enumerate(a))
def inv(a):
 z=mul(mul(conj(a,1,0),conj(a,0,1)),conj(a,1,1));n=mul(a,z);need(not any(n[1:]) and n[0],'field inverse');return scale(z,1/n[0])
def div(a,b):return mul(a,inv(b))
def fp(v,char):return tuple(sum(F(n)*ch[j] for n,ch in zip(v,char)) for j in range(4))
def read(p):return json.loads(p.read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def mj(X):return [[str(z) for z in row] for row in X.tolist()]
def main():
 source=read(P/'source.json');domain=read(P/'gram_cubic.json');need(domain['source_sha256']==digest(P/'source.json'),'source binding')
 pairs=list(cwr(range(1,5),2));quads=list(cwr(range(1,5),4));triples=list(cwr(range(1,5),3));out=[]
 for rec in source['records']:
  chars=[[tuple(map(F,x)) for x in ch] for ch in rec['full_characters']]; D=tuple(map(F,rec['formal_codegrees'][0])); ds=chars[0]
  lows=rec['low_columns'];highs=[(0,)+tuple(v) for v in rec['canonical_high_vectors']];cols=lows+highs
  beta=[scale(div(D,tuple(map(F,f))),F(1,n)) for f,n in zip(rec['formal_codegrees'],rec['irreducible_dimensions'])]
  vals=[[mul(b,fp(v,ch)) for b,ch in zip(beta,chars)]for v in cols];dims=[fp(v,ds)for v in cols]
  quartics=[]
  for quad in quads:
   coeff=[]
   for row,d in zip(vals,dims):
    z=ONE
    for e in quad:z=mul(z,row[e])
    coeff.append(div(z,mul(mul(d,d),mul(D,D))))
   coeff=[tuple(sum(z[j]for z in coeff[:5])for j in range(4))]+coeff[5:]
   den=math.lcm(*(x.denominator for z in coeff for x in z));quartics.append(([[int(x*den) for x in z]for z in coeff],den))
  cubicforms=[]
  for t in rec['low_cubic_equations']:
   cs=[list(map(F,t['constant']))]+[list(map(F,v))for v in t['coefficients']];den=math.lcm(*(x.denominator for z in cs for x in z));cubicforms.append(([[int(x*den)for x in z]for z in cs],den))
  V=s.Matrix.hstack(*(s.Matrix(v)for v in highs));counts0=domain['patterns'][0];Q=V*s.diag(*counts0)*V.T;ind=list(Q.rref()[1]);Qb=Q.extract(ind,ind);Qinv=Qb.inv();groups={};fail=[];remain=[]
  for ix,counts in enumerate(domain['patterns']):
   cubic=[]
   for co,den in cubicforms:
    v=[sum(n*z[j]for n,z in zip([1]+counts,co))for j in range(4)];need(not any(v[1:]) and v[0]%den==0 and v[0]>=0,'cubic');cubic.append(v[0]//den)
   moments=[];why=None
   for quad,(co,den)in zip(quads,quartics):
    v=[sum(n*z[j]for n,z in zip([1]+counts,co))for j in range(4)]
    if any(v[1:]) or v[0]%den or v[0]<0:why={'reason':'nonintegral_or_negative_fourth_moment','quad':quad,'coordinates':[str(F(x,den))for x in v]};break
    moments.append(v[0]//den)
   if why:fail.append(dict(index=ix,**why));continue
   key=(tuple(cubic),tuple(moments))
   if key not in groups:
    low=dict(zip(triples,cubic));four=dict(zip(quads,moments))
    G=s.Matrix(10,10,lambda p,q:four[tuple(sorted(pairs[p]+pairs[q]))]-int(pairs[p][0]==pairs[p][1])*int(pairs[q][0]==pairs[q][1])-sum(low[tuple(sorted(pairs[p]+(e,)))]*low[tuple(sorted(pairs[q]+(e,)))]for e in range(1,5)))
    R=rec['tensor'];T=s.Matrix(8,10,lambda k,p:sum(lows[pairs[p][0]][u]*lows[pairs[p][1]][v]*R[u][v][k]for u in range(8)for v in range(8))-int(pairs[p][0]==pairs[p][1]and k==0)-sum(low[tuple(sorted(pairs[p]+(e,)))]*lows[e][k]for e in range(1,5)))
    C=Qinv*T[ind,:];need(Q[:,ind]*C==T,'restriction consistency');X=V[ind,:].T*C;H=G-C.T*Qb*C
    groups[key]={'group':len(groups),'indices':[],'G':mj(G),'H':mj(H),'T':mj(T),'Xtypes':mj(X),'Qrank':Q.rank(),'Grank':G.rank(),'Hrank':H.rank(),'H_psd':bool(H.is_positive_semidefinite)}
   group=groups[key];group['indices'].append(ix)
   if not group['H_psd']:fail.append({'index':ix,'group':group['group'],'reason':'nonpositive_residual_Gram'})
   elif sum(counts)-len(ind)<group['Hrank']:fail.append({'index':ix,'group':group['group'],'reason':'insufficient_kernel_dimension'})
   else:remain.append(ix)
  out.append({'id':rec['id'],'tensor_sha256':rec['tensor_sha256'],'domain':len(domain['patterns']),'pairs':pairs,'quartics':quads,'restriction_rank':len(ind),'groups':list(groups.values()),'failures':fail,'survivors':remain})
 result={'kind':'coupled_fourth_moment_restriction_Gram','records':out,'source_sha256':{str(p.relative_to(ROOT)):digest(p)for p in [P/'source.json',P/'gram_cubic.json']},'verifier_sha256':digest(Path(__file__)),'scope':'Necessary center constraints only; a survivor is not a category.'}
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
