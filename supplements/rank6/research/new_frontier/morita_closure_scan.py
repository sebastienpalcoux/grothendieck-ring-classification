import sys,json,itertools,time,signal
def alarm_handler(signum,frame):raise TimeoutError("per-branch hard deadline")
signal.signal(signal.SIGALRM,alarm_handler)
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'software'))
import numpy as np
import sympy as s
from full_morita_gram import *
from rings import permute
def iso(A,B):
 return next(((0,)+p for p in itertools.permutations(range(1,len(A))) if permute(A,(0,)+p)==B),None)

def frames(R,g,T,fixed,limit=10000,seconds=20):
 start=time.monotonic();labels,M=module_matrices(R,g,fixed,T);r=len(labels);G=full_gram(M)
 cols=first_columns(M,g);counts=Counter(cols);unique=sorted(counts);rank=G.rank()
 if rank!=len(cols):return None,{'reason':'nonfaithful_or_rank','rank':rank,'dual_rank':len(cols)}
 V=s.Matrix.hstack(*G.columnspace());ident=tuple(int(i==j) for i in range(r) for j in range(r));u=tuple(int(i==0) for i in range(r));counts[u]-=1
 ij=list(itertools.combinations_with_replacement(range(r*r),2));Gv=np.array([int(G[i,j])-ident[i]*ident[j] for i,j in ij],dtype=np.int64)
 lists=[]
 for c in unique:
  cs=set()
  for row in unique:cs.update(image_candidates(G,V,c,row))
  cs=[x for x in sorted(cs) if all(s.Matrix(r,r,x)*m==m*s.Matrix(r,r,x) for m in M)]
  options=[]
  for inds in itertools.combinations(range(len(cs)),counts[c]):
   vv=np.array([sum(cs[a][i]*cs[a][j] for a in inds) for i,j in ij],dtype=np.int64)
   if np.all(vv<=Gv):options.append((vv,[cs[a] for a in inds]))
  lists.append(options)
 lists.sort(key=len);out=[];nodes=[0]
 def search(q,res,chosen):
  nodes[0]+=1
  if time.monotonic()-start>seconds:raise TimeoutError('frame enumeration timeout')
  if q==len(lists):
   if not np.any(res):out.append([ident]+chosen)
   if len(out)>limit:raise TimeoutError('too many frames')
   return
  for v,cs in lists[q]:
   new=res-v
   if np.all(new>=0):search(q+1,new,chosen+cs)
 search(0,Gv,[])
 return out,{'rank':rank,'dual_rank':len(cols),'nodes':nodes[0],'frames':len(out),'options':list(map(len,lists))}

def tensor(B):
 r=int(len(B[0])**.5);m=len(B);V=s.Matrix.hstack(*[s.Matrix(v) for v in B]);piv=list(V.T.rref()[1]);W=V.extract(piv,range(m)).inv();N=[]
 mats=[s.Matrix(r,r,v) for v in B]
 for a in mats:
  row=[]
  for b in mats:
   z=(a*b).reshape(r*r,1);n=W*z.extract(piv,[0])
   if V*n!=z or any(not x.is_Integer or x<0 for x in n):return None
   row.append(list(map(int,n)))
  N.append(row)
 return N

census=json.load(open(ROOT/'data/census.json'));ledger={x['id']:x for x in json.load(open(ROOT/'data/decisions.json'))}
tensor_index={str(x['N']):x['id'] for x in census}
rows=[x for x in census if ledger[x['id']]['existence']['general']=='unknown']
output=ROOT/'research/new_frontier/morita_closure_scan.json'
report=json.load(open(output)) if output.exists() else []
completed={x['id'] for x in report}
for row in rows:
 if row['id'] in completed:continue
 R=row['N'];t0=time.monotonic();rec={'id':row['id'],'branches':[]}
 for g in invs(R):
  info=anti_representations(R,g)
  if not info:continue
  fixed,seed,nodes,reps=info
  for t,T in enumerate(reps):
   try:
    signal.alarm(8)
    Bs,meta=frames(R,g,T,fixed)
    rr={'g':g,'branch':t,**meta}
    if Bs is not None:
     nn=[tensor(B) for B in Bs];rr['nonfusion_frames']=nn.count(None);nn=[N for N in nn if N]
     seen=[]
     for N in nn:
      if not any(iso(N,V) is not None for V in seen):seen.append(N)
     rr['fusion_types']=[]
     for N in seen:
      matches=[(tensor_index[str(permute(N,(0,)+p))],list((0,)+p)) for p in itertools.permutations(range(1,len(N))) if str(permute(N,(0,)+p)) in tensor_index]
      rr['fusion_types'].append({'N':N,'matches':matches})
     if seen: print(row['id'],g,t,'TYPES',[x['matches'] for x in rr['fusion_types']],flush=True)
    signal.alarm(0)
    rec['branches'].append(rr)
   except (TimeoutError,ValueError) as e:
    signal.alarm(0)
    rec['branches'].append({'g':g,'branch':t,'error':str(e)})
 rec['seconds']=time.monotonic()-t0;report.append(rec)
 (ROOT/'research/new_frontier/morita_closure_scan.json').write_text(json.dumps(report,indent=2))
 print('DONE',row['id'],rec['seconds'],flush=True)
