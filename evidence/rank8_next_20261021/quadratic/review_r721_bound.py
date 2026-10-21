"""Independent exact reconstruction of R721 dual multiplicity inequalities.
Imports no discovery/producer module. Source tensor and induction rows come
only from the separately derived bimodule-rank receipt.
"""
from pathlib import Path
import json,itertools,hashlib
from fractions import Fraction as F
import sympy as s
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];NEXT=HERE.parent

def need(b,msg):
 if not b:raise ValueError(msg)
def pmul(a,b):return(a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0]+3*a[1]*b[1])
def pdiv(a,b):
 # alpha conjugate is3-alpha; norm(b)=b0²+3b0b1-2b1².
 conjugate=(b[0]+3*b[1],-b[1]);den=pmul(b,conjugate);need(den[1]==0 and den[0]!=0,'quadratic norm');v=pmul(a,conjugate);return tuple(F(x,den[0])for x in v)
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run():
 rankpath=NEXT/'semion_fermion/construction/r721_bimodule_rank.json';proofpath=NEXT/'models/r721_dual_multiplicity_bound.json';src=json.loads(rankpath.read_text());proof=json.loads(proofpath.read_text());N=src['source_fusion_tensor'];avec=src['algebra_object'];need(avec==[1,0,0,0,1,0,0,0],'actual algebra source')
 factor=next(x for x in src['factors']if x['rank']==8);raw=factor['forgetful_rows'];sd=[(1,0)]*4+[(1,2)]*4;ad=tuple(sum(n*d[k]for n,d in zip(avec,sd))for k in (0,1));rawdim=[pdiv(tuple(sum(n*d[k]for n,d in zip(v,sd))for k in (0,1)),ad)for v in raw]
 for i,j in itertools.product(range(8),repeat=2):need(pmul(sd[i],sd[j])==tuple(sum(N[i][j][k]*sd[k][q]for k in range(8))for q in(0,1)),'source FP homomorphism')
 dims=[(1,0),(0,1),(0,1),(1,1),(1,1),(1,2),(0,2),(2,2)];unused=set(range(8));order=[]
 for d in dims:
  ix=min(j for j in unused if rawdim[j]==d);order.append(ix);unused.remove(ix)
 B=s.Matrix([raw[j]for j in order]).T;need(B[:,0]==s.Matrix(avec),'unit forgetful column');need(B*B.T==s.Matrix(src['free_bimodule_Gram']),'induction Gram source')
 proofby={(bool(p['dual_a']),bool(p['dual_b'])):p for p in proof};need(len(proof)==len(proofby)==4,'complete four duality certificates');triples=list(itertools.product(range(8),repeat=3));output=[]
 # All equality systems are generated afresh, with a different equation order
 # and a union-find orbit implementation instead of the producer BFS.
 for swap_a,swap_b in itertools.product((False,True),repeat=2):
  dual=list(range(8))
  if swap_a:dual[1],dual[2]=2,1
  if swap_b:dual[3],dual[4]=4,3
  parent=list(range(512))
  def encode(t):return(t[0]*8+t[1])*8+t[2]
  def find(x):
   while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
   return x
  def join(a,b):
   x,y=find(encode(a)),find(encode(b))
   if x!=y:parent[max(x,y)]=min(x,y)
  for i,j,k in triples:
   for t in ((dual[i],k,j),(k,dual[j],i),(dual[j],dual[i],dual[k])):join((i,j,k),t)
  blocks={}
  for t in triples:blocks.setdefault(find(encode(t)),[]).append(t)
  orbits=sorted(blocks.values(),key=lambda b:b[0]);loc={t:q for q,block in enumerate(orbits)for t in block};n=len(orbits);equations=[]
  def add(terms,rhs):
   row=[0]*(n+1)
   for t,c in terms:row[loc[t]]+=int(c)
   row[n]=int(rhs);equations.append(row)
  # AXA tensor_A AYA = A(XAY)A; calculate XAY by two direct products.
  for i,j in itertools.product(range(8),repeat=2):
   middle=[sum(avec[a]*N[i][a][u]*N[u][j][v]for a in range(8)for u in range(8))for v in range(8)]
   for z in range(8):add([((x,y,z),B[i,x]*B[j,y])for x,y in itertools.product(range(8),repeat=2)],sum(middle[v]*B[v,z]for v in range(8)))
  for i,j,k in triples:
   if i==0:add([((i,j,k),1)],int(j==k))
   if j==0:add([((i,j,k),1)],int(i==k))
   if k==0:add([((i,j,k),1)],int(j==dual[i]))
  for i,j in itertools.product(range(8),repeat=2):
   d=pmul(dims[i],dims[j])
   for q in (0,1):add([((i,j,k),dims[k][q])for k in range(8)],d[q])
  E=s.Matrix(equations);R,piv=E.rref();need(n not in piv,'independent system consistent');R=R[:len(piv),:];A=R[:,:n];b=R[:,n];rr=[[str(v)for v in R.row(i)]for i in range(R.rows)];sha=hashlib.sha256(json.dumps(rr,separators=(',',':')).encode()).hexdigest();cert=proofby[(swap_a,swap_b)];need(sha==cert['rref_sha256'],'independently reconstructed row space matches certificate')
  cs=cert['certificates'];need([c['variable']for c in cs]==list(range(n)),'every orbit bounded');bounds=[]
  for c in cs:
   y=s.zeros(1,R.rows);seen=set()
   for q,v in c['covector']:need(q not in seen and 0<=q<R.rows,'covector index');seen.add(q);y[q]=s.Rational(v)
   domination=y*A;need(all(domination[k]>=int(k==c['variable'])for k in range(n)),'exact rational upper-bound domination');ub=(y*b)[0];need(ub==s.Rational(c['upper_bound'])and ub<=3,'exact upper bound at most3');bounds.append(ub)
  need(sum(map(len,orbits))==512,'all tensor coefficients covered');output.append({'dual_a':swap_a,'dual_b':swap_b,'independent_equations':len(equations),'coefficient_orbits':n,'equality_rank':R.rows,'free_variables':n-R.rows,'rref_sha256':sha,'all_512_coefficients_bounded':True,'maximum_upper_bound':str(max(bounds))})
 out={'kind':'independent_R721_dual_coefficient_bound_review','imports_producer_modules':False,'induction_row_reordering':order,'exact_source_dimensions_and_Gram_verified':True,'cases':output,'scope':'Given the separately proved rank-eight bimodule factor and actual algebra A, every possible nonnegative dual fusion tensor has all512 coefficients at most3. This review does not independently establish Q-system existence or census uniqueness.','source_sha256':{str(p.relative_to(ROOT)):h(p)for p in [rankpath,proofpath,NEXT/'models/r721_dual_fusion.py',NEXT/'models/r721_dual_multiplicity_bound.py']},'verifier_sha256':h(Path(__file__))}
 (HERE/'r721_bound_review.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));return out
if __name__=='__main__':run()
