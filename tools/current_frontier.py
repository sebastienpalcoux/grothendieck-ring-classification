"""Current project-wide open identifiers, derived from accepted ledgers."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
def identifiers(repo=ROOT):
 from rank7_publication import remaining_ids
 repo=Path(repo);ids=set(remaining_ids(repo))
 for name in ('evidence/rank10_m1_exclusions_20261023/accepted_ledger.json','evidence/rank9_m2_20261024/ledger.json'):
  path=repo/name
  if not path.exists():continue
  data=json.loads(path.read_text());rows=data.get('records',[])if isinstance(data,dict)else data
  ids.update(r['id']for r in rows if r['status']=='unresolved')
 return sorted(ids,key=lambda x:tuple(map(int,re.findall(r'\d+',x))))
def count(repo=ROOT):return len(identifiers(repo))
