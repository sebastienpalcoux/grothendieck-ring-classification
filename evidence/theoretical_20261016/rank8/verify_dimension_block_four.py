"""Independent exact source-tensor audit of four dimension-block exclusions.
The categorical implication invokes Schopieray 2023 Lemma 3.1 (published)
and Schopieray arXiv:2609.35287v1 Theorem 5.1.
"""
import gzip,json,hashlib
from pathlib import Path
from fractions import Fraction
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[3])
base=parser.parse_args().repo.resolve()
flat=lambda R:tuple(v for a in R for b in a for v in b)
rows=[json.loads(x.replace('{','[').replace('}',']')) for x in gzip.open(base/'supplements/rank8/data/rank8_tables.txt.gz','rt')]
rows=sorted([R for R in rows if max(flat(R))==2],key=flat)
ledger={x['id']:x for x in json.load(open(base/'supplements/rank8/data/decisions.json'))}
def mul(x,y):return (x[0]*y[0]+10*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
reports=[]
for index in [35,38,346,406]:
 id=f'R8_2_{index}';R=rows[index-1]
 digest=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
 if digest!=ledger[id]['tensor_sha256']:raise ValueError('source mismatch')
 dual=[next(j for j in range(8) if R[i][j][0]) for i in range(8)]
 inv=[i for i in range(8) if sum(R[i][dual[i]])==1]
 if len(inv)!=4:raise ValueError('invertible count')
 ds=[(1,0) if i in inv else (3,1) for i in range(8)]
 for i in range(8):
  for j in range(8):
   rhs=tuple(sum(R[i][j][k]*ds[k][a] for k in range(8)) for a in (0,1))
   if mul(ds[i],ds[j])!=rhs:raise ValueError('dimension not character')
 # These values are positive; uniqueness of the positive dimension character
 # identifies them as FP dimensions. All objects use Q(sqrt10), as does D.
 D=tuple(sum(mul(d,d)[a] for d in ds) for a in (0,1))
 if D!=(80,24):raise ValueError('global dimension')
 norm=D[0]**2-10*D[1]**2
 bound=Fraction(1,40)
 twisted_square=Fraction(4*10*D[1]**2,norm**2)
 if not twisted_square>bound:raise ValueError('no contradiction')
 reports.append({'id':id,'tensor_sha256':digest,'invertibles':inv,'dimension_noninvertible':'3+sqrt(10)','global_dimension':'80+24sqrt(10)','norm':norm,'conductor':40,'twisted_sum_square':str(twisted_square),'upper_bound':str(bound),'excess':str(twisted_square-bound)})
print(json.dumps({'status':'PASS','decisions':4,'categorical_scope':'general complex fusion categorification','cases':reports},indent=2))
