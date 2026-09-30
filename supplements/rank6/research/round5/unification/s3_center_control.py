"""Nonzero-word categorical control from D(S3), derived by finite group sums.

S is computed from centralizer characters; fusion is computed by exact
Verlinde. No fusion matrices or numerical optimization are supplied.
"""
import hashlib
import itertools
import json
import sys
from collections import Counter
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'software'))
from character_induction import CharacterTable
from exact import field,evaluate,require
from modular_character_induction import rational_rows
from round5_unified import low_word_data,joint_coefficient_domains,count_system
from round5_balancing import build_coupled


def main():
 C=field(s.Poly(s.cyclotomic_poly(6,s.Symbol('t')),s.Symbol('t')));z=C.unit
 conj=lambda x:evaluate(x.to_list(),z**5,C)
 group=list(itertools.permutations(range(3)));e=(0,1,2);t=(1,0,2);c=(1,2,0)
 mul=lambda a,b:tuple(a[b[i]] for i in range(3))
 inv=lambda a:tuple(a.index(i) for i in range(3))
 power=lambda a,k:e if k==0 else (a if k==1 else mul(a,a))
 reps=[e,t,c];centralizers=[[x for x in group if mul(g,x)==mul(x,g)] for g in reps]
 def chi(typ,k,x):
  require(x in centralizers[typ],'character evaluated outside centralizer')
  if typ==0:
   if k==0:return C.one
   if k==1:return C((-1)**sum(x[i]>x[j] for i in range(3) for j in range(i+1,3)))
   return C(sum(x[i]==i for i in range(3))-1)
  if typ==1:return C.one if x==e else C((-1)**k)
  r=next(j for j in range(3) if power(c,j)==x)
  return z**((2*k*r)%6)
 objects=[(0,0),(0,1),(0,2),(1,0),(1,1),(2,0),(2,1),(2,2)]
 S=[]
 for a,k in objects:
  g=reps[a];row=[]
  for b,l in objects:
   h=reps[b];value=C.zero
   for x in group:
    h1=mul(mul(x,h),inv(x))
    if mul(g,h1)!=mul(h1,g):continue
    g1=mul(mul(inv(x),g),x)
    value+=conj(chi(a,k,h1))*conj(chi(b,l,g1))
   row.append(value/C(len(centralizers[a])*len(centralizers[b])))
  S.append(row)
 dims=[int((C(6)*S[0][j]).to_list()[0]) for j in range(8)]
 require(dims==[1,1,2,3,3,2,2,2],'center dimensions')
 require(all(sum((S[i][k]*conj(S[j][k]) for k in range(8)),C.zero)==C(i==j)
             for i in range(8) for j in range(8)),'unitary character-sum S')
 N=[]
 for a in range(8):
  plane=[]
  for b in range(8):
   row=[]
   for d in range(8):
    v=sum((S[a][x]*S[b][x]*conj(S[d][x])/S[0][x] for x in range(8)),C.zero)
    co=v.to_list();require(len(co)<=1 and (not co or co[0].denominator==1),'integral Verlinde')
    q=int(co[0]) if co else 0;require(q>=0,'nonnegative Verlinde');row.append(q)
   plane.append(row)
  N.append(plane)
 theta=[chi(a,k,reps[a])/chi(a,k,e) for a,k in objects]
 dual=[next(b for b in range(8) if N[a][b][0]) for a in range(8)]
 require(all(sum((C(N[a][b][d])*C(dims[d])*theta[d] for d in range(8)),C.zero)
             ==theta[a]*theta[b]*C(6)*S[dual[a]][b]
             for a in range(8) for b in range(8)),'all-center ribbon equations')
 # Restriction multiplicities are finite centralizer character inner products.
 restrictions=[]
 for a,k in objects:
  v=[]
  for j in range(3):
   x=sum((chi(0,j,h)*conj(chi(a,k,h)) for h in centralizers[a]),C.zero)/C(len(centralizers[a]))
   co=x.to_list();require(len(co)<=1 and (not co or co[0].denominator==1),'integral restriction')
   v.append(int(co[0]) if co else 0)
  restrictions.append(v)
 require(restrictions==[[1,0,0],[0,1,0],[0,0,1],[1,0,1],[0,1,1],[1,1,0],[0,0,1],[0,0,1]],'induced restrictions')
 # Rep(S3) fusion is independently derived by its character inner products.
 def integer(x):
  co=x.to_list();require(len(co)<=1 and (not co or co[0].denominator==1),'exact integral character product')
  value=int(co[0]) if co else 0;require(value>=0,'nonnegative character product');return value
 R=[[[integer(sum((chi(0,i,h)*chi(0,j,h)*conj(chi(0,k,h)) for h in group),C.zero)/C(6))
       for k in range(3)] for j in range(3)] for i in range(3)]
 tab=CharacterTable.__new__(CharacterTable);tab.n=3;tab.du=[0,1,2];tab.K=C
 tab.rows=[tuple(chi(0,k,g) for k in range(3)) for g in reps]
 tab.codegrees=[C(6),C(2),C(3)];tab.ds=[C(1),C(1),C(2)];tab.D=C(6);tab.fp=0
 tab.dims={};tab.values={};tab.allowed={};tab.compatibility={};tab._automorphisms=[z,z**5]
 lows=[0,3,5];highs=[i for i in range(8) if i not in lows];cols=[restrictions[i] for i in lows]
 V=sorted(set(tuple(restrictions[i][1:]) for i in highs));counts=[sum(tuple(restrictions[i][1:])==v for i in highs) for v in V]
 words=[w for n in (2,3) for w in itertools.combinations_with_replacement(range(1,3),n)]
 data=dict(C=C,F=6,tab=tab,dims=tab.ds,DD=tab.D,phases=[(z**i,) for i in range(6)])
 wd=low_word_data(R,data,cols,V,counts,[0,1,2],words=words)
 products=[]
 for word in words:
  p=[1]+[0]*7
  for a in word:p=[sum(p[i]*N[i][lows[a]][j] for i in range(8)) for j in range(8)]
  products.append(p)
 require(wd['low_coefficients']==[[p[i] for i in lows] for p in products],'independent known low words')
 X=[[p[j] for p in products] for j in highs]
 require(wd['gram']==[[sum(x[i]*x[j] for x in X) for j in range(len(words))] for i in range(len(words))],'independent nonzero Gram')
 require(any(x for row in X for x in row),'nonzero high-word coefficients')
 domains=joint_coefficient_domains(wd,time_limit=30);require(domains['complete'] and not domains['impossible'],'complete joint domains')
 gram=count_system(wd,domains)
 actual=Counter((tuple(restrictions[j]),tuple(X[h])) for h,j in enumerate(highs))
 gp=[actual[(tuple(v),tuple(x))] for v,x in gram['labels']]
 require(sum(gp)==len(highs),'actual columns in exact domains')
 require(all(sum(gp[int(j)]*v for j,v in row.items())==b for row,b in zip(gram['rows'],gram['rhs'])),'count equations')
 labels=[(v,ti) for v in V for ti in range(6)];A=[];b=[]
 for v,ct in zip(V,counts):A.append([int(w==v) for w,ti in labels]);b.append(ct)
 def eigen(a,v):
  tab.prepare(v);return tab.D/tab.codegrees[a]*tab.values[a,tuple(v)]/tab.dims[tuple(v)]
 for a,bb in itertools.combinations_with_replacement(range(3),2):
  target=tab.D*C(dims[lows[a]])*tab.values[a,tuple(cols[bb])]-sum((C(dims[j]**2)*eigen(a,restrictions[j])*eigen(bb,restrictions[j]) for j in lows),C.zero)
  co=[tab.dims[(0,)+v]**2*eigen(a,(0,)+v)*eigen(bb,(0,)+v)*z**ti for v,ti in labels]
  for row,rhs in rational_rows(co,target,C):A.append(row);b.append(rhs)
 coupled=build_coupled(R,data,cols,[0,1,2],A,b,labels,list(range(len(labels))),[1]*len(labels),wd,domains)
 actual_phase=Counter((tuple(restrictions[j]),tuple(X[h]),next(t for t in range(6) if z**t==theta[j])) for h,j in enumerate(highs))
 point=[actual_phase[(tuple(coupled['coefficient_labels'][q][0]),tuple(coupled['coefficient_labels'][q][1]),t)] for q,t in coupled['labels']]
 require(sum(point)==len(highs),'actual refined columns present')
 require(all(sum(point[int(j)]*v for j,v in row.items())==rhs for row,rhs in zip(coupled['rows'],coupled['rhs'])),'exact coupled equations')
 balancing_start=len(A)+len(gram['rows']);balance_rows=coupled['rows'][balancing_start:];balance_rhs=coupled['rhs'][balancing_start:]
 require(balance_rows and any(balance_rhs),'nontrivial product balancing equations')
 collapsed=[0]*len(point)
 for (q,ti),value in zip(coupled['labels'],point):
  collapsed[coupled['labels'].index((q,0))]+=value
 failed=sum(sum(collapsed[int(j)]*v for j,v in row.items())!=rhs for row,rhs in zip(balance_rows,balance_rhs))
 require(failed>0,'replacing actual twists by one must violate product balancing')
 out=dict(passed=True,optimizer_used=False,optimized_python=not __debug__,category='Rep(S3)',center='D(S3)',
          modular_data_source='finite group centralizer character sum',fusion_source='exact Verlinde',center_simples=8,
          all_center_ribbon_equations=64,low_columns=cols,high_restrictions=[list(v) for v in V],profile_counts=counts,
          words=[list(w) for w in words],high_word_coefficients=X,joint_domains_complete=True,
          gram_count_rows=len(gram['rows']),coupled_rows=len(coupled['rows']),product_balancing_rows=len(balance_rows),
          refined_variables=len(point),all_twists_one_balancing_failures=failed,nonzero_refined_counts=[[i,v] for i,v in enumerate(point) if v],source_sha256={})
 for name in ['software/round5_unified.py','software/round5_balancing.py','research/round5/unification/s3_center_control.py']:
  out['source_sha256'][name]=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
 Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
