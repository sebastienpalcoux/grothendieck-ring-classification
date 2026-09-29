"""Exact antiinvariant-module sign patterns on all currently unresolved inputs."""
import json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'software'))
from involution_module import invs
from module_dual_gram import anti_representations
from rings import dual
rows=json.load(open(ROOT/'data/decisions.json'));census={r['id']:r for r in json.load(open(ROOT/'data/census.json'))}
out=[]
for row in rows:
 if row['existence']['general']!='unknown':continue
 R=census[row['id']]['N'];du=dual(R)
 if any(R[i][j]!=R[j][i] for i in range(6) for j in range(6)):continue
 for g in invs(R):
  info=anti_representations(R,g)
  if info is None:continue
  fixed,seed,nodes,reps=info;f=len(fixed)
  patterns={tuple(T[g][j*f+j] for j in range(fixed.__len__())) for T in reps}
  record={'id':row['id'],'m':row['m'],'g':g,'fixed':fixed,'cubic_dimensions':[R[y][y][du[y]] for y in fixed],
          'generators':list(seed),'generator_nodes':nodes,'module_branches':len(reps),'kappa_patterns':sorted(map(list,patterns)),
          'forced_minus_objects':[y for j,y in enumerate(fixed) if all(T[g][j*f+j]==-1 for T in reps)],
          'branches':[{'T':[list(x) for x in T],'kappa':[T[g][j*f+j] for j in range(f)]} for T in reps]}
  out.append(record)
  print(json.dumps({k:v for k,v in record.items() if k not in ('branches',)}),flush=True)
 (Path(__file__).with_suffix('.json')).write_text(json.dumps(out,indent=2)+'\n')
