import sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT/'software'),str(ROOT/'research/round3/quartic')]
from galois_probe import *
for rid in ['R6_4_22','R6_4_91']:
 R=next(r['N'] for r in json.load(open(ROOT/'data/census.json')) if r['id']==rid);m.R=R;data=data_for(R,3);tab=table_for(R,data);cols=data['lows'][1];C=data['C'];z=__import__('cmath').exp(2j*__import__('math').pi/data['F'])
 def approx(v):return sum(complex(a)*z**i for i,a in enumerate(reversed(v.to_list()))).real
 print(rid,'dims',list(map(approx,data['dims'])),'low',cols,flush=True)
 for lab in tab.assignments(cols):
  print('lab',lab,flush=True)
  wi=json.load(open(ROOT/f'research/round3/quartic/{rid}_witness_{lab[-1]}.json'));from fractions import Fraction
  from collections import Counter
  counts=Counter()
  for j,v in zip(wi['keep'],map(Fraction,wi['variables'])):
   if j<len(wi['labels']) and v:counts[tuple(wi['labels'][j][0])]+=v
  print('highvectors',dict(counts),flush=True)
  triple=list(itertools.combinations_with_replacement(range(1,6),3))
  print('lowtriples',[(t,wi['variables'][wi['keep'].index(wi['base']+i)]) for i,t in enumerate(triple)],flush=True)
