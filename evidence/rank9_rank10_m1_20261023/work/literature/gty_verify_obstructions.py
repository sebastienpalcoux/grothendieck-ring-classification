"""Independently reconstruct and verify arbitrary-complex Liptrap impossibility certificates."""
from pathlib import Path
import json,itertools,numpy as np
P=Path(__file__).resolve().parents[2]
D=json.load(open(P/'work/input_audit/tensors.json'))
C=json.load(open(P/'work/literature/gty_exact_obstructions.json'))
results={}
for rid,cert in C.items():
 N=np.array(D[rid]);n=len(N);dual=np.argmax(N[:,:,0],axis=1).tolist()
 S=[i for i in range(n) if sum(N[i,dual[i]])==1];M=[i for i in range(n) if i not in S]
 def prod(a,b):
  inds=np.flatnonzero(N[a,b]);assert len(inds)==1;return int(inds[0])
 H=[a for a in S if prod(a,M[0])==M[0]];hi={a:i for i,a in enumerate(H)}
 assert len(M)==2 and len(H)==4
 assert all([a for a in S if prod(a,m)==m]==H for m in M)
 assert all([a for a in S if prod(m,a)==m]==H for m in M)
 # Complete direct enumeration: symmetric normalized maps H² -> fourth roots.
 forms=[];positions=[(a,b) for a in range(1,4) for b in range(a,4)]
 for values in itertools.product(range(4),repeat=len(positions)):
  F=[[0]*4 for a in H]
  for (a,b),v in zip(positions,values):F[a][b]=F[b][a]=v
  if len(set(tuple(row) for row in F))!=4:continue
  if all((F[hi[prod(a,b)]][hi[c]]-F[hi[a]][hi[c]]-F[hi[b]][hi[c]])%4==0 for a,b,c in itertools.product(H,H,H)):
   forms.append(tuple(tuple(row) for row in F))
 forms.sort();pairs=list(itertools.product(forms,repeat=2));assert len(forms)==cert['form_count']
 keys=[(f,a,b,m) for f in ['chi','upsilon'] for a in S if a for b in S if b for m in M];ki={k:i for i,k in enumerate(keys)}
 rows=[];rhs=[];descriptions=[]
 def add(terms,b,desc):
  row=[0]*len(keys)
  for e,key in terms:
   if key in ki:row[ki[key]]+=e
  if any(row) or any(b):rows.append(row);rhs.append(b);descriptions.append(desc)
 for a,b,m in itertools.product(S,S,M):
  add([(1,('chi',b,a,dual[m])),(-1,('chi',a,b,prod(prod(a,m),b)))],[0]*len(pairs),['quasisymmetry',a,b,m])
 for a,b,c,m in itertools.product(S,S,S,M):
  add([(1,('upsilon',a,b,m)),(-1,('upsilon',a,b,prod(m,dual[c]))),(1,('chi',prod(a,b),c,m)),(-1,('chi',a,c,m)),(-1,('chi',b,c,prod(dual[a],m)))],[0]*len(pairs),['biderivation',a,b,c,m])
 for im,m in enumerate(M):
  for ia,a in enumerate(H):
   for ib,b in enumerate(H):
    add([(1,('chi',a,b,m))],[pair[im][ia][ib] for pair in pairs],['bicharacter_value',a,b,m])
 assert rows==cert['equation_matrix'] and rhs==cert['rhs_mod4']
 assert len(cert['form_pairs'])==len(pairs)
 witnesses=[]
 for c in cert['form_pairs']:
  j=c['form_pair_index'];comb=c['row_combination']
  assert all(sum(v*rows[i][k] for i,v in comb)==0 for k in range(len(keys)))
  exp=sum(v*rhs[i][j] for i,v in comb)%4
  assert exp and exp==c['right_side_mod4']
  witnesses.append({'form_pair_index':j,'forms':pairs[j],'right_side_mod4':exp,'equations':[[v,descriptions[i]] for i,v in comb]})
 assert sorted(c['form_pair_index'] for c in cert['form_pairs'])==list(range(len(pairs)))
 results[rid]={'all_complex_solutions_excluded':True,'number_of_form_pairs':len(pairs),'serfs':S,'lords':M,'stabilizer':H,'human_readable_witnesses':witnesses}
print({rid:{k:v for k,v in data.items() if k!='human_readable_witnesses'} for rid,data in results.items()})
(P/'work/literature/gty_obstruction_verification.json').write_text(json.dumps(results,indent=2)+'\n')
