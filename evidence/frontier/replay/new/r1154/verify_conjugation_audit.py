from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent
P=H.parents[1]/'prior/evidence/unresolved_retry_20261024/proofs/unresolved11_20261024/inputs'
def get(rid):
 j=json.loads((P/(rid+'.json')).read_text());R=j['fusion_tensor'];n=len(R)
 return R,[next(k for k in range(n)if R[i][k][0])for i in range(n)]
def triple(R,du,i,j):
 n=len(R);return[sum(R[i][j][t]*R[t][du[i]][k]for t in range(n))for k in range(n)]
R,du=get('R8_3_1768');v=triple(R,du,2,1)
if v!=[0,1,2,2,2,2,1,1]:raise RuntimeError('triple mismatch')
adj=[set()for _ in R]
for i in range(8):
 for j in range(8):
  for k,m in enumerate(triple(R,du,i,j)):
   if m%2:adj[j].add(k);adj[k].add(j)
components=[];seen=set()
for x in range(8):
 if x in seen:continue
 todo=[x];c=set()
 while todo:
  a=todo.pop()
  if a in c:continue
  c.add(a);todo.extend(adj[a]-c)
 components.append(sorted(c));seen|=c
if components!=[[0,2,3,5],[1,4,6,7]]:raise RuntimeError('graph mismatch')
receipt={'tensor_sha256':hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest(),'triple':v,'conjugation_parity_components':components,'inherited_indicator_vector':[1,-1,1,1,1,1,1,1],'contradicting_constituents':[6,7],'other_case_checks':{}}
for rid,eps in [('R8_3_1154',[1,0,0,-1,1,1,1,1]),('R6_8_1660',[1,1,1,1,-1,1]),('R8_3_941',[1,0,0,1,1,1,1,1]),('R8_3_928',[1,0,0,0,0,0,0,-1])]:
 R,du=get(rid);n=len(R);bad=[]
 for i in range(n):
  for j in range(n):
   if not eps[j]:continue
   V=triple(R,du,i,j)
   for k,m in enumerate(V):
    if eps[k] and eps[j]!=eps[k] and m%2:bad.append([i,j,k])
 if bad:raise RuntimeError((rid,bad))
 receipt['other_case_checks'][rid]={'indicator_vector':eps,'contradictions':bad}
(H/'conjugation_audit_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS: exact R1768 triple and parity graph; four other case comparisons')
