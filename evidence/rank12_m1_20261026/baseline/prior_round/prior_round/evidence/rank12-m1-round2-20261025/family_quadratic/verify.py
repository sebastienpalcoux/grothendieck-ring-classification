"""Independent exact replay of four categorical identifications; no discovery search."""
from pathlib import Path
import hashlib,itertools,json,time
from triality import source_tensor,zest,require

ROOT=Path(__file__).resolve().parent
def sha(R):return hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
def main():
    start=time.monotonic();data=json.loads((ROOT/'tensors.json').read_text());results=json.loads((ROOT/'results.json').read_text())
    models={m:source_tensor(m)for m in [0,1]};counts=0
    for row in results['models']:
        rid=row['id'];R=data[rid];M=zest(models[row['m']])if row['zested']else models[row['m']]
        p=row['basis_map_source_to_model']
        require(sha(R)==row['tensor_sha256'],'input binding '+rid)
        require(M==row['model_tensor'],'stored model binding '+rid)
        require(p[0]==0 and sorted(p)==list(range(12)),'based bijection '+rid)
        require(all(R[i][j][k]==M[p[i]][p[j]][p[k]]for i,j,k in itertools.product(range(12),repeat=3)),'all tensor coefficients '+rid)
        counts+=1
    require(counts==4,'four accepted model IDs')
    conditional=json.loads((ROOT/'conditional_twists.json').read_text());degree=[0]*8+[1]*4
    for row in conditional:
        R=models[row['m']];p=row['involutive_ring_automorphism'];q=row['basis_map_source_to_model'];N=data[row['id']]
        require(all(p[p[i]]==i for i in range(12)),'conditional involution')
        require(all(R[i][j][k]==R[p[i]][p[j]][p[k]]for i,j,k in itertools.product(range(12),repeat=3)),'conditional ring automorphism')
        T=[[[R[i][p[j]if degree[i]else j][k]for k in range(12)]for j in range(12)]for i in range(12)]
        require(all(N[i][j][k]==T[q[i]][q[j]][q[k]]for i,j,k in itertools.product(range(12),repeat=3)),'conditional ring identity')
        require(row['status']=='conditional_only_not_a_model','scope of unsupported lifts')
    out=dict(status='PASS',accepted_unitary_models=counts,accepted_exclusions=0,full_tensor_coefficients_checked=1728*counts,conditional_only_ring_twists=len(conditional),optimized_python=not __debug__,elapsed_seconds=time.monotonic()-start)
    (ROOT/('verification_optimized.json'if not __debug__ else'verification.json')).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
