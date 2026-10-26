"""Independent exact audit of the two relative-transfer dimension-48 models."""
from pathlib import Path
from itertools import product
import json,time,hashlib
import numpy as np
from audit_graph_twist import audit,require
HERE=Path(__file__).resolve().parent

def sha(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()

def main():
    start=time.monotonic();rows=json.loads((HERE/'frozen/d48_positive_witnesses.json').read_text());out=[]
    for row in rows:
        G=np.array(row['group_table'],dtype=int);H=row['subgroup'];W=np.array(row['omega'],dtype=int);n=len(G);q=row['modulus']
        require(n==48 and q==8,'recorded group and phase orders')
        require(all(G[0,a]==G[a,0]==a for a in range(n)),'identity')
        require(all(sorted(G[a].tolist())==list(range(n)) and sorted(G[:,a].tolist())==list(range(n)) for a in range(n)),'Latin group table')
        require(all(G[G[a,b],c]==G[a,G[b,c]] for a,b,c in product(range(n),repeat=3)),'full group associativity')
        require(len(H)==4 and 0 in H and all(G[a,b] in H for a,b in product(H,repeat=2)),'actual subgroup of order four')
        require(not np.any(W[0]) and not np.any(W[:,0]) and not np.any(W[:,:,0]),'normalized three-cocycle')
        b=np.arange(n)[:,None,None];c=np.arange(n)[None,:,None];d=np.arange(n)[None,None,:]
        for a in range(n):
            delta=W[b,c,d]-W[G[a,b],c,d]+W[a,G[b,c],d]-W[a,b,G[c,d]]+W[a,b,c]
            require(not np.any(delta%q),'all 5308416 associator cocycle equations')
        require(all(int(W[a,b,c])==0 for a,b,c in product(H,repeat=3)),'strict subgroup algebra associativity')
        require(all(z[-1]==0 for z in row['psi']),'selected subgroup cochain is trivial')
        require(sha(row['omega'])==row['omega_sha256'],'frozen associator hash')
        require(sha(row['source_tensor'])==row['source_tensor_sha256'],'source tensor hash')
        require(sha(row['model_tensor'])==row['model_tensor_sha256'],'model tensor hash')
        adapted=dict(group_table=row['group_table'],subgroup=H,info={'objects':row['objects']},model_tensor=row['model_tensor'],matches=[dict(id=row['id'],basis_map_source_to_model=row['source_to_model'])])
        result=audit(adapted,lambda a,b,c:int(W[a,b,c]),modulus=q)
        result.update(id=row['id'],group_order=n,subgroup_order=len(H),cocycle_equations=n**4,modulus=q)
        out.append(result);print(result,flush=True)
    (HERE/'d48_independent.json').write_text(json.dumps(dict(status='PASS',records=out,seconds=time.monotonic()-start),indent=2)+'\n')

if __name__=='__main__':main()
