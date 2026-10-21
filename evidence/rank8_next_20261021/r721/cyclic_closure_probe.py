from pathlib import Path
import json,itertools
import sympy as s
repo=Path(__file__).resolve().parents[3]
r=json.loads((repo/'evidence/rank8_center_followup_20261021/r721_center_extension_receipt.json').read_text())
for c in r['case_results'][:4]:
 if 'matrices' not in c and 'witnesses' not in c:continue
 ws=[{'matrices':c['matrices'],'matching_size':None}] if 'matrices'in c else [next(x for x in c['witnesses'] if x['matching_size']==i)for i in range(3)]
 for w in ws:
  Ns=[s.eye(c['center_rank'])]+[s.Matrix(x)for x in w['matrices']];n=Ns[0].rows
  words=[(0,)]+[(i,)for i in range(1,5)]+list(itertools.combinations_with_replacement(range(1,5),2))
  ps=[Ns[a] if len(z)==1 else Ns[a]*Ns[b]for z in words for a in [z[0]]for b in [z[-1]]]
  W=s.Matrix.hstack(*(x[:,0]for x in ps));inds=W.rref()[1];V=W[:,inds];Ps=[ps[i]for i in inds]
  types=[i for i,k in enumerate(c['counts'])for _ in range(k)]
  groups=[[0],[1],[2],[3],[4]]+[[i+5 for i,t in enumerate(types)if t==k]for k in sorted(set(types))]
  print('CASE',n,w['matching_size'],groups)
  for g in groups[5:]:
   v=s.zeros(n,1)
   for i in g:v[i]=1
   x=V.gauss_jordan_solve(v)[0]
   N=sum((a*B for a,B in zip(x,Ps)),s.zeros(n))
   bad=[(i,j,str(N[i,j]))for i in range(n)for j in range(n)if N[i,j].q!=1 or N[i,j]<0]
   print('group',g,'bad',bad[:10], 'count',len(bad),'diag',list(N.diagonal()))
