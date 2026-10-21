"""Morita closure with the entire canonical module-dimension profile."""
import json,collections
import sympy as s
from gram_discovery import HERE,REPO,require
from morita_closure import DATA,dim,mul,div,enc

def run():
 recs={(x['id'],x['candidate_index']):x for x in json.loads((HERE/'integral_gram.json').read_text())};closure=json.loads((HERE/'morita_closure.json').read_text());source={x['id']:x for x in json.loads((REPO/'evidence/rank8_m3_20261021/pipeline/census_m3.json').read_text())};out={}
 for rid,rec in closure.items():
  n,ds=DATA[rid];R=source[rid]['tensor'];dual=[next(j for j in range(8)if R[i][j][0])for i in range(8)];factors=[]
  for a in rec['survivors']:
   x=recs[(rid,a['candidate_index'])];ad=dim(x['algebra_object'],ds)
   for fi in a['factor_indices']:
    ns=x['all_multiplicities'][fi];B=[x['algebra_object']]+[v for v,k in zip(x['vectors'],ns)for _ in range(k)];ts=tuple(sorted(div(mul(dim(v,ds),dim(v,ds),n),ad,n)for v in B));M=s.Matrix(B)
    f={'candidate_index':a['candidate_index'],'factor_index':fi,'profile':ts,'root_dimension':ad,'B':B,'full_rank_action':None}
    if M.rank()==M.rows:
     Q=M.T*(M*M.T).inv();actions=[M*s.Matrix(R[i]).T*Q for i in range(8)]
     require(all(all(z.q==1 and z>=0 for z in U)for U in actions),'full rank nonnegative integral')
     require(actions[0]==s.eye(M.rows),'unit action')
     require(all(actions[dual[i]]==actions[i].T for i in range(8)),'module duality')
     require(all(actions[i]*actions[j]==sum((R[i][j][k]*actions[k]for k in range(8)),s.zeros(M.rows))for i in range(8)for j in range(8)),'full fusion relations')
     f['full_rank_action']=[U.tolist()for U in actions]
    factors.append(f)
  roots=collections.defaultdict(set)
  for f in factors:roots[f['profile']].add(f['root_dimension'])
  removed=[];surv=[]
  for f in factors:
   missing=sorted(set(f['profile'])-roots[f['profile']]);f['profile']=[enc(t)for t in f['profile']];f['root_dimension']=enc(f['root_dimension'])
   if missing:removed.append({'candidate_index':f['candidate_index'],'factor_index':f['factor_index'],'missing_rebased_root_dimensions':[enc(t)for t in missing]})
   else:surv.append(f)
  out[rid]={'removed_factors':removed,'surviving_factors':surv,'surviving_algebras':len({f['candidate_index']for f in surv}),'factor_count':len(surv),'profile_count':len({tuple(tuple(t)for t in f['profile'])for f in surv})}
  print(rid,'algebras',out[rid]['surviving_algebras'],'factors',len(surv),'profiles',out[rid]['profile_count'],'unique full actions',sum(f['full_rank_action']is not None for f in surv),flush=True)
 (HERE/'profile_closure.json').write_text(json.dumps(out,default=int,separators=(',',':'))+'\n')
 return out
if __name__=='__main__':run()
