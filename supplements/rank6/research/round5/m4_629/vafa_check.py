"""All Vafa congruences for the retained self-dual rank-35 fusion datum."""
import itertools,json,sys
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
from exact import require
here=Path(__file__).parent
N=json.load(open(here/'rank35_fusion_data.json'))['fusion_tensor']
case=next(c for c in json.load(open(here/'decoded_twists.json')) if c['rank']==35 and c['solution']==0)
theta=[0]*6
for o in case['orbits']:theta.extend([15//o['root_order']*o['root_power']%15]*o['copies'])
count=0;bad=[]
for i,j,k,l in itertools.combinations_with_replacement(range(35),4):
 m=sum(N[i][j][a]*N[k][l][a] for a in range(35))
 lhs=m*(theta[i]+theta[j]+theta[k]+theta[l])
 rhs=sum(theta[a]*(N[i][j][a]*N[k][l][a]+N[i][k][a]*N[j][l][a]+N[i][l][a]*N[j][k][a]) for a in range(35))
 count+=1
 if (lhs-rhs)%15:bad.append([i,j,k,l,(lhs-rhs)%15])
require(not bad,'Vafa congruence failed')
record={'checked':count,'failures':bad};(here/'vafa_check.json').write_text(json.dumps(record,indent=2));print(record)
