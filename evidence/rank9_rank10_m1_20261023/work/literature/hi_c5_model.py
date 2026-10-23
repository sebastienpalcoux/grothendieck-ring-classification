"""Exact matching with known Haagerup–Izumi(C5) category."""
from pathlib import Path
import sys,json,itertools
P=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(P/'work/models'))
from match_models import based_iso
n=5;T=[[[0]*(2*n) for _ in range(2*n)] for _ in range(2*n)]
for i,j in itertools.product(range(n),repeat=2):
 T[i][j][(i+j)%n]=1
 T[i][n+j][n+(i+j)%n]=1
 T[n+i][j][n+(i-j)%n]=1
 T[n+i][n+j][(i-j)%n]=1
 for k in range(n):T[n+i][n+j][n+k]=1
D=json.load(open(P/'work/input_audit/tensors.json'));rid='R10_1_132';bm=based_iso(D[rid],T);assert bm is not None
assert all(D[rid][i][j][k]==T[bm[i]][bm[j]][bm[k]] for i,j,k in itertools.product(range(10),repeat=3))
c={'id':rid,'model':'Haagerup–Izumi(C5), positive unitary category','constructor':'haagerup_izumi_cyclic','parameters':{'group_order':5},'model_basis':[f'alpha_{i}' for i in range(5)]+[f'alpha_{i}rho' for i in range(5)],'basis_map_source_to_model':bm,'model_tensor':T,'references':['Izumi, The structure of sectors associated with Longo–Rehren inclusions II: Examples, Rev Math Phys13(2001)603–674, Example7.2','Gannon–Schopieray–Yadav, arXiv:2609.25185v1, §1.7 and §7.1, formula(2.1)']}
(P/'work/literature/hi_c5_certificate.json').write_text(json.dumps(c,indent=2)+'\n')
print(rid,bm)
