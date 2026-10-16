import gzip,json,itertools,collections,time,argparse,hashlib
from pathlib import Path
flat=lambda R:tuple(c for a in R for b in a for c in b)
def solve(R,idx):
 triples=[v for v in itertools.combinations_with_replacement(range(1,8),3)if R[v[0]][v[1]][v[2]]]
 unknown=[v for v in triples if (len(set(v))==3 and R[v[0]][v[1]][v[2]]==1)or(len(set(v))<3 and R[v[0]][v[1]][v[2]]==2)]
 extra=[v for v in triples if len(set(v))==3 and R[v[0]][v[1]][v[2]]==2]
 pos={t:i for i,t in enumerate(unknown)};m=len(unknown);cases=[]
 for extras in itertools.product([-2,0,2],repeat=len(extra)):
  given=dict(zip(extra,extras))
  def term(i,j,k):
   tri=tuple(sorted((i,j,k)));c=given.get(tri,R[i][j][k]);return c,1<<pos[tri]if tri in pos else 0
  eqs=set()
  for i,j,k,l in itertools.product(range(1,8),repeat=4):
   row=collections.defaultdict(int)
   for a in range(8):
    c,u=term(i,j,a);d,v=term(a,k,l);row[u^v]+=c*d
    c,u=term(j,k,a);d,v=term(i,a,l);row[u^v]-=c*d
   e=tuple(sorted((u,c)for u,c in row.items()if c));ne=tuple((u,-c)for u,c in e)
   if e:eqs.add(min(e,ne))
  eqs=sorted(eqs);supports=[{i for u,c in e for i in range(m)if u>>i&1}for e in eqs]
  if any(not x for x in supports):cases.append({'extras':extras,'constant_contradiction':True,'solutions':[]});continue
  left=set(range(m));order=[]
  while left:
   av=[x&left for x in supports if x&left];p=min(av,key=lambda x:(len(x),sorted(x)))if av else{min(left)};z=min(p,key=lambda i:(-sum(i in x for x in supports),i));order.append(z);left.remove(z)
  at={v:i for i,v in enumerate(order)};levels=[[]for _ in range(m+1)]
  for e,sp in zip(eqs,supports):levels[max(at[i]for i in sp)+1].append(e)
  sols=[];nodes=0
  def dfs(level,neg):
   nonlocal nodes
   nodes+=1
   if any(sum(-c if (u&neg).bit_count()%2 else c for u,c in e)for e in levels[level]):return
   if level==m:sols.append(neg);return
   dfs(level+1,neg);dfs(level+1,neg|(1<<order[level]))
  dfs(0,0)
  cases.append({'extras':extras,'unknown':unknown,'extra_triples':extra,'equations':len(eqs),'nodes':nodes,'solutions':[[unknown[i]for i in range(m)if neg>>i&1]for neg in sols]})
 return cases

def need(b,msg):
 if not b:raise ValueError(msg)
def fm(a,b):
 c=[0]*4
 for i,j in itertools.product(range(4),repeat=2):
  c[i^j]+=a[i]*b[j]*(3 if i&j&1 else 1)*(10 if i&j&2 else 1)
 return tuple(c)
def scalar(n):return(n,0,0,0)
def character_table(idx):
 if idx==630:
  offsets=[1,1,2,3,3,2,4,4]
  rational=[[1,-1,0,1,-1,0,0,0],[1,-1,1,-1,1,-1,0,0],[1,1,1,-1,-1,1,0,0],[1,-1,-2,-1,1,2,0,0]]
  small=[1,1,0,1,1,0,-1,-1]
 else:
  offsets=[1,1,3,4,4,3,2,2]
  rational=[[1,-1,1,0,0,-1,0,0],[1,-1,-1,1,-1,1,0,0],[1,1,1,-1,-1,1,0,0],[1,-1,-1,-2,2,1,0,0]]
  small=[1,1,-1,0,0,-1,1,1]
 rows=[[(n,0,sgn if i>=2 else 0,0)for i,n in enumerate(offsets)]for sgn in(1,-1)]
 rows += [[scalar(n)for n in row]for row in rational]
 rows += [[(n,sgn if i==6 else -sgn if i==7 else 0,0,0)for i,n in enumerate(small)]for sgn in(1,-1)]
 return rows

def verify(R,idx):
 n=8
 need(all(R[0][i][j]==int(i==j)and R[i][j][0]==int(i==j)for i,j in itertools.product(range(n),repeat=2)),'self-dual unit')
 need(all(R[i][j][k]==R[j][i][k]==R[i][k][j]for i,j,k in itertools.product(range(n),repeat=3)),'full symmetry')
 need(all(sum(R[i][j][a]*R[a][k][l]for a in range(n))==sum(R[j][k][a]*R[i][a][l]for a in range(n))for i,j,k,l in itertools.product(range(n),repeat=4)),'source associativity')
 cases=solve(R,idx)
 survivors=[(c['extras'],v)for c in cases for v in c['solutions']]
 need(survivors==[((),[])]if idx==630 else survivors==[((2,),[])],'only original signed quotient')
 rows=character_table(idx)
 need(len(set(map(tuple,rows)))==8,'eight distinct characters')
 for row in rows:
  need(all(fm(row[i],row[j])==tuple(sum(R[i][j][k]*row[k][a]for k in range(n))for a in range(4))for i,j in itertools.product(range(n),repeat=2)),'complete character homomorphisms')
 need(all(all(x!=(0,0,0,0)for x in row)for row in rows[:2]),'FP orbit has no zero simple dimensions')
 need(all(any(x==(0,0,0,0)for x in row)for row in rows[2:]),'every other character has a zero simple dimension')
 fs=[tuple(sum(fm(x,x)[a]for x in row)for a in range(4))for row in rows]
 need(fs==[(120,0,36,0),(120,0,-36,0)]+[scalar(k)for k in[4,6,6,12,12,12]],'formal codegrees')
 return {'id':f'R8_2_{idx}','tensor_sha256':hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest(),'signed_branches':cases,'character_basis':['1','sqrt3','sqrt10','sqrt30'],'characters':rows,'formal_codegrees':fs,'conclusion':'every categorification admits a spherical structure and has a pseudo-unitary Galois conjugate'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[3]);ap.add_argument('--output',type=Path);a=ap.parse_args()
 source=a.repo/'supplements/rank8/data/rank8_tables.txt.gz';sha=hashlib.sha256(source.read_bytes()).hexdigest();need(sha=='35a8d69e9af8c873b3003890218a35b38b792abb89c19066f6705bf9c1c1d1ed','source binding')
 rs=sorted((r for r in[json.loads(l.replace('{','[').replace('}',']'))for l in gzip.open(source,'rt')]if max(flat(r))==2),key=flat)
 report={'status':'PASS','classification_changes':0,'source_sha256':sha,'scope':'structural sphericality and Galois pseudo-unitarity only; no existence decision','cases':[verify(rs[i-1],i)for i in[630,671]]}
 if a.output:a.output.write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({'status':report['status'],'classification_changes':0,'ids':[c['id']for c in report['cases']]}))
if __name__=='__main__':main()
