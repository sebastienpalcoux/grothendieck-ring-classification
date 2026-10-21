#!/usr/bin/env python3
"""Audit the GAP transcript and exactly compare every compatible character tensor.

--check is read-only, uses only the Python standard library, and remains active
under python -O. It does not rerun GAP's group catalogue or character tables.
"""
import argparse,hashlib,itertools,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
EVIDENCE=HERE.parents[1]
def require(value,message):
 if not value:raise ValueError(message)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tensor_digest(t):return hashlib.sha256(json.dumps(t,separators=(',',':')).encode()).hexdigest()
def validate_tensor(n):
 require(len(n)==8 and all(len(a)==8 and all(len(b)==8 for b in a) for a in n),'tensor shape')
 require(all(type(c) is int and c>=0 for a in n for b in a for c in b),'nonnegative integral tensor')
 require(all(n[0][i][j]==n[i][0][j]==int(i==j) for i in range(8) for j in range(8)),'unit')
 for i,j,k,l in itertools.product(range(8),repeat=4):
  require(sum(n[i][j][s]*n[s][k][l] for s in range(8))==sum(n[j][k][s]*n[i][s][l] for s in range(8)),'associativity')
def isomorphisms(a,b,da,db):
 blocks=[]
 for value in sorted(set(da[1:])):
  left=[i for i in range(1,8) if da[i]==value];right=[i for i in range(1,8) if db[i]==value]
  require(len(left)==len(right),'degree block size');blocks.append((left,list(itertools.permutations(right))))
 for chosen in itertools.product(*(x[1] for x in blocks)):
  p=[0]*8
  for (left,_),right in zip(blocks,chosen):
   for i,j in zip(left,right):p[i]=j
  if all(a[i][j][k]==b[p[i]][p[j]][p[k]] for i,j,k in itertools.product(range(8),repeat=3)):yield p

def compute():
 targets=json.loads((HERE/'targets.json').read_text());raw=[json.loads(line) for line in (HERE/'gap_scan.jsonl').read_text().splitlines() if line.strip()]
 require(raw and raw[0]['kind']=='environment' and raw[-1]['kind']=='scan_complete','complete transcript markers')
 require(sum(x['kind']=='environment' for x in raw)==1 and sum(x['kind']=='scan_complete' for x in raw)==1,'unique transcript markers')
 require(all(x['kind'] in ['environment','order_start','group','order_complete','scan_complete'] for x in raw),'unexpected transcript record')
 require(targets['source_sha256']==digest(EVIDENCE/'pipeline/survivor_profiles.json'),'profile source hash')
 require(sorted({x['order'] for x in targets['targets']})==targets['orders'],'target order coverage')
 require(sorted({x['order'] for x in raw if 'order' in x})==targets['orders'],'transcript order coverage')
 census={x['id']:x for x in json.loads((EVIDENCE/'pipeline/census_m3.json').read_text())};groups={};orders=[]
 for order in targets['orders']:
  starts=[x for x in raw if x['kind']=='order_start' and x['order']==order];ends=[x for x in raw if x['kind']=='order_complete' and x['order']==order]
  require(len(starts)==len(ends)==1,'one start/end per order');count=starts[0]['groups'];require(type(count)is int and count>0 and ends[0]['groups']==count,'order counts')
  rows=[x for x in raw if x['kind']=='group' and x['order']==order]
  require(sorted(x['index'] for x in rows)==list(range(1,count+1)),'every group index exactly once')
  for row in rows:
   require(type(row['rank']) is int and row['rank']>0,'class number')
   if row['rank']==8:
    degrees=row['degrees'];require(len(degrees)==8 and all(type(x)is int and x>0 for x in degrees) and sum(x*x for x in degrees)==order,'character degrees')
   if 'tensor' in row:
    validate_tensor(row['tensor']);require(row['rank']==8,'exported tensor rank');d=row['unit_first_degrees'];require(d[0]==1 and sorted(d)==sorted(row['degrees']),'unit-first degrees')
    require(all(d[i]*d[j]==sum(row['tensor'][i][j][k]*d[k] for k in range(8)) for i in range(8) for j in range(8)),'exported degree homomorphism')
  groups[order]=rows;orders.append({'order':order,'groups':count,'rank_eight_groups':sum(x['rank']==8 for x in rows),'tensors_exported':sum('tensor' in x for x in rows)})
 attempts=[]
 for target in targets['targets']:
  ring=census[target['id']];n=ring['tensor'];d=target['degrees'];order=target['order']
  require(target['tensor_sha256']==tensor_digest(n)==ring['tensor_sha256'],'target tensor source hash')
  require(len(d)==8 and d[0]==1 and all(type(x)is int and x>0 for x in d) and sum(x*x for x in d)==order,'positive target degrees')
  require(all(d[i]*d[j]==sum(n[i][j][k]*d[k] for k in range(8)) for i in range(8) for j in range(8)),'all64 dimension equations')
  candidates=[g for g in groups[order] if g['rank']==8 and sorted(g['degrees'])==sorted(d)];matches=[]
  for group in candidates:
   require('tensor' in group,'every degree-compatible group tensor exported')
   p=next(isomorphisms(n,group['tensor'],d,group['unit_first_degrees']),None)
   if p is not None:matches.append({'small_group_id':[order,group['index']],'target_to_character_basis_permutation':p,'tensor_sha256':tensor_digest(group['tensor'])})
  attempts.append({**target,'method':'exhaustive_smallgroups_ordinary_representation_scan','outcome':'ordinary_group_model' if matches else 'no_ordinary_group_model','scope':'Ordinary complex representation rings of finite groups only; no conclusion for arbitrary fusion categories or twisted group-theoretical constructions.','groups_checked':len(groups[order]),'rank_eight_groups':sum(g['rank']==8 for g in groups[order]),'degree_matching_groups':len(candidates),'exact_full_tensor_isomorphism_test_for_every_degree_match':True,'matches':matches})
 result={'status':'COMPLETE','verification_scope':'Source-bound GAP transcript audit and exact Python comparison of exported tensors. Does not independently regenerate the SmallGroups catalogue or character tables.','environment':raw[0],'orders':orders,'total_groups':sum(x['groups'] for x in orders),'attempts':attempts,'sources_sha256':{name:digest(HERE/name) for name in ['scan.g','gap_scan.jsonl','targets.json','prepare_scan.py','summarize_scan.py']}}
 return result,attempts

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args();result,attempts=compute()
 if args.check:
  require(result==json.loads((HERE/'results.json').read_text()),'saved results mismatch');require(attempts==json.loads((HERE/'per_id_attempts.json').read_text()),'saved per-ID attempts mismatch')
 else:
  (HERE/'results.json').write_text(json.dumps(result,indent=2)+'\n');(HERE/'per_id_attempts.json').write_text(json.dumps(attempts,indent=2)+'\n')
 print(json.dumps({'status':'PASS','mode':'read-only transcript audit' if args.check else 'write summary','groups':result['total_groups'],'target_rings':len(attempts),'ordinary_group_models':[x['id'] for x in attempts if x['matches']]}))
if __name__=='__main__':main()
