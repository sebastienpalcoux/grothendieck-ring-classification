import json,itertools,sys
from pathlib import Path
P=Path(__file__).resolve().parents[2];sys.path.insert(0,str(P/'software'))
from c6_two_dimension_scan import tensor
from subring_descent import closed_subrings
from prepare import key
from induction import pseudo_certificate
from rings import dnumber,codegree_factors
from exact import norm_failure,poly
rows=json.load(open(Path(__file__).with_name('c6_two_dimension_scan.json')))
census=json.load(open(P/'data/census.json'));dec={r['id']:r for r in json.load(open(P/'data/decisions.json'))}
lookup={key(r['N']):r for r in census}
known4={}
for row in rows:
 if row['obstruction']:continue
 R=tensor(row['u'],row['a'])
 for J,S in closed_subrings(R):
  if len(S)>6:break
  if max(v for M in S for rr in M for v in rr)<2:continue
  if len(S)==2:
   print(row['u'],row['a'],'K4',J);break
  if len(S)==4:
   k=key(S)
   if k not in known4:
    c=pseudo_certificate(S);known4[k]=c
   print(row['u'],row['a'],'rank4',J,'certificate',known4[k]);break
  if len(S)==6:
   r=lookup.get(key(S));print(row['u'],row['a'],'rank6',J,r['id'] if r else 'no match',dec[r['id']]['status'] if r else '','certificate',dec[r['id']].get('certificate',{}).get('kind') if r else '');break
 else:print('NO SMALL SUBRING',row['u'],row['a'])
