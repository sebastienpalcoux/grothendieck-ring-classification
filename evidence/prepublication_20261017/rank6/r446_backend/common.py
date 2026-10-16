"""Exact input/source commitments for the append-only R446 replay packet."""
from pathlib import Path
import hashlib,json
PACKET=Path(__file__).resolve().parent
DEFAULT_REPO=PACKET.parents[3]
def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def canonical_digest(value):
 return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def require(okay,message):
 if not okay:raise ValueError(message)
def bound_inputs(repo):
 repo=Path(repo).resolve();base=repo/'supplements/rank6'
 c=json.loads((PACKET/'commitments.json').read_text())
 for name,expected in c['source_files_sha256'].items():
  require(digest(base/name)==expected,'source mismatch: '+name)
 for name,expected in c['input_files_sha256'].items():
  require(digest(base/name)==expected,'input file mismatch: '+name)
 row=next(x for x in json.loads((base/'data/census.json').read_text()) if x['id']=='R6_4_446')
 entry=next(x for x in json.loads((base/'data/decisions.json').read_text()) if x['id']=='R6_4_446')
 require(canonical_digest(row['N'])==c['tensor_sha256'],'tensor mismatch')
 require(canonical_digest(entry['certificate'])==c['certificate_sha256'],'certificate mismatch')
 return base,row,entry,c
