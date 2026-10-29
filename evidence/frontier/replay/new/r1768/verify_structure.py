"""Short exact checks supporting REPORT.md; no categorification decision."""
from pathlib import Path
import hashlib
import itertools
import json
import runpy

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1] / "prior"
source = BASE / "data/current_remaining_cases.py"
N = runpy.run_path(str(source))["TENSORS"]["R8_3_1768"]

def require(c, msg):
    if not c:
        raise RuntimeError(msg)

def mul(a, b):
    return (a[0]*b[0]+37*a[1]*b[1], a[0]*b[1]+a[1]*b[0])

ds = [(1,0),(1,0),(5,1),(6,1),(7,1),(7,1),(6,1),(5,1)]
for i,j in itertools.product(range(8), repeat=2):
    require(mul(ds[i],ds[j]) == tuple(sum(N[i][j][k]*ds[k][h] for k in range(8)) for h in range(2)), "dimension character")
D = tuple(sum(mul(d,d)[h] for d in ds) for h in range(2))
require(D == (444,72), "global dimension")
require(all(N[i][i][0] == 1 for i in range(8)), "all objects selfdual")
require(all(N[1][N[1][i].index(1)][i] == 1 for i in range(8)), "pointed involution")

subrings=[]
for mask in range(1 << 7):
    s={0}|{i+1 for i in range(7) if (mask>>i)&1}
    if all(not N[i][j][k] or k in s for i in s for j in s for k in range(8)):
        subrings.append(sorted(s))
require(subrings == [[0],[0,1],list(range(8))], "fusion subrings")

perms=[]
for bits in itertools.product((0,1),repeat=3):
    p=list(range(8))
    for bit,(i,j) in zip(bits,[(2,7),(3,6),(4,5)]):
        if bit: p[i],p[j]=p[j],p[i]
    if all(N[i][j][k] == N[p[i]][p[j]][p[k]] for i,j,k in itertools.product(range(8),repeat=3)):
        perms.append(p)
require(perms == [list(range(8))], "trivial based automorphisms")

# Source adjoint subring is full: X_2^2 contains every noninvertible,
# and X_2 X_7 contains g.
require(all(N[2][2][j]>0 for j in range(2,8)) and N[2][7][1]>0, "full adjoint ring")

# Transparent human-size witnesses distinguish each equal-dimension pair.
require((N[2][2][2],N[7][7][7]) == (1,2), "first pair")
require((N[2][2][3],N[2][2][6]) == (1,2), "second pair")
require((N[4][4][4],N[5][5][5]) == (2,3), "third pair")

receipt={
    "id":"R8_3_1768", "result":"PASS", "classification":"unresolved",
    "new_complete_exclusions":0,"new_models":0,
    "source_file_sha256":hashlib.sha256(source.read_bytes()).hexdigest(),
    "dimensions_in_Qsqrt37":ds,"global_dimension":D,
    "all_based_subrings":subrings,"based_automorphisms":perms,
    "adjoint_subring_full":True,
    "scope":"Finite ring checks only. The new conditional center/Brauer-Picard conclusions use the categorical proofs and previously published complete sector and Morita-pairing theorems in REPORT.md."
}
(HERE/"structure_receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt,indent=2))
