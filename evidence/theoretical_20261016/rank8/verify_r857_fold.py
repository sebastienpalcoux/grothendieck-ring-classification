"""Source-bound all-coefficient folded-SU(2) identification; no categorification claim."""
import argparse,gzip,json,hashlib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[3]);repo=p.parse_args().repo.resolve()
flat=lambda R:tuple(x for a in R for b in a for x in b)
rows=[json.loads(x.replace('{','[').replace('}',']')) for x in gzip.open(repo/'supplements/rank8/data/rank8_tables.txt.gz','rt')]
R=sorted((r for r in rows if max(flat(r))==2),key=flat)[856]
sha=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
entry=next(r for r in json.loads((repo/'supplements/rank8/data/decisions.json').read_text()) if r['id']=='R8_2_857')
if sha!=entry['tensor_sha256']:raise ValueError('Source tensor hash mismatch')
mapping=[0,1,3,6,5,4,7,2]
S=[[[0]*8 for j in range(8)] for i in range(8)]
for i in range(8):
 for j in range(8):
  a,b=2*mapping[i],2*mapping[j]
  for c in range(abs(a-b),min(a+b,60-a-b)+1,2):
   S[i][j][mapping.index(min(c,30-c)//2)]+=1
if R!=S:raise ValueError('Tensor identification failed')
print(json.dumps({'status':'PASS','id':'R8_2_857','tensor_sha256':sha,'source_to_j':mapping,'level':30,'coefficients_checked':512,'scope':'Exact based-ring identification only; categorification status is assessed separately.'},indent=2))
