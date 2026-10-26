"""Two independent exact constructions of the accepted order-48 models."""
from pathlib import Path
import itertools,json,sys,time
import numpy as np
BASE=Path(__file__).resolve().parents[2]/'rank12-m1-offline-20261025';OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE));import group_models as gm
import common
from twisted_h4_matrix import construct

def main():
    start=time.monotonic();D=json.loads((BASE/'tensors.json').read_text());rows=json.loads((OUT/'order48_models.json').read_text());ids=[]
    common.require({r['id']for r in rows}=={'R12_1_30','R12_1_417'},'accepted model inventory')
    for row in rows:
        rid=row['id'];m=row['model'];G=m['parameters']['group_table'];H=m['parameters']['subgroup'];A=np.array(G,dtype=np.int64)
        common.require(A.shape==(48,48)and np.array_equal(A[0],np.arange(48))and np.array_equal(A[:,0],np.arange(48)),'group unit and order')
        common.require(all(np.array_equal(A[A[a,:],:],A[a,A])for a in range(48)),'all group associativity equations')
        common.require(all(any(G[a][b]==G[b][a]==0 for b in range(48))for a in range(48)),'all group inverses')
        common.require(len(H)==4 and H==gm.subgroup(G,H),'subgroup closure')
        M,info=gm.fusion(G,H);common.require(M is not None,'ordinary complete convolution')
        common.validate(M);common.require(M==m['model_tensor'],'convolution agrees with stored model')
        B,binfo=construct(G,H,lambda a,b,c:0);common.require(B is not None,'explicit complete bimodule construction')
        common.validate(B);common.require(common.based_iso(B,M)is not None,'independent balanced quotient tensor')
        p=m['basis_map_source_to_model'];common.require(p[0]==0 and sorted(p)==list(range(12)),'unit-preserving based bijection')
        common.require(all(D[rid][i][j][k]==M[p[i]][p[j]][p[k]]for i,j,k in itertools.product(range(12),repeat=3)),'all 1728 input/model coefficients')
        ids.append(rid)
    out=dict(status='PASS',model_ids=ids,independent_algorithms=['equivariant-bundle character convolution','actual graded subgroup bimodules and balanced tensor quotients'],coefficients_checked_per_model=1728,optimized_python=not __debug__,elapsed_seconds=time.monotonic()-start)
    (OUT/('verification_optimized.json'if not __debug__ else'verification.json')).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
