import sys,json,math,itertools
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'));from round5_629 import *
from round4_629_orbits import orbit_domain
here=Path(__file__).parent;R,_,_,_,src=source_data();data=ambient.data_for(R,10,15);F=data['F'];C=data['C'];out=[]
def integer_log(n,p):
 k=0
 while p**(k+1)<=n:k+=1
 return k
for rank in (35,38):
 c=json.load(open(here/f'exact_rank{rank}_h10.json'));pi=c['metadata']['profile'];cs=src['counts'][src['surviving_indices'].index(pi)];weights={tuple(v):cc for v,cc in zip(src['vectors'],cs) if cc};labels=[(v,ti) for v in weights for ti in range(len(data['phases']))];nh=len(labels);keep=c['metadata']['columns'];B=max(cs);ps=data['primes'];cp={p:int(s.factorint(F)[p]) for p in ps};reps={}
 for es in itertools.product(*(range(cp[p]+integer_log(B,p)+1) for p in ps)):
  n=math.prod(p**a for p,a in zip(ps,es));e=math.prod(p**max(0,a-cp[p]) for p,a in zip(ps,es))
  if e>B:continue
  for a in range(n):
   if math.gcd(a,n)>1:continue
   ty=tuple(ambient.relative_root(C,F,n,a*j) for j in range(1,11));ti=data['phases'].index(ty);reps.setdefault((ti,e),(n,a))
 for si,x in enumerate(c['solutions']):
  orbitlist=[]
  for xx,(j,e) in zip(x,keep):
   if xx and j<nh:
    v,ti=labels[j];n,a=reps[ti,e];orbitlist.append({'column':list(v),'copies':xx,'orbit_degree':e,'root_order':n,'root_power':a})
  rec={'rank':rank,'solution':si,'exponent':math.lcm(*(x['root_order'] for x in orbitlist)),'orbits':orbitlist};out.append(rec);print('rank',rank,'solution',si,'exponent',rec['exponent'],'orbits',orbitlist,flush=True)
(here/'decoded_twists.json').write_text(json.dumps(out,indent=2))
