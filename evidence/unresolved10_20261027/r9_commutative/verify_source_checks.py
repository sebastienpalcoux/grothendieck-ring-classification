"""Short exact checks for the three commutative unresolved rank-nine rings.

No optimization, numerical associator search, or categorification claim.
"""
import hashlib
import json
import runpy
from pathlib import Path

import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TENSORS = runpy.run_path(str(ROOT / "data/current_remaining_cases.py"))["TENSORS"]
d = 4 + 3*s.sqrt(2)
D = 16 + 32*d
result = {}
for rid, y in [("R9_2_137", 8), ("R9_2_1607", 3), ("R9_2_1976", 5)]:
    n = TENSORS[rid]
    dual = [next(j for j in range(9) if n[i][j][0]) for i in range(9)]
    inv = [i for i in range(9) if sum(n[i][dual[i]]) == 1]
    large = [i for i in range(9) if i not in inv + [y]]
    dims = [s.Integer(1) if i in inv else s.Integer(2) if i == y else d
            for i in range(9)]
    for i in range(9):
        for j in range(9):
            if s.expand(dims[i]*dims[j] - sum(n[i][j][k]*dims[k] for k in range(9))) != 0:
                raise ValueError("Dimension character identity failed")
    if s.expand(sum(x*x for x in dims)-D) != 0:
        raise ValueError("Global dimension identity failed")
    result[rid] = {
        "sha256": hashlib.sha256(json.dumps(n, separators=(",", ":")).encode()).hexdigest(),
        "duals": dual, "invertibles": inv, "Y": y, "large": large,
        "self_dual_large": [i for i in large if dual[i] == i],
        "large_cubic_invariant_dimensions": [n[i][i][dual[i]] for i in large],
    }
result["common"] = {
    "d": "4+3sqrt(2)", "D": "144+96sqrt(2)",
    "D_over_d_squared": str(s.simplify((D/d)**2)),
    "pure_large_B_from_formal_codegree": [b for b in range(1, 35) if 1152 % (b*b) == 0],
    "B_in_galois_triple": [b for b in range(1, 35) if 1152 % (b*b) == 0 and 3*b*b < 1152],
}
expected = json.loads((HERE / "source_checks.json").read_text())
if result != expected:
    raise ValueError("Source receipt mismatch")
print("PASS: source dimensions, duality, cubic multiplicities and pure-large divisibility")
