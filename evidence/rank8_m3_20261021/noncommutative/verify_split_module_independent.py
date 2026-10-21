"""Scalar-integer independent replay, with a different sign-gauge forest."""
from pathlib import Path
import hashlib,itertools,json,math,time
HERE=Path(__file__).resolve().parent
def require(v,m):
 if not v:raise ValueError(m)
def multiply(A,B):return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def polynomial(A,coefficients):
 n=len(A);V=[[0]*n for _ in range(n)]
 for c in coefficients:
  V=multiply(V,A)
  for i in range(n):V[i][i]+=c
 return V
def zero(A):return not any(v for row in A for v in row)
def run(R,c):
 g,x=c['involution'],c['generator'];n=len(R);require(R[g][g]==[1]+[0]*(n-1) and g!=0,'bad involution');require(R[x][x][0]==1,'non-self-dual generator')
 fixed=[a for a in range(n) if R[g][a][a]];f=len(fixed);coefficients=c['search']['polynomial'];require(zero(polynomial(R[x],coefficients)),'source relation failed')
 A=[[R[x][a][b] for b in fixed] for a in fixed];require(A==list(map(list,zip(*A))),'nonsymmetric block');seen=set();forest=set()
 for start in range(f):
  if start in seen:continue
  seen.add(start);queue=[start]
  for a in queue:
   for b in range(f):
    if a!=b and A[a][b]%2 and b not in seen:seen.add(b);queue.append(b);forest.add(tuple(sorted((a,b))))
 entries=[]
 for a in range(f):
  for b in range(a,f):
   values=list(range(-A[a][b],A[a][b]+1,2))
   if (a,b) in forest:values=[v for v in values if v>0]
   entries.append((a,b,values))
 count=0
 for values in itertools.product(*(e[2] for e in entries)):
  S=[[0]*f for _ in range(f)]
  for (a,b,_),v in zip(entries,values):S[a][b]=S[b][a]=v
  require(not zero(polynomial(S,coefficients)),'exact split-module matrix survived');count+=1
 require(count==c['search']['cases'],'gauge-reduced count differs')
 return {'cases':count,'fixed_objects':fixed,'arithmetic':'unbounded Python integers','gauge':'breadth-first odd-entry forest'}
def main():
 start=time.monotonic();rows={r['id']:r for r in json.loads((HERE.parent/'pipeline/census_m3.json').read_text())};records=[];source=HERE/'split_module_polynomial_results.json'
 for item in json.loads(source.read_text()):
  if item['outcome']!='excluded':continue
  row=rows[item['id']];require(row['tensor_sha256']==item['tensor_sha256'],'source hash mismatch');result=run(row['tensor'],item['certificate']);records.append(dict(id=item['id'],**result));print(item['id'],result['cases'],'PASS',flush=True)
 out={'status':'PASS','records':records,'seconds':round(time.monotonic()-start,4),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'reference_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
 (HERE/'split_module_independent_validation.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS',out['seconds'],flush=True)
if __name__=='__main__':main()
