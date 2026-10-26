from pathlib import Path
import itertools,json,sys,time,collections,heapq
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1]/'prior_round/prior_round/evidence/rank12-m1-offline-20261025';sys.path.insert(0,str(BASE));import feudal
sys.path.insert(0,str(BASE/'sources/work/rank11'));import common

def tensor(u,nonsplit=1):
 G=list(itertools.product(range(4),range(2),range(2)));O=[(i,j)for i in range(8)if i%2 for j in range(2)];labs=[('g',)+x for x in G]+[('m',)+x for x in O];index={x:i for i,x in enumerate(labs)}
 def gm(g,h):
  a,b,c=g;d,e,f=h;return((a+(-1)**b*d)%4,b^e,(c+f+nonsplit*b*d)%2)
 def um(g,h):return((g[0]+u**g[1]*h[0])%8,g[1]^h[1])
 def ud(x):return(2*x[1],x[2])if x[0]=='g'else x[1:]
 n=len(labs);R=[[[0]*n for _ in range(n)]for _ in range(n)]
 for i,x in enumerate(labs):
  for j,y in enumerate(labs):
   if x[0]==y[0]=='g':R[i][j][index[('g',)+gm(x[1:],y[1:])]]=1
   else:
    a,b=um(ud(x),ud(y))
    if a%2:R[i][j][index[('m',a,b)]]=1
    else:
     for c in range(2):R[i][j][index[('g',a//2,b,c)]]=1
 common.validate(R);return R,labs

def sparse_solve(A,B,q,n):
 rows=[{k:v%q for k,v in row.items()if v%q}for row in A];rhs=[int(b)%q for b in B];active=set(range(len(rows)));free=set(range(n));steps=[];stats=[]
 while q>1:
  occ={k:set()for k in free};heap=[]
  for i in active:
   for k in rows[i]:occ[k].add(i)
   if any(v%2 for v in rows[i].values()):heapq.heappush(heap,(len(rows[i]),i))
  units=0
  while heap:
   length,i=heapq.heappop(heap)
   if i not in active or len(rows[i])!=length:continue
   odds=[k for k,v in rows[i].items()if v%2]
   if not odds:continue
   k=min(odds,key=lambda k:len(occ[k]));v=pow(rows[i][k],-1,q);p={a:b*v%q for a,b in rows[i].items()};b=rhs[i]*v%q;active.remove(i);free.remove(k)
   for a in rows[i]:occ[a].discard(i)
   for j in list(occ[k]):
    row=rows[j];v=row[k]
    for a,w in p.items():
     old=row.get(a,0);new=(old-v*w)%q
     if new:
      row[a]=new
      if not old:occ[a].add(j)
     elif old:del row[a];occ[a].discard(j)
    rhs[j]=(rhs[j]-v*b)%q
    if not row:
     if rhs[j]:return None,stats+[dict(modulus=q,contradiction=True)]
     active.remove(j)
    elif any(v%2 for v in row.values()):heapq.heappush(heap,(len(row),j))
   del p[k];steps.append((k,p,b,q));units+=1
  if any(rhs[i]%2 for i in active):return None,stats+[dict(modulus=q,odd_rhs=True,unit_pivots=units)]
  stats.append(dict(modulus=q,unit_pivots=units,remaining=len(active),free=len(free)));print('ELIM',stats[-1],flush=True)
  for i in active:rows[i]={k:v//2 for k,v in rows[i].items()};rhs[i]//=2
  q//=2
 x=[0]*n
 for k,p,b,q0 in reversed(steps):x[k]=(b-sum(v*x[j]for j,v in p.items()))%q0
 return x,stats

def main():
 for u in [7,3]:
  R,labs=tensor(u);z=feudal.setup(R,variable_tau=True);q=16;A=z['equations'];B=[b[0]*(q//2)for b in z['B']];start=time.monotonic();x,stats=sparse_solve(A,B,q,len(z['keys']));print('RESULT',u,x is not None,'seconds',time.monotonic()-start,flush=True)
  row=dict(u=u,nonsplit=True,tensor=R,labels=labs,equation_count=len(A),variable_count=len(z['keys']),modulus=q,stats=stats)
  if x is not None:
   common.require(all((sum(v*x[k]for k,v in a.items())-b)%q==0 for a,b in zip(A,B)),'all original Liptrap equations')
   row['certificate']=dict(kind='liptrap_unitary_model',modulus=q,serfs=z['S'],lords=z['M'],stabilizer=z['H'],tau_times_tau_dual='1/2',tau='phase_times_inverse_square_root',bicharacter_assignment=[0]*8,phase_values=[list(k)+[x[i]]for i,k in enumerate(z['keys'])],reference='Liptrap 1002.3166v2 Definition4.3, Theorem4, Lemma5.4')
   row['verification']=feudal.check_positive(R,row['certificate'])
  (HERE/('nonsplit_ising_'+str(u)+'.json')).write_text(json.dumps(row,indent=2)+'\n')
if __name__=='__main__':main()
