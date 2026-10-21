"""Exact necessary module-action row completion for all induction factors."""
import json,time,collections
import sympy as s
from integral_gram import bounded_solutions
from gram_discovery import HERE,REPO,require
FLOORS={
 'R8_3_65':[1,1,1,11,11,11,11,1],
 'R8_3_1768':[1,1,11,12,13,13,12,11],
 'R8_3_1795':[1,1,12,13,13,13,13,12],
 'R8_3_3472':[1,13,13,14,13,15,15,15],
}
# Matrices on module simple classes have nonnegative integer entries; their
# spectral radius is FPdim(X_i), and M_{i*}=M_i^T. Therefore every entry is
# at most floor FPdim(X_i), without a unitarity assumption.
def row_check(R,a,V,ns,di):
 active=[j for j,n in enumerate(ns)if n]; W=[V[j]for j in active];mult=[ns[j]for j in active]
 A=s.Matrix(W).T
 for uidx,u in enumerate(W):
  for i in sorted(range(1,8),key=lambda i:di[i]):
   # M_i B=B N_i^T and its column 0 fixes M_i[r,0]=B[r,i].
   b=[sum(u[k]*R[i][j][k]for k in range(8))-u[i]*a[j]for j in range(8)]
   if any(x<0 for x in b):return {'kind':'negative_rhs','row_type_index':active[uidx],'simple':i,'rhs':b}
   bounds=[min([n*di[i]]+[b[k]//v[k]for k in range(8)if v[k]])for v,n in zip(W,mult)]
   sol,meta=bounded_solutions(A,b,bounds)
   if not sol:return {'kind':'integer_row_obstruction','row_type_index':active[uidx],'simple':i,'rhs':b,'bounds':bounds,'enumeration':meta}
 return None

def run():
 source={r['id']:r for r in json.loads((REPO/'evidence/rank8_m3_20261021/pipeline/census_m3.json').read_text())}
 recs=json.loads((HERE/'integral_gram.json').read_text());out=[]
 for rec in recs:
  t=time.monotonic();R=source[rec['id']]['tensor'];a=rec['algebra_object'];V=rec['vectors'];checks=[]
  for fi,ns in enumerate(rec['all_multiplicities']):
   bad=row_check(R,a,V,ns,FLOORS[rec['id']]);checks.append({'factor_index':fi,'obstruction':bad})
  survive=[c['factor_index']for c in checks if c['obstruction']is None]
  result={'id':rec['id'],'candidate_index':rec['candidate_index'],'algebra_object':a,'factor_count':len(checks),'surviving_factor_indices':survive,'factor_checks':checks}
  out.append(result);print(rec['id'],rec['candidate_index'],len(checks),len(survive),round(time.monotonic()-t,3),flush=True)
  (HERE/'module_rows.json').write_text(json.dumps(out,default=int,separators=(',',':'))+'\n')
 return out
if __name__=='__main__':run()
