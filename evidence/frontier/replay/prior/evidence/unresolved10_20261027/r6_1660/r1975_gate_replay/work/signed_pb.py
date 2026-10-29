from signed_sieve import *
from signed_problem_data import data
from match_models import signature
class FiniteProblem:
 def __init__(self,R,timeout=5000):
  active,mapping,bounds,gauge,eqs,du,dualorbits=data(R)
  self.active=active;self.mapping=mapping;self.bounds=bounds;self.gauge=gauge;self.eqs=eqs;self.dualorbits=dualorbits
  sig=signature(R);groups=[[i for i in range(1,9)if sig[i]==q]for q in sorted(set(sig[1:]))];N=np.asarray(R);automorphisms=[]
  for parts in itertools.product(*(itertools.permutations(g)for g in groups)):
   p=list(range(9))
   for group,part in zip(groups,parts):
    for i,j in zip(group,part):p[i]=j
   if np.array_equal(N,N[np.ix_(p,p,p)]):automorphisms.append(p)
  self.automorphism_maps=sorted({tuple(mapping[p[a],p[b],du[p[c]]]for o in active for a,b,c in [o[0]])for p in automorphisms})
  self.gauge_signs=[tuple(mathprod(bits[j]for i in o[0]for j,orb in enumerate(dualorbits)if i in orb)for o in active)for bits in itertools.product((-1,1),repeat=len(dualorbits))]
  self.covered=set()
  self.s=z3.SolverFor('QF_FD');self.s.set(timeout=timeout);self.states=[]
  for i,b in enumerate(bounds):
   if b==1:
    neg=z3.Bool(f'n{i}');states={-1:neg,1:z3.Not(neg)}
    if i in gauge:self.s.add(z3.Not(neg))
   else:
    pos,neg=z3.Bools(f'p{i} n{i}');self.s.add(z3.Not(z3.And(pos,neg)))
    states={-2:neg,2:pos,0:z3.Not(z3.Or(pos,neg))}
    if i in gauge:self.s.add(z3.Not(neg))
   self.states.append(states)
  for eq in eqs:
   weights=[];constant=0
   for (a,b),co in eq:
    if a==b==-1:constant+=co;continue
    if a==b and bounds[a]==1:constant+=co;continue
    if a==b:
     weights.append((z3.Or(self.states[a][-2],self.states[a][2]),co*4));continue
    aa={1:z3.BoolVal(True)}if a==-1 else self.states[a];bb={1:z3.BoolVal(True)}if b==-1 else self.states[b]
    for x,cx in aa.items():
     for y,cy in bb.items():
      if x*y:weights.append((z3.And(cx,cy),co*x*y))
   positive=[];rhs=-constant
   for cond,w in weights:
    if w<0:positive.append((z3.Not(cond),-w));rhs-=w
    else:positive.append((cond,w))
   self.s.add(z3.PbEq(positive,rhs))
 def check(self):return self.s.check()
 def values(self):
  m=self.s.model();return [next(v for v,c in row.items()if z3.is_true(m.eval(c,model_completion=True)))for row in self.states]
 def block(self,vals):self.s.add(z3.Or(*(z3.Not(self.states[i][v])for i,v in enumerate(vals))))
 def block_gauge_orbit(self,vals):
  seen=set()
  for perm in self.automorphism_maps:
   v=[vals[j]for j in perm]
   for signs in self.gauge_signs:
    if any(v[i]*signs[i]<0 for i in self.gauge):continue
    vv=tuple(x*y for x,y in zip(v,signs))
    if vv not in self.covered:self.block(vv);self.covered.add(vv)
    seen.add(vv)
  return len(seen)
def mathprod(values):
 p=1
 for x in values:p*=x
 return p
def discover_pb(R,spherical_report,max_seconds=35,max_branches=256,previous=None):
 start=time.time();src=chars(R);P=FiniteProblem(R);branches=[]
 # The positive table always occurs; close it before asking the finite solver.
 initial=[R[a][b][next(j for j in range(9)if R[c][j][0])]for o in P.active for a,b,c in [o[0]]]
 if previous and previous.get('branches'):
  for b in previous['branches']:
   if tuple(b['values'])in P.covered:continue
   size=P.block_gauge_orbit(b['values']);branches.append(dict(b,gauge_orbit_size=size))
 else:branches.append({'values':initial,'obstruction':{'kind':'original_gauge','signs':[1]*9,'spherical_report':spherical_report},'gauge_orbit_size':P.block_gauge_orbit(initial)})
 while time.time()-start<max_seconds and len(branches)<max_branches:
  result=P.check()
  if result==z3.unsat:return {'outcome':'excluded','complete':True,'variables':len(P.states),'equations':len(P.eqs),'gauge_coordinates':P.gauge,'branches':branches,'seconds':time.time()-start,'backend':'exact_pseudo_boolean_associativity'}
  if result!=z3.sat:return {'outcome':'no_conclusion','complete':False,'reason':str(result),'branches':branches,'seconds':time.time()-start}
  values=P.values();T=tensor(R,P.mapping,values);g=original_gauge(R,T)
  if g is not None:why={'kind':'original_gauge','signs':g,'spherical_report':spherical_report}
  else:
   why=dnumber(T)
   if why is None:
    a=chars(T);cb=[]
    for f,m in a.components:cb.append({'factor':pc(f),'obstruction':char_obstruction(a,f,list(src.cf)+list(a.cf))})
    if any(b['obstruction'] is None for b in cb):return {'outcome':'no_conclusion','complete':False,'reason':'signed character survives','branches':branches,'surviving_values':values,'surviving_characters':cb,'seconds':time.time()-start}
    why={'kind':'all_signed_scalar_characters_excluded','characters':cb}
  branches.append({'values':values,'obstruction':why,'gauge_orbit_size':P.block_gauge_orbit(values)})
 return {'outcome':'no_conclusion','complete':False,'reason':'discovery allowance','branches':branches,'seconds':time.time()-start}
if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--ring');ap.add_argument('--seconds',type=int,default=90);args=ap.parse_args()
 raw={r['id']:r for r in read()};pre={r['id']:r['report']for r in load('sphere_original.json')}
 for rid in ([args.ring]if args.ring else ['R9_2_686','R9_2_690','R9_2_736','R9_2_769']):
  old=load('pb_'+rid+'.json')if(BASE/'work'/('pb_'+rid+'.json')).exists()else None
  r=discover_pb(raw[rid]['tensor'],pre[rid],max_seconds=args.seconds,max_branches=2000,previous=old);save('pb_'+rid+'.json',r);print(rid,r['outcome'],len(r['branches']),round(r['seconds'],2),flush=True)
