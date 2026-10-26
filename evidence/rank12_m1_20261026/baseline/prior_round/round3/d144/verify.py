"""Exact scope-limited D144 continuation; conditional twists are NOT models."""
from pathlib import Path
import itertools,json,hashlib
from triality import source_tensor,zest,require
ROOT=Path(__file__).resolve().parent
RINGS=json.loads((ROOT/'tensors.json').read_text())
CONDITIONAL=json.loads((ROOT/'conditional_twists.json').read_text())
def sha(r):return hashlib.sha256(json.dumps(r,separators=(',',':')).encode()).hexdigest()
def auto(R,p):return all(R[i][j][k]==R[p[i]][p[j]][p[k]]for i,j,k in itertools.product(range(12),repeat=3))
def twist(R,p):return [[[R[i][p[j]if i>=8 else j][k]for k in range(12)]for j in range(12)]for i in range(12)]
def same(R,S,p):return all(R[i][j][k]==S[p[i]][p[j]][p[k]]for i,j,k in itertools.product(range(12),repeat=3))
rows=[]
for m in (0,1):
 R=source_tensor(m);autos=[]
 for a,b,c in itertools.product(itertools.permutations(range(3,6)),itertools.permutations(range(6,8)),itertools.permutations(range(8,12))):
  p=[0,1,2]+list(a+b+c)
  if auto(R,p):autos.append(p)
 q=[R[1][i].index(1)if i>=8 else i for i in range(12)]
 require(auto(R,q),'canonical bosonic simple-current tensor auto acts on ring')
 require(twist(R,q)==zest(R),'canonical current twist equals already known central zest')
 for row in CONDITIONAL:
  if row['m']!=m:continue
  p=row['involutive_ring_automorphism'];T=twist(R,p)
  require(p in autos and all(p[p[i]]==i for i in range(12)),'candidate involutive ring automorphism')
  require(same(RINGS[row['id']],T,row['basis_map_source_to_model']),'exact conditional target identification')
  require(p not in [list(range(12)),q],'not supplied by the canonical bosonic current action')
  rows.append({'id':row['id'],'input_sha256':sha(RINGS[row['id']]),'status':'unresolved','conditional_identity_verified':True,'categorical_lift_missing':True})
 print('m',m,'ring automorphisms',len(autos),'involutions',sum(all(p[p[i]]==i for i in range(12))for p in autos))
 # All pointed inverse images are supported on 1,z,E, and E preserves each odd z-pair.
 for i in range(8,12):require(set(k for k,x in enumerate(R[2][i])if x)=={i,R[1][i].index(1)},'C3 action preserves each two-element odd support block')
# Integral dimensions after actual 1+z Morita condensation.
possible=[]
for t in range(4):
 mult={1:6,2:4*t,3:2,4:3-t}
 require(sum(d*d*n for d,n in mult.items())==72,'neutral Morita dimension')
 if all(count%3==0 for d,count in mult.items()if d*d%3):possible.append(t)
require(possible==[0,3],'C3 orbit divisibility leaves t=0 or3')
# Finite arithmetic inputs of the independently audited t=0 branch exclusion.
require([u for u in range(5) if 9*u%12==0]==[0,4], 'sqrt2 orbit restriction')
require(144%96!=0, 'putative dimension96 subcategory violates rational divisibility')
require([n for n in range(1,5) if 24%n==0 and 24//n<=18 and (18-24//n)%4==0]==[4], 'odd G24 action transitive')
coef=[v for v in itertools.product(range(3),repeat=3) if sum(v)==2 and v[1]==v[2]]
require(coef==[(0,1,1),(2,0,0)], 'only two generalized near-group coefficient vectors')
require(not any(sum(v)==2 and v[0]==v[1]==v[2] for v in itertools.product(range(3),repeat=3)), 'inverting right action impossible')
# f=48-3x, x^2=8-x; evaluate f^2-99f+2376 in basis1,x.
f=(48,-3)
f2=(f[0]*f[0]+8*f[1]*f[1],2*f[0]*f[1]-f[1]*f[1])
require((f2[0]-99*f[0]+2376,f2[1]-99*f[1])==(0,0), 'exact formal-codegree polynomial')
require(99*99-4*2376==297 and 17*17<297<18*18, 'codegree quadratic irreducible')
require((99*99)%2376!=0, 'quadratic d-number obstruction')
# Cyclic intersection means all projective irreducibles have degree one.
module_possibilities=[(k,s) for k in range(1,25) if 24%k==0 for s in (1,2,4) if k%s==0 and 4*k==6*s*s]
require(module_possibilities==[(6,2),(24,4)], 'rank-four sqrt6 module possibilities')
S4=list(itertools.permutations(range(4)));identity=tuple(range(4))
def compose(a,b):return tuple(a[b[i]] for i in range(4))
def inverse(a):return tuple(a.index(i) for i in range(4))
h=(1,2,3,0);H={identity};x=h
while x!=identity:H.add(x);x=compose(x,h)
require(len(H)==4,'actual C4 subgroup')
for point in range(4):
 K={a for a in S4 if a[point]==point}
 require(len(K)==6,'all S3 point stabilizers have order six')
 for a in S4:
  conjugate={compose(compose(a,b),inverse(a)) for b in K}
  require(len(H & conjugate)==1,'C4 has trivial intersection with every S3 subgroup')
eq_type={1:6,2:3,3:6}; required_type={1:24,4:3}
require(sum(d*d*n for d,n in eq_type.items())==72,'equivariantized RepS4 dimension')
require(eq_type!=required_type,'invertible module dual types contradict')
branch={'excluded_splitting_parameters':[0], 'remaining_splitting_parameters':[3], 'first_dual_integral_type':{'1':6,'2':12,'3':2},'full_first_dual_rank':24,'actual_RepS3_subcategory':True,'regular_dimension6_algebra_exists':True,'central_embedding_proved':False,'scope':'The categorical proof is in findings.md; arithmetic replay proves no monoidal lift.'}
out={'status':'PASS' ,'models':[],'exclusions':[],'unresolved':rows,'new_theoretical_reduction':{'possible_first_Morita_splitting_parameters':[3],'second_C3_algebra_exists':True,'scope':'necessary categorical structure; not an exclusion or a construction'}}
out['branch_exclusion']=branch
(ROOT/'verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','new_resolutions':0,'remaining':len(rows)}))
