"""Fresh rank-12 input binding, fusion axioms, embeddings, and route inventory."""
from pathlib import Path
from collections import Counter
import gzip,hashlib,itertools,json
import numpy as np

HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]/'prior_round'
FIRST=BASE/'prior_round/evidence/rank12-m1-offline-20261025'
def need(x,m):
    if not x:raise ValueError(m)
def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
def read(p):return json.loads(p.read_text())
data=read(FIRST/'tensors.json');ledger=read(BASE/'ledger.json')['records']
need(len(data)==len(ledger)==632,'census count')
with gzip.open(FIRST/'input/rank12_M1_verified/FusionRingMultiplicationTables.txt.gz','rt') as stream:
    lines=stream.readlines()
need(len(lines)==632,'original physical line count')
duals={}
for i,(line,row) in enumerate(zip(lines,ledger),1):
    rid=f'R12_1_{i}';R=json.loads(line.replace('{','[').replace('}',']'))
    need(row['id']==rid and row['input_line']==i,'permanent ID binding')
    need(R==data[rid] and digest(R)==row['tensor_sha256'],'original tensor/ledger hash')
    A=np.asarray(R,dtype=np.int64)
    need(A.shape==(12,12,12) and A.min()==0 and A.max()==1,'rank/multiplicity')
    need(np.array_equal(A[0],np.eye(12,dtype=int)) and np.array_equal(A[:,0],np.eye(12,dtype=int)),'unit')
    need(np.all(A[:,:,0].sum(axis=0)==1) and np.all(A[:,:,0].sum(axis=1)==1),'duality permutation')
    du=A[:,:,0].argmax(axis=1).tolist();need(all(du[du[j]]==j for j in range(12)),'involutive duality')
    need(np.array_equal(np.einsum('ija,akl->ijkl',A,A),np.einsum('jka,ial->ijkl',A,A)),'full associativity')
    need(all(R[a][b][c]==R[du[b]][du[a]][du[c]]==R[du[a]][c][b]==R[c][du[b]][a] for a,b,c in itertools.product(range(12),repeat=3)),'all reciprocity identities')
    duals[rid]=du
subs=read(FIRST/'subrings.json');count=0
for C in subs['classes']:need(digest(C['tensor'])==C['tensor_sha256'],'subring class digest')
for rec in subs['records']:
    R=data[rec['id']];du=duals[rec['id']]
    for e in rec['subrings']:
        J=e['subset'];p=e['source_to_class_basis_map'];T=subs['classes'][e['class_index']]['tensor'];n=len(J)
        need(J[0]==0 and len(set(J))==n and all(du[i] in J for i in J),'dual closed proper subring')
        need(p[0]==0 and sorted(p)==list(range(n)),'subring based map')
        need(all(not R[i][j][k] for i in J for j in J for k in range(12) if k not in J),'subring product closure')
        need(all(R[J[i]][J[j]][J[k]]==T[p[i]][p[j]][p[k]] for i,j,k in itertools.product(range(n),repeat=3)),'entire embedded tensor')
        count+=1
excluded=[r for r in ledger if r['status']=='excluded'];need(len(excluded)==438,'exclusion count')
parent_routes={'forced_group_theoretical_D120_exhaustion','central_class_induction_relative_indicator_traces'}
inventory=[]
for r in excluded:
    route=r['exclusion_route']
    inventory.append({'id':r['id'],'tensor_sha256':r['tensor_sha256'],'route':route,'proof_auditor':'parent' if route in parent_routes else 'audit_exclusions','proof_status':'pending fresh review','tensor_binding':'PASS'})
out={'status':'PASS','input_tensors':632,'closed_subring_embeddings':count,'excluded':438,'route_counts':dict(Counter(r['exclusion_route'] for r in excluded)),'assigned_here':sum(r['proof_auditor']=='audit_exclusions' for r in inventory),'records':inventory}
(HERE/'route_inventory.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='records'},indent=2))
