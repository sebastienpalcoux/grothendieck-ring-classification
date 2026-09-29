"""Exact half-E6 subcategory branching and twist-mass necessary condition.

The six distinguished twist classes have source x-masses d,2d,d,d,d+1,2d+3.
Conjugating all twists leaves this nonnegative moment system unchanged.
It combines Gram equations, full-character spectral integrality, and Galois
multiplicity balance. Discovery proposes integer Farkas rays; replay is exact.
"""
import json,itertools
from pathlib import Path
import sympy as s
from exact import require,vector,key,evaluate,VerificationError
from rings import Characters,validate
from induction import discover_roots,check_roots,restriction_columns,low_matrices,low_failure
from character_induction import CharacterTable,Ineligible
from spectral_induction import Spectrum
from round4_higher_fast import half_e6_subrings,half_e6_low_allowed
from round3_m4 import high_vectors
from higher_traces import farkas,check_farkas
ROOT=Path(__file__).resolve().parents[1]

def data_for(R):
 if not half_e6_subrings(R):raise Ineligible('no half-E6 based subcategory')
 validate(R);ch=Characters(R);f,K,ds,D,pD,emb=ch.fp()
 if f.degree()>4:raise Ineligible('FP field exceeds supported degree4')
 roots=discover_roots(ch.p,K)
 if roots is None:raise Ineligible('full character field not contained in FP field')
 check_roots(ch.p,K,roots);cr=discover_roots(ch.C.charpoly().as_poly(),K)
 if cr is None:raise Ineligible('codegrees outside FP field')
 check_roots(ch.C.charpoly().as_poly(),K,cr);rest=list(cr);rest.remove(D)
 cs=[restriction_columns(ds,D/r,K,ch.C)for r in rest];lows=low_matrices(cs,ch.C,gram_prune=True)
 tab=CharacterTable.__new__(CharacterTable);tab.n=len(R);tab.du=ch.du;tab.K=K;tab.seed=[]
 tab.rows=[tuple(evaluate(list(reversed(co)),r,K)for co in ch.coeff)for r in roots]
 tab.codegrees=[sum((row[i]*row[tab.du[i]]for i in range(len(R))),K.zero)for row in tab.rows]
 tab.ds=ds;tab.D=D;tab.fp=next(i for i,row in enumerate(tab.rows)if list(row)==ds)
 tab.dims={};tab.values={};tab.allowed={};tab.compatibility={};tab._automorphisms=discover_roots(f,K)
 require(tab._automorphisms is not None and len(tab._automorphisms)==f.degree(),'FP field is not Galois')
 return dict(ch=ch,K=K,ds=ds,D=D,embedding=emb,lows=lows,columns=cs,tab=tab)

def system(R,data,cols,g,x):
 K=data['K'];ds=data['ds'];D=data['D'];n=len(R);e=K.mod.degree();tab=data['tab']
 G,vs=high_vectors(data,cols);sp=Spectrum(tab,cols,[(v,None)for v in vs]);bad=set(map(tuple,sp.forbidden));vs=[v for v in vs if v not in bad]
 if sp.missing_low:return None,None,{'spectrum':sp.metadata()}
 labels=[(v,t)for v in vs for t in range(6)if(not v[g-1]and not v[x-1]and t==5)or(not v[g-1]and v[x-1]and t<4)or(v[g-1]>=v[x-1]and v[g-1]and t==4)]
 z={v:sum((K(v[i])*ds[i+1]for i in range(n-1)),K.zero)for v in vs};A=[];b=[]
 for i in range(n-1):
  for j in range(i,n-1):A.append([v[i]*v[j]for v,t in labels]);b.append(int(G[i,j]))
 dx=ds[x];DE=K(2)+dx*dx;targets=[dx,2*dx,dx,dx,dx+K.one]
 for t0,target in enumerate(targets):
  aa=s.Matrix.hstack(*(vector(K(v[x-1])*z[v]if t==t0 else K.zero,e)for v,t in labels));bb=vector(D/DE*target,e)
  for i in range(e):
   den=s.ilcm(*(a.q for a in list(aa[i,:])+[bb[i]]));A.append([int(a*den)for a in aa[i,:]]);b.append(int(bb[i]*den))
 rows,rhs=sp.balance(labels,len(labels),None);A+=rows;b+=rhs
 return A,b,{'spectrum':sp.metadata(),'labels':[[list(v),t]for v,t in labels],'variables':len(labels),'rows':len(A)}

def certificate(R,progress=None):
 data=data_for(R);tab=data['tab'];g,x=half_e6_subrings(R)[0];out={'kind':'half_e6_projection_mass','version':1,'scope':'pseudo_unitary','subring':[0,g,x],'column_counts':list(map(len,data['columns'])),'branches':[]}
 for ix,cols in enumerate(data['lows']):
  br={'columns':list(map(list,cols))};out['branches'].append(br)
  why=low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
  if why:br['ordinary']=why;continue
  if not half_e6_low_allowed(cols,g,x):br['low_branching_failure']=True;continue
  labs=tab.assignments(cols);br['labellings']=list(map(list,labs))
  if not labs:continue
  A,b,meta=system(R,data,cols,g,x);br['system']=meta
  if A is None:br['ray']=None;continue
  ray=farkas(A,b);br['ray']=ray
  if progress:progress(ix,meta,ray)
  if ray is None:return None,out
  check_farkas(A,b,ray)
 return out,out

def verify(R,c):
 require(c['kind']=='half_e6_projection_mass'and c['version']==1 and c['scope']=='pseudo_unitary','wrong half-E6 projection certificate')
 data=data_for(R);tab=data['tab'];g,x=half_e6_subrings(R)[0]
 require(c['subring']==[0,g,x]and c['column_counts']==list(map(len,data['columns'])),'wrong half-E6 subring or low domain')
 require(len(c['branches'])==len(data['lows']),'omitted low branch');rays=0
 for cols,br in zip(data['lows'],c['branches']):
  require(br['columns']==list(map(list,cols)),'wrong low frame')
  why=low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
  if why:require(br['ordinary']==why,'wrong ordinary rejection');continue
  if not half_e6_low_allowed(cols,g,x):require(br['low_branching_failure']is True,'wrong projection rejection');continue
  labs=tab.assignments(cols);require(br['labellings']==list(map(list,labs)),'omitted character labelling')
  if not labs:continue
  A,b,meta=system(R,data,cols,g,x);require(br['system']==meta,'wrong necessary system')
  if A is None:require(br['ray']is None,'unexpected spectral ray')
  else:check_farkas(A,b,br['ray']);rays+=1
 return {'passed':True,'low_frames':len(data['lows']),'rays':rays,'optimizer_used':False}

def add_verlinde(R,data,cols,lab,A,b,labels):
 K=data['K'];tab=data['tab'];n=len(R);vs=list(dict.fromkeys(tuple(v)for v,ti in labels));sp=Spectrum(tab,cols,[(v,None)for v in vs]);require(not sp.missing_low,'spectral domain lost a low column')
 tuples=dict(zip(sp.vectors,sp.types));nv=len(A[0]);nh=len(labels);triples={}
 from modular_character_induction import rational_rows
 for a,bb,c in itertools.combinations_with_replacement(range(1,n),3):
  ha,hb,hc=[lab[x]for x in(a,bb,c)];weights={v:tuples[v][ha]*tuples[v][hb]*tuples[v][hc]*tab.dims[v]**2/tab.D**2 for v in set(sp.vectors)};rhs=-sum((weights[v]for v in sp.low),K.zero)
  co=[weights[(0,)+tuple(v)]for v,ti in labels]+[K.zero]*(nv-nh)+[-K.one]
  for row in A:row.append(0)
  triples[(a,bb,c)]=nv;nv+=1
  for row,value in rational_rows(co,rhs,K):A.append(row);b.append(value)
 for a,bb in itertools.combinations_with_replacement(range(1,n),2):
  ca,cb=cols[a],cols[bb];fp=[sum(ca[i]*cb[j]*R[i][j][k]for i in range(n)for j in range(n))for k in range(n)];qvars={}
  for v in sp.high:
   bound=min(fp[k]//v[k]for k in range(n)if v[k])
   if bound:qvars[v]=(nv,bound);nv+=1
  for row in A:row.extend([0]*(nv-len(row)))
  for k in range(n):
   row=[0]*nv
   for c in range(1,n):row[triples[tuple(sorted((a,bb,c)))]]+=cols[c][k]
   for v,(j,B)in qvars.items():row[j]=v[k]
   A.append(row);b.append(fp[k]-int(a==bb and k==0))
  for v,(j,B)in qvars.items():
   row=[0]*(nv+1);row[j]=1;row[nv]=1
   for k,(w,ti)in enumerate(labels):
    if tuple(w)==v[1:]:row[k]-=B
   for rr in A:rr.append(0)
   A.append(row);b.append(0);nv+=1
 return A,b
