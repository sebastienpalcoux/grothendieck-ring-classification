import sys,json,time,math
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
from round4_629_orbits import *
from modular_moments import congruence_witness,check_congruence
from round4_quartic_profiles import enumerate_affine
from exact import require
here=Path(__file__).parent;st=time.monotonic();R=next(x['N'] for x in json.load(open(P/'data/unresolved_tensors.json')) if x['id']=='R6_4_629');src=json.load(open(here/'filtered_profiles.json'));record=json.load(open(here/'fixed_twist_h6.json'));d=ambient.data_for(R,6,15);cols=d['lows'][3];A,b,meta=ambient.system(R,d,cols,record['ep'],record['lab']);br=next(x for x in record['branches'] if x['rank']==30);c=src['counts'][src['surviving_indices'].index(br['profile'])];vs=list(map(tuple,src['vectors']));labs=[(v,ti) for v in vs for ti in range(len(d['phases']))];nh=len(labs);keep=br['columns'];AA=[[row[j]*e for j,e in keep] for row in A];bb=b[:]
for v,cc in zip(vs,c):
 if cc:AA.append([int(j<nh and labs[j][0]==v)*e for j,e in keep]);bb.append(cc)
print('system',len(AA),len(AA[0]),flush=True);out={'id':'R6_4_629','profile':br['profile'],'rank':30,'rows':len(AA),'variables':len(keep)}
co=congruence_witness(AA,bb,[1]*len(keep),primes=(2,3,5,7));print('congruence',co,flush=True)
if co:check_congruence(AA,bb,[1]*len(keep),co);out.update(outcome='exact_congruence_obstruction',congruence=co)
else:
 bounds=[]
 for j,e in keep:
  if j<nh:bounds.append(c[vs.index(labs[j][0])]//e)
  else:
   block=next(x for x in meta['rotation_blocks'] if x[2]<=j<x[2]+x[3]);obj,order,_,_=block;p=[1]+[0]*5
   for _ in range(order):p=[sum(p[a]*R[a][obj][z] for a in range(6)) for z in range(6)]
   bounds.append(p[0])
 out['bounds']=bounds
 sols,stats=enumerate_affine(AA,bb,bounds,node_limit=30000000);out.update(outcome='exact_integer_obstruction' if not sols else 'integer_system_survives',enumeration=stats,solutions=[list(z) for z in sols]);print('enum',stats,'solutions',len(sols),flush=True)
out['seconds']=time.monotonic()-st;(here/'rank30_exact.json').write_text(json.dumps(out));print({k:v for k,v in out.items() if k not in ['bounds','solutions','congruence']},flush=True)
