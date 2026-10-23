#!/usr/bin/env python3
import json,itertools
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent
receipts=[]
for k in [21,114,115,152,153,179]:
 d=json.loads((P/f'R10_1_{k}_module.json').read_text());basis=[s.Matrix(8,8,list(map(s.sympify,v))) for v in d['commutant_basis']];z=s.symbols('z:'+str(len(basis)));B=sum((t*b for t,b in zip(z,basis)),s.zeros(8));out=[];cases=[]
 if len(basis)!=12:raise RuntimeError('wrong commutant dimension')
 for m in range(8):
  v=next(iter(s.linsolve([B[i,0]-int(i==m) for i in range(8)],z)));M=B.subs(dict(zip(z,v)));free=sorted(M.free_symbols,key=str);sol=[]
  # Each free parameter is a distinct entry of B, so nonnegative.
  # A safe PF bound over all matrix entries for dimension <=delta² is <34.
  # Linear nonnegativity often pins a parameter to <=1; derive scalar bounds.
  
  if len(free)!=4:raise RuntimeError('wrong affine dimension')
  entry_positions={str(t):[[i,j] for i in range(8) for j in range(8) if M[i,j]==t] for t in free}
  for t in free:
   if not any(x==t for x in M):raise RuntimeError('parameter is not an actual matrix entry')
  if not 12*12*2 < 17*17:raise RuntimeError('FP entry bound')
  bounds={t:[0,33] for t in free}
  changed=True
  while changed:
   changed=False
   for x in M:
    poly=s.Poly(x,*free);coeff={t:poly.coeff_monomial(t) for t in free};const=poly.coeff_monomial(1)
    for t,a in coeff.items():
     if not a:continue
     maxi=const+sum(b*(bounds[u][1] if b>0 else bounds[u][0]) for u,b in coeff.items() if u!=t)
     if a>0:
      lo=max(bounds[t][0],int(s.ceiling(-maxi/a)))
      if lo!=bounds[t][0]:bounds[t][0]=lo;changed=True
     else:
      hi=min(bounds[t][1],int(s.floor(-maxi/a)))
      if hi!=bounds[t][1]:bounds[t][1]=hi;changed=True
  for vals in itertools.product(*(range(bounds[t][0],bounds[t][1]+1) for t in free)):
   mat=M.subs(dict(zip(free,vals)))
   if all(x.is_Integer and x>=0 for x in mat):sol.append(mat)
  out.extend((m,a) for a in sol)
  cases.append({'module_index':m,'free_parameters':[str(t) for t in free],'parameter_entry_positions':entry_positions,'initial_bounds':[0,33],'propagated_bounds':{str(t):bounds[t] for t in free},'candidate_count':len(sol)})
  print(k,'m',m,'bounds',bounds,'count',len(sol),'dualpos',[[j for j,x in enumerate(a[0,:]) if x] for a in sol])
 
 T=s.eye(8);T.row_swap(4,5);T.row_swap(6,7)
 if len(out)!=16:raise RuntimeError('wrong candidate count')
 if not all(m==out[j^1][0] and B*T==out[j^1][1] and B!=B*T for j,(m,B) in enumerate(out)):raise RuntimeError('left equivariance sign does not exchange both candidates')
 receipts.append({'id':d['id'],'commutant_dimension':12,'affine_dimension_per_unit_column':4,'unit_column_cases':cases,'candidate_count':16,'left_sign_pairs':[[j,j+1] for j in range(0,16,2)],'sign_pair_check':'B_j*T=B_(j xor 1), with distinct matrices'})
 (P/f'R10_1_{k}_dual_action_candidates.json').write_text(json.dumps({'id':d['id'],'candidates':[{'module_index':m,'matrix':[list(map(int,row)) for row in a.tolist()]} for m,a in out]},indent=2)+'\n')
(P/'commutant_completeness_receipt.json').write_text(json.dumps({'initial_integer_entry_bound':33,'exact_bound':'delta^4=17+12sqrt(2)<34, because 288<289','cases':receipts},indent=2)+'\n')
