"""Generic ring-data certificate for the module-functor sign criterion.

Categorical input: a hypothetical fusion categorification. The proof is in
SOURCE_LOCAL_CLIFFORD.md. No TY parameter, guessed half-braiding, numerical
optimizer, or selected F-symbol solution enters this check.
"""
from pathlib import Path
from collections import deque
import hashlib
import json

HERE = Path(__file__).resolve().parent
INPUTS = HERE.parents[1] / "unresolved11_20261024/inputs"


def sign_criterion(R, subcategory):
    n = len(R)
    D = set(subcategory)
    if 0 not in D:
        raise ValueError("Subcategory must contain the unit")
    dual = []
    for i in range(n):
        choices = [j for j in range(n) if R[i][j][0] == 1]
        if len(choices) != 1:
            raise ValueError("Duality is not uniquely determined")
        dual.append(choices[0])
    if any(dual[i] not in D for i in D):
        raise ValueError("Subcategory not closed under duality")
    if any(R[i][j][k] for i in D for j in D for k in range(n) if k not in D):
        raise ValueError("Subcategory not closed under products")
    components = []
    unseen = set(range(n))
    while unseen:
        start = min(unseen)
        todo = deque([start]); M = {start}; unseen.remove(start)
        while todo:
            x = todo.popleft()
            for a in D:
                for y in range(n):
                    if R[a][x][y] and y not in M:
                        M.add(y); unseen.remove(y); todo.append(y)
        components.append(M)
    result = []
    for M in components:
        for x in sorted(M):
            internal_end = {a: R[a][x][x] for a in D if R[a][x][x]}
            if len(internal_end) != 2 or internal_end.get(0) != 1:
                continue
            h = next(a for a in internal_end if a)
            if internal_end[h] != 1:
                continue
            unit = [int(k == 0) for k in range(n)]
            if R[h][h] != unit:
                continue
            ex = [int(k == x) for k in range(n)]
            if R[h][x] != ex or R[x][h] != ex:
                continue
            perm = {}
            for y in M:
                support = [k for k in range(n) if R[y][h][k]]
                if len(support) != 1 or R[y][h][support[0]] != 1 or support[0] not in M:
                    raise ValueError("Right tensoring fails to preserve the left module")
                perm[y] = support[0]
            moved = [y for y in M if perm[y] != y]
            if not moved:
                continue
            cubic = R[x][x][dual[x]]
            if cubic % 2:
                raise ValueError("The categorical criterion would exclude this ring by odd cubic multiplicity")
            result.append({"object": x, "stabilizer": h,
                           "internal_end": internal_end, "left_module_component": sorted(M),
                           "right_permutation": perm, "moved_objects": sorted(moved),
                           "dual": dual[x], "cubic_dimension": cubic,
                           "forced_stabilizer_commutator": -1})
    return result


def main():
    subcategories = {
        137: [0,1,2,7,8], 1607: [0,3,4,5,6],
        1975: [0,5,6,7,8], 1976: [0,5,6,7,8],
    }
    out = {"classification_change": False, "sources": {}}
    for number, D in subcategories.items():
        rid = f"R9_2_{number}"
        profile = json.loads((INPUTS / f"{rid}.json").read_text())
        R = profile["fusion_tensor"]
        result = sign_criterion(R, D)
        expected = 0 if number == 1975 else 4
        if len(result) != expected:
            raise ValueError(f"Unexpected number of applicable objects: {rid}")
        if any(item["cubic_dimension"] != 2 for item in result):
            raise ValueError("Unexpected cubic dimension")
        out["sources"][rid] = {
            "tensor_sha256": hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest(),
            "subcategory": D, "forced_objects": result,
            "status": "four individual Clifford constraints" if result else
                      "not applicable: left/right stabilizers differ",
        }
    (HERE / "source_local_receipt.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"checked":True,"forced_objects":12,"classification_change":False}))


if __name__ == "__main__":
    main()
