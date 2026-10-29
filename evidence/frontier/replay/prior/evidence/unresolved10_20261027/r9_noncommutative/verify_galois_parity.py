"""Exact, bounded replay of GALOIS_PARITY_EXCLUSION.md.

No associator or center enumeration. The all-complex cochain and categorical
arguments are proved in the accompanying document, not inferred from a search.
"""
from itertools import product
from pathlib import Path
import hashlib
import importlib.util
import json
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
INPUT = ROOT / "evidence/unresolved_retry_20261024/proofs/unresolved11_20261024/rank9_noncommutative/new_results_inputs.json"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(",", ":")).encode()).hexdigest()


def main():
    raw = INPUT.read_bytes()
    require(hashlib.sha256(raw).hexdigest() ==
            "89173bf51976f6fa9abd854d2fe0d9ce3c9b2dec7fbc1a6cb157a025fc22761d",
            "Archived input file changed")
    data = json.loads(raw)
    require(digest(data["source_tensor"]) ==
            "8b30652d59e868a120b6c423e46a99ab51f6032af752dc0082a3d80fd9e61323",
            "Original R9_2_1975 tensor binding failed")
    selected = [c for c in data["morita_candidates"] if c["alpha"] == 3 and c["a"] == 2]
    require(len(selected) == 1, "Rotation branch is not unique in archive")
    N = selected[0]["N"]
    require(digest(N) ==
            "c2cce7d6536e2fc1b52bac8184c90c5a98a2435bd3b27981c4d8266fa6cf975f",
            "Rotation tensor binding failed")

    spec = importlib.util.spec_from_file_location("duality", HERE / "verify_duality_obstruction.py")
    d = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(d)
    even = [g for g in d.G if g[2] == 0]
    for sign in (0, 1):
        require(all(d.w(a, b, c, sign) == 0 for a, b, c in product(even, repeat=3)),
                "Pointed even V4 is not strict")
        for q in (d.R0, d.mul(d.R0, d.Z0)):
            cq = lambda a, b: d.obstruction(q, a, b, sign=sign)
            require(d.comm(cq, d.P, d.E) == 0, "Rotation P,E commutator failed")
            require(d.comm(cq, d.S, d.E) == 0, "Rotation S,E commutator failed")
    require(d.comm(d.beta, d.P, d.Z) == 2, "Diagonal P,Z anticommutator failed")

    def unique_product(i, j):
        row = N[i][j]
        require(sum(row) == 1 and max(row) == 1, "Expected a simple product")
        return row.index(1)

    # Bind the abstract D8 coordinates and four Q-labels to the archived tensor.
    bind = {d.ONE: 0}
    todo = [d.ONE]
    while todo:
        g = todo.pop()
        for abstract, actual in ((d.P0, 2), (d.S0, 4)):
            ag = d.mul(g, abstract)
            found = unique_product(bind[g], actual)
            if ag in bind:
                require(bind[ag] == found, "D8 coordinate assignment inconsistent")
            else:
                bind[ag] = found
                todo.append(ag)
    require(set(bind.values()) == set(range(8)), "D8 invertibles not exhausted")
    for g, h in product(d.G, repeat=2):
        require(unique_product(bind[g], bind[h]) == bind[d.mul(g, h)],
                "D8 multiplication mismatch")
    quotient = lambda g: (g[0] ^ g[1], g[2])
    add = lambda a, b: (a[0] ^ b[0], a[1] ^ b[1])
    large = {}
    for g in d.G:
        q = quotient(g)
        found = unique_product(bind[g], 8)
        if q in large:
            require(large[q] == found, "Central stabilizer mismatch")
        else:
            large[q] = found
    require(set(large.values()) == set(range(8, 12)), "Four large objects not exhausted")
    alpha = quotient(d.R0)
    for g in d.G:
        for q, X in large.items():
            target = large[add(q, quotient(g))]
            require(unique_product(bind[g], X) == target and
                    unique_product(X, bind[g]) == target, "Quotient actions differ")
    for p, q in product(large, repeat=2):
        target_coset = add(add(p, q), alpha)
        expected = [0] * 12
        for g in d.G:
            expected[bind[g]] = int(quotient(g) == target_coset)
        for X in large.values():
            expected[X] = 2
        require(N[large[p]][large[q]] == expected, "Uniform large product mismatch")

    dual = []
    for i in range(12):
        candidates = [j for j in range(12) if N[i][j][0] == 1]
        require(len(candidates) == 1, "Dual object is not unique")
        dual.append(candidates[0])
    require(dual[8] == 11, "Archived rotation duality changed")
    for q, X in large.items():
        require(dual[X] == large[add(q, alpha)], "Rotation duality formula mismatch")

    mats = [sp.Matrix(Ni) for Ni in N]
    I = sp.eye(12)
    require(mats[0] == I, "Unit matrix mismatch")
    C = sum((mats[i] * mats[dual[i]] for i in range(12)), sp.zeros(12))
    V = mats[0] + sum((mats[i] for i in range(8, 12)), sp.zeros(12))
    t = sp.Symbol("t")
    expected_charpoly = (t-16)**6 * (t-8)**4 * (t*t-288*t+2304)
    require(sp.Poly(C.charpoly(t).as_expr() - expected_charpoly, t).is_zero,
            "Regular Casimir polynomial mismatch (degree factor retained)")
    P = (-C**3 + 304*C**2 - 6848*C + 36352*I) / 512
    require(P == V, "Full Galois-unit matrix identity failed")
    require(list(P.row(0)) == [1] + [0]*7 + [1]*4,
            "Galois-unit restriction does not contain each X once")
    require(all(V*A == A*V for A in mats), "Forced restriction is not central")

    poly = (-t**3 + 304*t*t - 6848*t + 36352)/sp.Integer(512)
    require(poly.subs(t, 8) == 1 and poly.subs(t, 16) == 1,
            "Rational Casimir blocks are not fixed")
    require(sp.rem(poly - t*t/sp.Integer(2304), t*t-288*t+2304, t) == 0,
            "Quadratic block does not have the Galois ratio")
    dimension = 4 + 3*sp.sqrt(2)
    global_dim = 8 + 4*dimension**2
    require(sp.simplify(global_dim/(144-96*sp.sqrt(2)) - (1+4*dimension)) == 0,
            "Galois-unit dimension mismatch")

    receipt = {
        "status": "PASS",
        "ring": "R9_2_1975",
        "research_conclusion": "excluded over C by the proved obstruction and archived scope gates",
        "input_file_sha256": hashlib.sha256(raw).hexdigest(),
        "source_tensor_sha256": digest(data["source_tensor"]),
        "rotation_tensor_sha256": digest(N),
        "abstract_D8_to_tensor": {str(k): v for k, v in sorted(bind.items())},
        "Q_to_large_tensor": {str(k): v for k, v in sorted(large.items())},
        "rotation_P_E_commutator": 1,
        "diagonal_P_Z_commutator": -1,
        "strict_even_V4_triples_per_TY_sign": 64,
        "regular_Casimir_characteristic_polynomial": str(sp.factor(expected_charpoly)),
        "CRT_polynomial": str(poly),
        "forced_Galois_unit_restriction": [int(x) for x in P.row(0)],
        "full_matrix_identity_checked": True,
        "caution": "This replay verifies exact finite inputs. The all-C* cochain cancellation, relative-center parity, Galois theorem and prior general-scope gates are mathematical proofs in the linked reports."
    }
    (HERE / "galois_parity_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
