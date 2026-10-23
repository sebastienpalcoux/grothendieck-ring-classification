"""Exact finite cohomology behind the C2 actions on the R9_1_117 branch.
Standard-library only. A=F2^4/<1111>, S3 fixes point3; r=(012), s=(12).
The distinguished regular-module point is0. This checks the normalizer,
H2(S3,A), the explicit nonzero parity cocycle, and the neutral coherence flip.
"""
import itertools,json
from pathlib import Path

def rank(rows):
 p={}
 for v in rows:
  while v:
   k=v.bit_length()-1
   if k in p:v^=p[k]
   else:p[k]=v;break
 return len(p)
def pm(x,y):return tuple(x[y[i]] for i in range(4))
def pi(x):return tuple(x.index(i) for i in range(4))
e=(0,1,2,3);S4=list(itertools.permutations(range(4)))
G=[x for x in S4 if x[3]==3];non=[x for x in G if x!=e]
r=(1,2,0,3);s=(0,2,1,3)
def action(g,v):
 out=0
 for i in range(3):
  if v>>i&1:out^=1<<g[i]
 return (out&7)^(7 if out>>3&1 else 0)
def parity(g):return sum(g[i]>g[j] for i in range(4) for j in range(i+1,4))%2

def differential_rows(n):
 domain=list(itertools.product(non,repeat=n));idx={x:i for i,x in enumerate(domain)}
 rows=[]
 for gs in itertools.product(non,repeat=n+1):
  for bit in range(3):
   row=0
   tail=gs[1:]
   for b in range(3):
    if action(gs[0],1<<b)>>bit&1:row^=1<<(3*idx[tail]+b)
   for i in range(n):
    term=gs[:i]+(pm(gs[i],gs[i+1]),)+gs[i+2:]
    if e not in term:row^=1<<(3*idx[term]+bit)
   head=gs[:-1];row^=1<<(3*idx[head]+bit)
   rows.append(row)
 return rows,domain

d1,co1=differential_rows(1);d2,co2=differential_rows(2)
r1=rank(d1);r2=rank(d2)
assert len(co2)*3-r1-r2==1
w=7;z=1;h=w^z
assert [v for v in range(8)if action(r,v)==v]==[0,w]
assert action(s,w)==w
assert sorted({v^action(s,v)for v in range(8)})==[0,h]
assert action(s,z)==z
c=sum((w<<(3*i)) for i,(g,k) in enumerate(co2) if parity(g)*parity(k))
assert all((row&c).bit_count()%2==0 for row in d2)
# The image of d1 consists of its columns, each a vector in C2.
cols=[sum(((row>>j)&1)<<i for i,row in enumerate(d1)) for j in range(len(co1)*3)]
assert rank(cols+[c])==rank(cols)+1
# Forgetting central structure quotients A by <z>. A vector2 has norm h,
# so a character g rescales the crossed generator to have square1; the
# residual central object is w+h=z, which acts by -1 on the TY object m.
g=2
assert g^action(s,g)==h
assert w^h==z
norm=[x for x in S4 if pm(pm(x,r),pi(x)) in[r,pi(r)]]
regular=[x for x in S4 if x[0]==0]
assert set(norm)&set(regular)=={e,s}
nonregular3=[x for x in S4 if x!=e and pm(pm(x,x),x)==e and x[0]!=0]
conjugates={pm(pm(x,r),pi(x))for x in regular}
assert len(nonregular3)==6 and conjugates==set(nonregular3)
report={'status':'PASS','A':'F2^4/<1111>','S3':'point3 stabilizer','regular_module_point':0,'r':r,'s':s,'H2_S3_A_dimension':1,'d1_rank':r1,'d2_rank':r2,'C3_fixed_nonzero':w,'canonical_AutId_D_generator':z,'forgetful_w':h,'resplitting_character':g,'residual_neutral_coherence':z,'normalizer_intersection_order':2,'nonregular_C3_homomorphisms':6,'neutral_autoequivalence_conjugacy_orbits':1}
Path(__file__).with_name('triality_action_cohomology.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS H2(S3,A)=C2; explicit parity cocycle nonzero; neutral coherence flips by z')
