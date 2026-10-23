import json,itertools
from pathlib import Path
import sympy as s
from sympy.matrices.normalforms import smith_normal_form
P=Path(__file__).resolve().parent
for kind in ['P','Q']:
 d=json.loads((P/f'{kind}_soft_aut_support.json').read_text());R=d['tensor'];V=list(map(tuple,d['variables']));idx={v:i for i,v in enumerate(V)}
 A=s.Matrix([row for row,rec in zip(d['constraints'],d['nonzero_F_support_used']) if rec[-1]=='singleton']);rank=A.rank();S0=smith_normal_form(A,domain=s.ZZ);base_invs=[abs(S0[i,i]) for i in range(min(S0.shape)) if S0[i,i]]
 if rank!=12 or base_invs!=[1]*12:raise RuntimeError('base lattice not primitive rank12')
 gauge=s.Matrix([[int(a==v)+int(b==v)-int(c==v) for v in [1,2,3]] for a,b,c in V])
 if gauge.rank()!=3 or A*gauge!=s.zeros(A.rows,3):raise RuntimeError('gauge dimension or invariance')
 K=s.Matrix.hstack(*A.nullspace());classes={}
 for a,b,c,eout in itertools.product(range(4),repeat=4):
  E=[e for e in range(4) if R[a][b][e] and R[e][c][eout]];F=[f for f in range(4) if R[b][c][f] and R[a][f][eout]]
  for e in E:
   for f in F:
    v=[0]*len(V)
    for t,sgn in [((a,b,e),1),((e,c,eout),1),((b,c,f),-1),((a,f,eout),-1)]:
     if t in idx:v[idx[t]]+=sgn
    proj=tuple(s.Matrix([v])*K)
    if any(proj):classes.setdefault(proj,v)
 bad=[];stats={};valid=[]
 for (p,v),(q,w) in itertools.combinations(classes.items(),2):
  if s.Matrix([p,q]).rank()<2:continue
  M=A.col_join(s.Matrix([v,w]));S=smith_normal_form(M,domain=s.ZZ);invs=[abs(S[i,i]) for i in range(min(S.shape)) if S[i,i]]
  mx=int(max(invs));stats[mx]=stats.get(mx,0)+1
  if mx!=1:bad.append([list(map(str,p)),list(map(str,q)),list(map(int,invs))])
 if bad or len(classes)!=(6 if kind=='P' else 4) or stats!={1:(12 if kind=='P' else 4)}:raise RuntimeError('universal primitive pair verification failed')
 print(kind,'base rank',rank,'nonzero quotientclasses',len(classes),'rank14pairSmithcounts',stats,'bad',bad[:3])
 (P/f'{kind}_soft_aut_universal.json').write_text(json.dumps({'kind':kind,'base_rank':rank,'base_smith_invariants':list(map(int,base_invs)),'gauge_rank':gauge.rank(),'all_nonzero_quotient_classes':[{'projection':list(map(str,p)),'row':v} for p,v in classes.items()],'rank14_pair_smith_counts':stats,'bad_pairs':bad},indent=2)+'\n')
