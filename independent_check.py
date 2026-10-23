"""Independent exact checks for bounded mixed-integer necessary systems.

Only Python's standard library is used. Numerical solver status is never
accepted as proof. Continuous variables retain real, rather than integer,
domains. None at a bound means a genuinely unbounded side.
"""
from fractions import Fraction
import hashlib
import json
import math


class InvalidCertificate(ValueError):
    pass


def need(condition, message):
    if not condition:
        raise InvalidCertificate(message)


def rational(value):
    need(type(value) in (int, str), "Rational entries must be integers or strings, never floats")
    return Fraction(value)


def model_digest(model):
    return hashlib.sha256(json.dumps(model, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def sparse(row, size):
    if isinstance(row, dict):
        items = row.items()
    elif isinstance(row, list):
        if all(isinstance(item, (list, tuple)) and len(item) == 2 for item in row):
            items = row
        else:
            need(len(row) == size, "Dense vector has wrong size")
            items = enumerate(row)
    else:
        raise InvalidCertificate("Invalid sparse vector")
    result = {}
    for index, coefficient in items:
        index = int(index)
        need(0 <= index < size, "Vector index outside model")
        value = rational(coefficient)
        result[index] = result.get(index, Fraction(0)) + value
    return {index: value for index, value in result.items() if value}


def unpack(model):
    n = model["n"]
    need(type(n) is int and n >= 0, "Invalid variable count")
    rows = [sparse(row, n) for row in model["rows"]]
    rhs = [rational(value) for value in model["rhs"]]
    need(len(rows) == len(rhs), "Equation count mismatch")
    lo = [None if value is None else rational(value) for value in model["lo"]]
    up = [None if value is None else rational(value) for value in model["up"]]
    integer = model["integrality"]
    need(len(lo) == len(up) == len(integer) == n, "Variable domain count mismatch")
    need(all(type(value) is int and value in (0, 1) for value in integer), "Only continuous/integer domain flags 0/1 are supported")
    return n, rows, rhs, lo, up, integer


def covector_data(rows, rhs, n, covector):
    y = sparse(covector, len(rows))
    product = [Fraction(0)] * n
    value = Fraction(0)
    for i, coefficient in y.items():
        value += coefficient * rhs[i]
        for j, entry in rows[i].items():
            product[j] += coefficient * entry
    return product, value


def box_extreme(coefficients, lo, up, maximum):
    total = Fraction(0)
    for j, coefficient in enumerate(coefficients):
        if not coefficient:
            continue
        choose_upper = (coefficient > 0) == maximum
        bound = up[j] if choose_upper else lo[j]
        need(bound is not None, "Requested exact box extreme is unbounded")
        total += coefficient * bound
    return total


def contradictory_box(lo, up):
    return any(a is not None and b is not None and a > b for a, b in zip(lo, up))


def apply_cuts(data, cuts, lo, up):
    n, rows, rhs, _, _, integer = data
    for cut in cuts:
        j, sign = cut["variable"], cut["sign"]
        need(type(j) is int and 0 <= j < n and integer[j] == 1, "Integer rounding cut on noninteger variable")
        need(type(sign) is int and sign in (-1, 1), "Invalid cut sign")
        product, value = covector_data(rows, rhs, n, cut["covector"])
        residual = [-entry for entry in product]
        residual[j] += sign
        lower = value + box_extreme(residual, lo, up, maximum=False)
        rounded = math.ceil(lower)
        if "lower_bound" in cut:
            need(rational(cut["lower_bound"]) == rounded, "Claimed integer bound differs from exact bound")
        if sign == 1:
            lo[j] = max(lo[j], Fraction(rounded)) if lo[j] is not None else Fraction(rounded)
        else:
            bound = Fraction(-rounded)
            up[j] = min(up[j], bound) if up[j] is not None else bound
        if contradictory_box(lo, up):
            return True
    return False


def verify_separator(data, separator, lo, up):
    n, rows, rhs, _, _, _ = data
    product, value = covector_data(rows, rhs, n, separator["covector"])
    gap = value - box_extreme(product, lo, up, maximum=True)
    need(gap > 0, "Separating gap is not strictly positive")
    if "gap" in separator:
        need(rational(separator["gap"]) == gap, "Claimed separating gap differs")
    return gap


def verify_proof(model, proof):
    """Check a cut/separator proof or an exhaustive finite integer split tree.

    Every split is x_j <= k versus x_j >= k+1, for an INTEGER variable.
    Each node may carry valid integer cuts before its separator or split.
    """
    need(proof.get("model_sha256") == model_digest(model), "Proof is bound to a different exact model")
    data = unpack(model)
    statistics = {"nodes": 0, "cuts": 0, "separators": 0, "box_contradictions": 0}
    pending = [(proof["root"], list(data[3]), list(data[4]))]
    while pending:
        node, lo, up = pending.pop()
        statistics["nodes"] += 1
        cuts = node.get("cuts", [])
        statistics["cuts"] += len(cuts)
        contradiction = contradictory_box(lo, up) or apply_cuts(data, cuts, lo, up)
        if contradiction:
            statistics["box_contradictions"] += 1
            continue
        if "separator" in node:
            verify_separator(data, node["separator"], lo, up)
            statistics["separators"] += 1
            continue
        need("split" in node, "Unclosed proof leaf")
        split = node["split"]
        j, threshold = split["variable"], split["floor"]
        need(type(j) is int and 0 <= j < data[0] and data[5][j] == 1, "Branching on noninteger variable")
        need(type(threshold) is int, "Integer split threshold required")
        left_lo, left_up = list(lo), list(up)
        right_lo, right_up = list(lo), list(up)
        left_up[j] = min(left_up[j], Fraction(threshold)) if left_up[j] is not None else Fraction(threshold)
        right_lo[j] = max(right_lo[j], Fraction(threshold + 1)) if right_lo[j] is not None else Fraction(threshold + 1)
        need("left" in split and "right" in split, "Incomplete integer branch coverage")
        pending.append((split["left"], left_lo, left_up))
        pending.append((split["right"], right_lo, right_up))
    return {"status": "EXACT_MODEL_INFEASIBILITY_VERIFIED", **statistics}


def verify_witness(model, values):
    data = unpack(model)
    n, rows, rhs, lo, up, integer = data
    need(len(values) == n, "Witness length mismatch")
    x = list(map(rational, values))
    for j, value in enumerate(x):
        need(lo[j] is None or value >= lo[j], "Witness violates lower bound")
        need(up[j] is None or value <= up[j], "Witness violates upper bound")
        need(not integer[j] or value.denominator == 1, "Witness violates integer domain")
    for row, target in zip(rows, rhs):
        need(sum((a*x[j] for j, a in row.items()), Fraction(0)) == target, "Witness violates exact equation")
    return {"status": "EXACT_NECESSARY_SYSTEM_WITNESS_VERIFIED"}


def self_test():
    model = {"n": 2, "rows": [{"0": 1, "1": 1}], "rhs": [3], "lo": [0, 0], "up": [1, 1], "integrality": [1, 0]}
    proof = {"model_sha256": model_digest(model), "root": {"separator": {"covector": [1], "gap": 1}}}
    verify_proof(model, proof)
    model2 = {"n": 1, "rows": [{"0": 1}], "rhs": ["1/2"], "lo": [0], "up": [1], "integrality": [1]}
    cuts = [{"variable": 0, "sign": 1, "covector": [1], "lower_bound": 1},
            {"variable": 0, "sign": -1, "covector": [-1], "lower_bound": 0}]
    verify_proof(model2, {"model_sha256": model_digest(model2), "root": {"cuts": cuts}})
    continuous = {**model2, "integrality": [0]}
    try:
        verify_proof(continuous, {"model_sha256": model_digest(continuous), "root": {"cuts": cuts}})
    except InvalidCertificate:
        pass
    else:
        raise AssertionError("Continuous rounding was accepted")
    feasible = {**model, "rhs": [1]}
    verify_witness(feasible, [1, 0])
    unbounded = {"n": 2, "rows": [{"0": 1, "1": -1}], "rhs": [1], "lo": [0, 0], "up": [0, None], "integrality": [0, 0]}
    verify_proof(unbounded, {"model_sha256": model_digest(unbounded), "root": {"separator": {"covector": [1]}}})
    return {"status": "PASS", "scope": "exact separators, integer rounding, mixed domains, rational witnesses and infinite-bound support"}


if __name__ == "__main__":
    print(json.dumps(self_test(), sort_keys=True))
