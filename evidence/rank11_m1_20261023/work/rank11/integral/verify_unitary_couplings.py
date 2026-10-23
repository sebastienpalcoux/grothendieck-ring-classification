"""Replay every Lim coupling using only the Python standard library.

Reads source tensors independently, checks their hashes and exact FP
characters, and verifies all three pairwise marginals for all 1331 triples.
"""
from pathlib import Path
import fractions,gzip,hashlib,itertools,json
F=fractions.Fraction
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]

def require(c,m):
 if not c:raise ValueError(m)

def main():
 rows=json.loads((HERE/'unitary_checks.json').read_text())
 with gzip.open(ROOT/'repositories/fusion-ring-census/results/rank11/tables.txt.gz','rt') as f:lines=f.read().splitlines()
 require([q['id'] for q in rows]==['R11_1_104','R11_1_153'],'case identities')
 for row in rows:
  rid=row['id'];R=json.loads(lines[int(rid.rsplit('_',1)[1])-1].replace('{','[').replace('}',']'));n=len(R);d=row['dimensions']
  require(hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()==row['tensor_sha256'],'source tensor hash')
  require(len(d)==n and d[0]==1 and all(type(x)==int and x>0 for x in d),'positive dimensions')
  require(sum(x*x for x in d)==row['global_dimension']==32,'global dimension')
  for i,j in itertools.product(range(n),repeat=2):require(sum(R[i][j][k]*d[k] for k in range(n))==d[i]*d[j],'FP character')
  P=[[[F(R[i][j][k]*d[k],d[i]*d[j]) for k in range(n)] for j in range(n)] for i in range(n)]
  seen=set();nonzero=0
  for entry in row['couplings']:
   i,j,k=entry['ijk'];require((i,j,k) not in seen,'duplicate triple');seen.add((i,j,k));acc=[{} for _ in range(3)];labels=set()
   for l,m,t,a,b in entry['entries']:
    require(all(type(x)==int and 0<=x<n for x in (l,m,t)),'label bounds');require((l,m,t) not in labels,'duplicate variable');labels.add((l,m,t));q=F(a,b);require(q>0,'positive sparse entry');nonzero+=1
    for z,tag in enumerate(((l,m),(l,t),(m,t))):acc[z][tag]=acc[z].get(tag,F(0))+q
   for a,b in itertools.product(range(n),repeat=2):
    require(acc[0].get((a,b),0)==P[i][j][a]*P[j][k][b],'independence marginal')
    require(acc[1].get((a,b),0)==P[i][j][a]*P[a][k][b],'left conditional marginal')
    require(acc[2].get((a,b),0)==P[j][k][a]*P[i][a][b],'right conditional marginal')
  require(seen==set(itertools.product(range(n),repeat=3)),'complete triple coverage')
  print(rid,'PASS',len(seen),'triples',nonzero,'nonzero entries',3*n**5,'exact marginal equations')
if __name__=='__main__':main()
