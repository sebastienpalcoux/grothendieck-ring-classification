"""Verify that the necessary central fusion datum has the required forgetful map."""
import sys,json
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
from round5_629 import source_data,require
here=Path(__file__).parent;R,d,cols,lab,src=source_data()
case=next(c for c in json.load(open(here/'decoded_twists.json')) if c['rank']==35 and c['solution']==0);vs=list(cols)
for o in case['orbits']:vs.extend([(0,)+tuple(o['column'])]*o['copies'])
N=json.load(open(here/'rank35_fusion_data.json'))['fusion_tensor'];bad=[];checks=0
for i in range(35):
 for j in range(i,35):
  for k in range(6):
   a=sum(N[i][j][z]*vs[z][k] for z in range(35));b=sum(vs[i][x]*vs[j][y]*R[x][y][k] for x in range(6) for y in range(6));checks+=1
   if a!=b:bad.append([i,j,k,a,b])
require(not bad,'forgetful map not multiplicative')
record={'checked':checks,'failures':bad};(here/'full_restriction_check.json').write_text(json.dumps(record,indent=2));print(record)
