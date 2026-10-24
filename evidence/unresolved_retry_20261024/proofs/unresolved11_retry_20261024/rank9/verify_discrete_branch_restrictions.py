"""Replay discrete third-indicator branch exclusions and ring relabellings.

This proves a restriction within the reconstructed necessary center systems,
not noncategorifiability of either source ring.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import permutations, product
import gzip
import json

HERE = Path(__file__).resolve().parent
INPUTS = HERE.parents[1] / "unresolved11_20261024/inputs"
results = []
for rid, tau, Y in [("R9_2_137",1,8),("R9_2_1976",-1,5)]:
    name = f"{rid}_tau{tau}_h4_discrete_clifford"
    report = json.loads((HERE/f"{name}.json").read_text())
    system = json.loads(gzip.decompress((HERE/f"{name}_system.json.gz").read_bytes()))
    A, b = system["A"], system["b"]
    expected_shape = (248,22231) if rid == "R9_2_137" else (188,21697)
    if (report["source"],report["tau"],report["height"]) != (rid,tau,4):
        raise ValueError("Wrong source/sign/height report")
    if not A or not A[0] or len(A) != len(b) or any(len(row) != len(A[0]) for row in A):
        raise ValueError("Empty, truncated, or nonrectangular system")
    if (len(A),len(A[0])) != expected_shape:
        raise ValueError("Incorrect expected system size")
    if any(type(x) is not int for row in A for x in row) or any(type(x) is not int for x in b):
        raise ValueError("The portable system must be integral")
    assignments = [tuple(rec["projected_indicators"]) for rec in report["branch_records"]]
    if len(assignments) != 16 or set(assignments) != set(product(("-1","1/2"),repeat=4)):
        raise ValueError("The report does not cover all sixteen discrete assignments")
    feasible = next(rec for rec in report["branch_records"] if "exact_witness" in rec)
    denoms = [Q(bb)/(96*Q(v)) for bb,v in zip(b[-4:],feasible["projected_indicators"])]
    if any(x.denominator != 1 or x <= 0 for x in denoms):
        raise ValueError("Invalid source row scale")
    excluded = {}
    for rec in report["branch_records"]:
        if "exact_ray" not in rec:
            continue
        choices = tuple(rec["projected_indicators"])
        rhs = b[:-4]+[int(96*Q(v)*den) for v,den in zip(choices,denoms)]
        ray = rec["exact_ray"]
        if len(ray) != len(A) or any(type(y) is not int for y in ray):
            raise ValueError("Ray has wrong length")
        bTy = sum(y*z for y,z in zip(rhs,ray))
        if bTy >= 0:
            raise ValueError("No strict separating inequality")
        supported_rows = [(row,y) for row,y in zip(A,ray) if y]
        minimum = min(sum(row[j]*y for row,y in supported_rows) for j in range(len(A[0])))
        if minimum < 0:
            raise ValueError("Invalid dual nonnegativity")
        excluded[choices] = {"bTy":bTy,"minimum_ATy":minimum}
    R = json.loads((INPUTS/f"{rid}.json").read_text())["fusion_tensor"]
    n = len(R)
    G = [i for i in range(n) if sum(sum(R[i][j]) for j in range(n)) == n]
    X = [i for i in range(n) if i not in G and i != Y]
    automorphisms = []
    for pg in permutations(G[1:]):
        for px in permutations(X):
            perm = list(range(n))
            for i,j in zip(G[1:],pg): perm[i] = j
            for i,j in zip(X,px): perm[i] = j
            if all(R[i][j][k] == R[perm[i]][perm[j]][perm[k]]
                   for i,j,k in product(range(n),repeat=3)):
                automorphisms.append(perm)
    transports = []
    survivors = []
    for choices in product(("-1","1/2"),repeat=4):
        if choices in excluded:
            continue
        target = None
        for perm in automorphisms:
            moved = [None]*4
            for i,value in zip(X,choices): moved[X.index(perm[i])] = value
            if tuple(moved) in excluded:
                target = {"source_assignment":choices,"permutation":perm,
                          "excluded_assignment":moved}
                break
        if target:
            transports.append(target)
        else:
            survivors.append(choices)
    if survivors != [("1/2",)*4]:
        raise ValueError("Unexpected surviving projected assignment")
    results.append({"source":rid,"tau":tau,"large_objects":X,
                    "direct_exact_exclusions":[{"assignment":k,**v} for k,v in excluded.items()],
                    "relabelled_exclusions":transports,
                    "based_automorphism_count":len(automorphisms),
                    "surviving_assignment":survivors[0],
                    "classification_change":False})
receipt = {"scope":"Exact necessary-system branch restrictions; requires the source-center builder semantics and the new categorical Clifford theorem.",
           "results":results}
if {(r["source"],r["tau"]) for r in results} != {("R9_2_137",1),("R9_2_1976",-1)}:
    raise ValueError("Missing expected conditional branch restriction")
(HERE/"discrete_branch_restrictions_receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps({"checked":True,"restrictions":[{"source":r["source"],"tau":r["tau"],
                  "direct":len(r["direct_exact_exclusions"]),"transported":len(r["relabelled_exclusions"]),
                  "remaining_assignment":r["surviving_assignment"]} for r in results]}))
