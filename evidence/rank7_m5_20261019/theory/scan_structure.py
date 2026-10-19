import json,sys,itertools,collections,numpy as np,sympy as s
from pathlib import Path
P=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(P/'supplements/rank7/software'))
from prepare import key,dual
from subring_descent import closed_subrings
from rings import codegree_factors

def sig(R):return sorted(tuple(sorted(sum(row) for row in M)) for M in R)
rows=json.load(open(P/'supplements/rank7/output/m5/survivors.json'))
r6=json.load(open(P/'supplements/rank6/data/census.json'));d6={d['id']:d for d in json.load(open(P/'supplements/rank6/data/decisions.json'))}; out=[]
for a in rows:
 R=a['tensor'];du=dual(R);A=np.array(R);v=np.linalg.eigh(np.sum(A,axis=0))[1][:,-1];v=v/v[0];D=sum(v*v)
 subs=list(closed_subrings(R));matches=[]
 for J,S in subs:
  if len(J)==6:
   ss=sig(S);ks=key(S); rs=[b for b in r6 if sig(b['N'])==ss and key(b['N'])==ks];assert len(rs)==1,(a['id'],len(rs));b=rs[0];dec=d6[b['id']]
   perm=next(p for q in itertools.permutations(range(1,6)) if (p:=(0,)+q) and [[[S[i][j][k] for k in p] for j in p] for i in p]==b['N'])
   matches.append({'id':b['id'],'subset':list(J),'permutation':perm,'status':dec['status'],'certificate':dec.get('certificate'),'models':dec.get('models')})
 out.append({'id':a['id'],'commutative':a['commutative'],'dimensions_approx':v.tolist(),'dimension_approx':D,'invertibles':[i for i in range(7) if all(sum(row)==1 for row in R[i])],'duality':du,'subrings':[list(J) for J,S in subs],'codegree_factors':[[str(p.as_expr()),m] for p,m in codegree_factors(R)],'rank6_matches':matches})
 print(a['id'],round(D,8),len(subs),[(b['id'],b['status']) for b in matches],flush=True)
Path(__file__).with_name('structural_invariants.json').write_text(json.dumps(out,indent=2)+'\n')
print('DONE',len(out))
