"""Finite group-theoretical FP-type enumeration in dimension42.

All six groups of order42 and all their subgroups are enumerated directly.
Squarefree stabilizers have zero Schur multiplier; hence arbitrary allowed
associators do not change these projective representation degree lists.
The mathematical completeness reduction is in dimension84_obstruction.md.
"""
import argparse,collections,itertools,json
from pathlib import Path
OUT=Path(__file__).resolve().parent

def require(x,m):
 if not x:raise ValueError(m)

def group(kind,action):
 if kind=='cyclic':
  Q=list(range(6));qm=lambda x,y:(x+y)%6;rho=lambda x:pow(action,x,7)
 else:
  Q=list(itertools.permutations(range(3)));Q.sort(key=lambda p:(p!=(0,1,2),p));qm=lambda x,y:tuple(x[y[i]] for i in range(3));rho=lambda x:pow(action,sum(x[i]>x[j] for i in range(3) for j in range(i+1,3))%2,7)
 elems=[(a,q) for a in range(7) for q in Q];index={x:i for i,x in enumerate(elems)}
 table=[[index[((a+rho(q)*b)%7,qm(q,r))] for b,r in elems] for a,q in elems]
 require(all(table[0][i]==table[i][0]==i for i in range(42)),'identity')
 inverse=[next(j for j in range(42) if table[i][j]==table[j][i]==0) for i in range(42)]
 require(all(table[table[a][b]][c]==table[a][table[b][c]] for a in range(42) for b in range(42) for c in range(42)),'group associativity')
 return table,inverse,elems

def closure(T,generators):
 H={0};todo=list(generators)
 while todo:
  x=todo.pop()
  if x in H:continue
  old=list(H);H.add(x)
  for h in old+[x]:
   for y in (T[x][h],T[h][x]):
    if y not in H:todo.append(y)
 return frozenset(H)

def subgroups(T):
 seen={frozenset({0})};queue=[frozenset({0})]
 while queue:
  H=queue.pop()
  for g in range(len(T)):
   if g in H:continue
   K=closure(T,list(H)+[g])
   if K not in seen:seen.add(K);queue.append(K)
 return sorted(seen,key=lambda H:(len(H),tuple(sorted(H))))

def degrees(T,inv,H):
 remaining=set(H);classes=0
 while remaining:
  x=min(remaining);conjugacy={T[T[h][x]][inv[h]] for h in H};remaining-=conjugacy;classes+=1
 comm=closure(T,[T[T[T[x][y]][inv[x]]][inv[y]] for x in H for y in H]);linear=len(H)//len(comm)
 # Every subgroup has cyclic normal subgroup inside C7 and cyclic/S3
 # complement; Clifford theory permits only degrees1,2,3,6.
 solutions=[]
 for n2 in range(classes-linear+1):
  for n3 in range(classes-linear-n2+1):
   n6=classes-linear-n2-n3
   if linear+4*n2+9*n3+36*n6==len(H):solutions.append([1]*linear+[2]*n2+[3]*n3+[6]*n6)
 require(len(solutions)==1,('ambiguous degree data',len(H),classes,linear,solutions))
 return solutions[0]

def category_type(T,inv,H):
 remaining=set(range(42));out=[];cosets=[]
 while remaining:
  g=min(remaining);D={T[T[h][g]][k] for h in H for k in H};remaining-=D
  K=H&{T[T[g][h]][inv[g]] for h in H};ds=degrees(T,inv,K);scale=len(H)//len(K);out.extend(scale*d for d in ds)
  cosets.append({'representative':g,'size':len(D),'stabilizer':sorted(K),'stabilizer_degrees':ds,'scale':scale})
 require(sum(d*d for d in out)==42,'double-coset dimension')
 return sorted(out),cosets

def enumerate_all():
 records=[];wanted=[[1,1,2,6],[1]*6+[6],[1,1,2]+[3]*4,[1]*6+[3]*4]
 for kind,action in [('cyclic',1),('cyclic',6),('cyclic',2),('cyclic',3),('symmetric',1),('symmetric',6)]:
  T,inv,elems=group(kind,action);subs=subgroups(T);cases=[]
  for H in subs:
   ds,cosets=category_type(T,inv,H)
   if ds in wanted:
    cases.append({'subgroup':sorted(H),'order':len(H),'type':ds,'double_cosets':cosets})
  records.append({'group_kind':kind,'action_multiplier':action,'order':42,'subgroup_count':len(subs),'wanted_cases':cases})
 types=sorted({tuple(x['type']) for r in records for x in r['wanted_cases']})
 require(tuple(wanted[0]) not in types and tuple(wanted[2]) not in types,'forbidden42base appeared')
 return {'result':'PASS','dimension':42,'groups':records,'possible_requested_types':[list(x) for x in types],'scope':'all six order42 groups and all subgroups; arbitrary projective stabilizers reduce to ordinary representations by squarefreeness'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args();out=enumerate_all();path=OUT/'dimension42_group_types.json'
 if args.write:path.write_text(json.dumps(out,separators=(',',':'))+'\n')
 else:require(json.loads(path.read_text())==out,'stored42enumeration differs')
 print('PASS dimension42',len(out['groups']),'groups',sum(x['subgroup_count'] for x in out['groups']),'subgroups')
if __name__=='__main__':main()
