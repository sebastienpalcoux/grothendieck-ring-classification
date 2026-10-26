from pathlib import Path
import itertools,json,hashlib
import ring_checks as common
HERE=Path(__file__).resolve().parent

def main():
 D=json.loads((HERE/'original_tensors.json').read_text());allowed=json.loads((HERE/'exhaustive_catalog.json').read_text())['allowed_ids'];records=[]
 for rid,R in D.items():
  common.validate(R);n=len(R);du=common.dual(R);G=[i for i in range(n)if R[i][du[i]]==[1]+[0]*(n-1)];non=[i for i in range(n)if i not in G];common.require(len(G)==8 and len(non)==4,'family invertible count');solutions=[]
  for small in itertools.combinations(non,2):
   dims=[(1,0)if i in G else(2,0)if i in small else(0,2)for i in range(n)]
   good=True
   for i,j in itertools.product(range(n),repeat=2):
    a,b=dims[i];c,d=dims[j];rhs=tuple(sum(R[i][j][k]*dims[k][t]for k in range(n))for t in range(2))
    if rhs!=(a*c+2*b*d,a*d+b*c):good=False;break
   if good:solutions.append(dims)
  common.require(len(solutions)==1,'unique exact positive dimension character');dims=solutions[0];squares=[a*a+2*b*b for a,b in dims];common.require(sum(squares)==32,'global dimension32');small=[i for i,x in enumerate(squares)if x==4];neutral=[i for i,(a,b)in enumerate(dims)if not b];odd=set(range(n))-set(neutral)
  common.require(sum(squares[i]for i in neutral)==16,'neutral dimension16')
  for i,j,k in itertools.product(range(n),repeat=3):
   if R[i][j][k]:common.require(int(k in odd)==(int(i in odd)^int(j in odd)),'integral C2 grading')
  H=[g for g in G if R[g][small[0]][small[0]]];common.require(len(H)==4,'stabilizer order4')
  for x in small:common.require([g for g in G if R[g][x][x]]==H==[g for g in G if R[x][g][x]],'common bilateral stabilizer')
  for i,j in itertools.product(small,repeat=2):common.require(all(not R[i][j][k]for k in range(n)if k not in G),'neutral generalizedTY')
  def closure(S):
   S=set(S)
   while True:
    T=S|{du[i]for i in S}|{k for i in S for j in S for k,v in enumerate(R[i][j])if v}
    if T==S:return S
    S=T
  series=[set(range(n))]
  while len(series[-1])>1:
   T=closure({k for i in series[-1]for k,v in enumerate(R[i][du[i]])if v});common.require(T!=series[-1],'nilpotent decrease');series.append(T)
  sd=[sum(squares[i]for i in S)for S in series];common.require(sd==[32,16,4,1],'exact adjoint dimensions')
  hits=[]
  for aid in allowed:
   p=common.based_iso(R,D[aid])
   if p is not None:hits.append(dict(id=aid,basis_map=p))
  if rid in allowed:common.require(len(hits)==1 and hits[0]['id']==rid,'allowed ring unique')
  else:common.require(not hits,'not any allowable categorical tensor')
  records.append(dict(id=rid,tensor_sha256=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest(),squared_dimensions=squares,integral_neutral=neutral,stabilizer=H,adjoint_series=[sorted(S)for S in series],adjoint_dimensions=sd,allowed_matches=hits))
 out=dict(status='pass',census_count=len(D),allowed_count=len(allowed),outside_catalog_count=sum(not r['allowed_matches']for r in records),records=records);(HERE/'structural_binding.json').write_text(json.dumps(out,indent=2)+'\n');print(out['census_count'],out['allowed_count'],out['outside_catalog_count'])
if __name__=='__main__':main()
