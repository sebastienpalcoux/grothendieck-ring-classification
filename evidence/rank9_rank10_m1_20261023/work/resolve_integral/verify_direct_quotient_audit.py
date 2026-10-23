"""Independent direct quotient audit; does not import the construction solver."""
from pathlib import Path
from itertools import product,permutations
from collections import Counter
import hashlib,json
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'work/input_audit/tensors.json').read_text())
PROPOSED=json.loads((ROOT/'work/resolve_rank9_neargroup/direct_quotient.json').read_text())
D=(1,1,1,1,2,2,2,2,2);A=(0,1,3,2,4,6,5,8,7)
TRIPLES=list(product(range(9),repeat=3))
def need(x,msg):
 if not x:raise ValueError(msg)
def dual(T):
 ans=[]
 for i in range(9):
  z=[j for j in range(9)if T[i][j][0]];need(len(z)==1,'source dual');ans.append(z[0])
 return tuple(ans)
def digest(T):return hashlib.sha256(bytes(x for row in T for col in row for x in col)).hexdigest()
def build_F(C,cd,g):
 p=[]
 for i in range(9):
  z=[j for j in range(9)if C[g][i][j]];need(len(z)==1,'sign action');p.append(z[0])
 need(all(p[p[i]]==i for i in range(9)),'sign square')
 oo=sorted({tuple(sorted({i,p[i]}))for i in range(9)})
 iv=[o for o in oo if cd[o[0]]==1]
 lo=[o for o in oo if cd[o[0]]==2]
 hi=[o for o in oo if cd[o[0]]==4]
 if len(iv)!=2 or any(len(o)!=2 for o in iv):return None
 if sorted(map(len,lo))!=[1,2]or len(hi)!=2 or any(len(o)!=1 for o in hi):return None
 groups=[(iv[0],[0]),(iv[1],[1]),(next(o for o in lo if len(o)==1),[2,3]),(next(o for o in lo if len(o)==2),[4]),(hi[0],[5,6]),(hi[1],[7,8])]
 F=[[0]*9 for i in range(9)]
 for src,dst in groups:
  for i in src:
   for j in dst:F[i][j]=1
 need(F[0]==[1]+[0]*8,'unit F')
 need(all(sum(F[i][j]*D[j]for j in range(9))==cd[i]for i in range(9)),'F dimensions')
 return F

def enumerate_duals(C,F):
 cs=dual(C);ans=[]
 for p in permutations(range(1,4)):
  for q in permutations(range(4,9)):
   s=(0,)+p+q
   if any(s[s[i]]!=i or s[A[i]]!=A[s[i]]for i in range(9)):continue
   if all(F[i][j]==F[cs[i]][s[j]]for i,j in product(range(9),repeat=2)):ans.append(s)
 return ans

def equations(C,F,s):
 # Compute equality classes by breadth-first orbits, rather than union-find.
 unseen=set(TRIPLES);classes=[];at={}
 while unseen:
  start=min(unseen);todo=[start];orb={start};unseen.remove(start)
  for i,j,k in todo:
   for z in [(s[i],k,j),(k,s[j],i),(A[i],A[j],A[k])]:
    if z not in orb:orb.add(z);todo.append(z);unseen.remove(z)
  n=len(classes);classes.append(orb)
  for z in orb:at[z]=n
 E=set()
 def put(terms,rhs):
  c=Counter()
  for z,w in terms:c[at[z]]+=w
  E.add((tuple(sorted(c.items())),rhs))
 for i,j in product(range(9),repeat=2):
  put([((0,i,j),1)],int(i==j));put([((i,0,j),1)],int(i==j))
  put([((i,j,0),1)],int(s[i]==j))
  put([((i,j,k),D[k])for k in range(9)],D[i]*D[j])
  for k in range(9):
   put([((a,b,k),1)for a,b in product(range(9),repeat=2)if F[i][a]and F[j][b]],sum(C[i][j][h]*F[h][k]for h in range(9)))
 E=sorted(E);bounds=[999]*len(classes)
 for terms,rhs in E:
  need(rhs>=0 and all(w>0 for v,w in terms),'positive equation')
  for v,w in terms:bounds[v]=min(bounds[v],rhs//w)
 need(max(bounds)<=1,'nonnegative equations do not force binary coefficients')
 return at,E,bounds

def enumerate_linear(at,E,bounds):
 answers=[];nodes=0
 def rec(x):
  nonlocal nodes
  nodes+=1
  while True:
   changed=False;unknown=set()
   for terms,rhs in E:
    u=[]
    for v,w in terms:
     if x[v]<0:u.append((v,w));unknown.add(v)
     else:rhs-=w*x[v]
    total=sum(w for v,w in u)
    if rhs<0 or rhs>total:return
    for v,w in u:
     val=0 if rhs<w else 1 if rhs>total-w else -1
     if val<0:continue
     if x[v]<0:x[v]=val;changed=True
     elif x[v]!=val:return
   if not changed:break
  if unknown:
   v=min(unknown)
   for val in [0,1]:
    y=x[:];y[v]=val;rec(y)
  else:
   need(all(t>=0 for t in x),'unconstrained variable')
   answers.append([[[x[at[i,j,k]]for k in range(9)]for j in range(9)]for i in range(9)])
 rec([0 if b==0 else -1 for b in bounds])
 return nodes,answers

def associative(T):
 return all(sum(T[i][j][x]*T[x][k][l]for x in range(9))==sum(T[j][k][x]*T[i][x][l]for x in range(9))for i,j,k,l in product(range(9),repeat=4))

def main():
 old={r['source']:r for r in PROPOSED['sources']};report=[]
 for rid in ['R9_1_12','R9_1_62','R9_1_87','R9_1_108']:
  C=DATA[rid]
  # Obtain dimensions from the input audit, but check every multiplicativity equation.
  aud=json.loads((ROOT/'work/input_audit/audit.json').read_text())
  sq=next(r['squared_fp_dimensions_exact']for r in aud['9']['rings']if r['id']==rid)
  cd=[{1:1,4:2,16:4}[x]for x in sq]
  need(all(sum(C[i][j][k]*cd[k]for k in range(9))==cd[i]*cd[j]for i,j in product(range(9),repeat=2)),'source dimensions')
  fs=[(g,F)for g in range(1,9)if cd[g]==1 and (F:=build_F(C,cd,g))is not None]
  need(len(fs)==1,'unique profile sign');g,F=fs[0]
  need(g==old[rid]['sign']and F==old[rid]['restriction'],'independent F mismatch')
  ss=enumerate_duals(C,F);obs={tuple(b['dual']):b for b in old[rid]['dual_branches']}
  need(set(ss)==set(obs),'missing dual branch');rows=[]
  for s in ss:
   at,E,bounds=equations(C,F,s);nodes,linear=enumerate_linear(at,E,bounds)
   good=[T for T in linear if associative(T)];stored=obs[s]
   need(len(linear)==stored['linear_completions'],'linear enumeration mismatch')
   need({digest(T)for T in good}=={digest(z['tensor'])for z in stored['solutions']},'associative enumeration mismatch')
   # R117 appears only here, after every admissible completion is generated.
   for z in stored['solutions']:
    T=z['tensor'];p=z['quotient_to_R117'];B=DATA['R9_1_117']
    need(sorted(p)==list(range(9))and p[0]==0,'based permutation')
    need(all(T[i][j][k]==B[p[i]][p[j]][p[k]]for i,j,k in TRIPLES),'R117 isomorphism')
   rows.append({'dual':s,'variables':len(bounds),'zero_bounds':bounds.count(0),'one_bounds':bounds.count(1),'independent_nodes':nodes,'linear_completions':len(linear),'associative_completions':len(good),'solution_sha256':sorted(digest(T)for T in good)})
  report.append({'source':rid,'sign':g,'restriction':F,'branches':rows})
  print(rid,'PASS',len(ss),'dual branches,',sum(r['associative_completions']for r in rows),'associative completions')
 out={'status':'PASS','method':'Independent canonical F, permutation enumeration of all dualities, equality-class orbit BFS, nonnegative coefficient bounds, interval-only binary backtracking, full associativity and explicit R117 maps. No solver imports or census filter.','sources':report}
 (HERE/'direct_quotient_audit.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
