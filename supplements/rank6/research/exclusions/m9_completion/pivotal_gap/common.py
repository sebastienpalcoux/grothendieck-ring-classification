import json, hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
def require(v,msg):
 if not v: raise ValueError(msg)
def tensors(source_root=None):
 rows=json.loads((HERE/'tensors.json').read_text())
 hashes=json.loads((HERE/'tensor_hashes.json').read_text())
 require({r['id'] for r in rows}==set(hashes),'fixture inventory differs')
 for r in rows:
  require(hashlib.sha256(json.dumps(r['N'],separators=(',',':')).encode()).hexdigest()==hashes[r['id']],'tensor digest differs')
 if source_root is not None:
  source={r['id']:r for r in json.loads((Path(source_root)/'data/census.json').read_text())}
  for r in rows: require(r['id'] in source and source[r['id']]['N']==r['N'],'source tensor differs: '+r['id'])
 return rows
def stable(report): return json.loads(json.dumps({k:v for k,v in report.items() if k!='seconds'}))
