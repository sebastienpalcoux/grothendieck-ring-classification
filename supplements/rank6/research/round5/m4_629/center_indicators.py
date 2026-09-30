import sys,json,itertools,time
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'));from round5_629 import *
here=Path(__file__).parent;R,d,cols,lab,src=source_data();C=d['C'];D=d['DD'];f=json.load(open(here/'rank35_fusion_data.json'));N=f['fusion_tensor'];rank=35;br=next(x for x in json.load(open(here/'rank35_modular_completions.json'))['branches'] if x['signs']==f['signs']);S=[[C([s.Rational(z) for z in v]) for v in row] for row in br['S']];dims=[z/S[0][0] for z in S[0]]
case=next(x for x in json.load(open(here/'decoded_twists.json')) if x['rank']==35 and x['solution']==0);theta=[0]*6
for o in case['orbits']:theta.extend([15//o['root_order']*o['root_power']%15]*o['copies'])
nu=[]
for i in range(rank):
 z=sum((C(N[j][k][i])*dims[j]*dims[k]*C.unit**(2*(theta[j]-theta[k])) for j in range(rank) for k in range(rank)),C.zero)/D**2
 nu.append(list(map(str,z.to_list())));print(i,nu[-1],flush=True)
(here/'center_indicators.json').write_text(json.dumps({'rank':35,'second_indicators':nu,'valid_self_dual_indicators':all(x in [['1'],['-1']] for x in nu)},indent=2))
