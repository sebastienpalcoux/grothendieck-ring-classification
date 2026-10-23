"""Mixed-integer discovery with independently replayable rational certificates.

Only exact arithmetic establishes a result. HiGHS/SciPy proposes points,
bounds and separating covectors; every accepted step is rechecked here.
A certified infeasible necessary model is not automatically a categorical
exclusion: its mathematical domain and coverage remain separate obligations.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import time
from fractions import Fraction as F

SCHEMA = "rank8-exact-mip-v1"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def q(value):
    if isinstance(value, F):
        return value
    if isinstance(value, bool) or isinstance(value, float):
        raise ValueError("Exact model coefficients must be integers or rational strings, never floats.")
    if isinstance(value, int):
        return F(value)
    if isinstance(value, str):
        return F(value)
    # numpy integer scalars have an exact __index__, unlike numpy floats.
    if hasattr(value, "__index__"):
        return F(value.__index__())
    raise ValueError("Unsupported exact coefficient: " + repr(value))


def s(value):
    value = F(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def ceiling(value):
    value = F(value)
    return -((-value.numerator) // value.denominator)


def floor(value):
    value = F(value)
    return value.numerator // value.denominator


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n")
    os.replace(temporary, path)


def normalize_model(model):
    n = int(model["n"])
    require(n > 0, "Model must have at least one variable.")
    rows = []
    raw_rows = model.get("rows", [])
    rhs = model.get("rhs")
    row_lo, row_up = model.get("row_lo"), model.get("row_up")
    bounded_rows = row_lo is not None or row_up is not None
    if bounded_rows:
        row_lo = row_lo if row_lo is not None else [None] * len(raw_rows)
        row_up = row_up if row_up is not None else [None] * len(raw_rows)
        require(len(row_lo) == len(row_up) == len(raw_rows), "Row-bound lengths differ.")
    else:
        require(rhs is not None and len(rhs) == len(raw_rows), "Missing equality right-hand sides.")
    for i, raw in enumerate(raw_rows):
        require(isinstance(raw, dict), "Each row must be a sparse dictionary.")
        row = {}
        for j, a in raw.items():
            j = int(j)
            require(0 <= j < n, "Column index out of range.")
            a = q(a)
            if a:
                row[j] = row.get(j, F(0)) + a
        row = {j: a for j, a in row.items() if a}
        if bounded_rows:
            lower = None if row_lo[i] is None else q(row_lo[i])
            upper = None if row_up[i] is None else q(row_up[i])
            require(lower is None or upper is None or lower <= upper, "Inconsistent row bounds.")
        else:
            lower = upper = q(rhs[i])
        if lower is not None and upper is not None and lower == upper:
            rows.append({"a": row, "b": lower, "sense": "eq", "source_row": i})
        else:
            if lower is not None:
                rows.append({"a": row, "b": lower, "sense": "ge", "source_row": i})
            if upper is not None:
                rows.append({"a": {j: -a for j, a in row.items()}, "b": -upper,
                             "sense": "ge", "source_row": i})
    lo, up = list(map(q, model["lo"])), list(map(q, model["up"]))
    require(len(lo) == len(up) == n, "Variable-bound lengths differ.")
    integer = [int(v) for v in model.get("integrality", [1] * n)]
    require(len(integer) == n and all(v in (0, 1) for v in integer), "Use integrality 0/1.")
    for j in range(n):
        if integer[j]:
            lo[j], up[j] = F(ceiling(lo[j])), F(floor(up[j]))
    return {"n": n, "rows": rows, "lo": lo, "up": up, "integrality": integer}


def serialized_core(core):
    return {"n": core["n"], "rows": [
        {"a": {str(j): s(a) for j, a in sorted(row["a"].items())},
         "b": s(row["b"]), "sense": row["sense"], "source_row": row["source_row"]}
        for row in core["rows"]], "lo": list(map(s, core["lo"])),
        "up": list(map(s, core["up"])), "integrality": core["integrality"]}


def model_digest(core):
    data = json.dumps(serialized_core(core), sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


def combination(core, multipliers):
    vector, beta = {}, F(0)
    seen = set()
    for index, value in multipliers:
        index, value = int(index), q(value)
        require(0 <= index < len(core["rows"]) and index not in seen, "Bad covector row.")
        seen.add(index)
        row = core["rows"][index]
        require(row["sense"] == "eq" or value >= 0, "Negative multiplier on an inequality.")
        beta += value * row["b"]
        for j, a in row["a"].items():
            vector[j] = vector.get(j, F(0)) + value * a
    return {j: a for j, a in vector.items() if a}, beta


def support(vector, lo, up, maximum=True):
    if maximum:
        return sum((max(a * lo[j], a * up[j]) for j, a in vector.items()), F(0))
    return sum((min(a * lo[j], a * up[j]) for j, a in vector.items()), F(0))


def separator_gap(core, multipliers, lo, up):
    vector, beta = combination(core, multipliers)
    return beta - support(vector, lo, up)


def cut_bound(core, cut, lo, up):
    """Return the exact strongest bound supplied by this cut's covector."""
    j = int(cut["variable"])
    require(0 <= j < core["n"], "Bad cut variable.")
    vector, beta = combination(core, cut["multipliers"])
    if cut["type"] == "row_bound":
        a = vector.pop(j, F(0))
        require(a != 0, "A row bound needs a nonzero target coefficient.")
        bound = (beta - support(vector, lo, up)) / a
        side = "lo" if a > 0 else "up"
        if core["integrality"][j]:
            bound = F(ceiling(bound) if side == "lo" else floor(bound))
    elif cut["type"] == "objective_bound":
        sign = int(cut["sign"])
        require(sign in (-1, 1), "Bad objective sign.")
        residual = {k: -a for k, a in vector.items()}
        residual[j] = residual.get(j, F(0)) + sign
        lower = beta + support(residual, lo, up, maximum=False)
        if core["integrality"][j]:
            lower = F(ceiling(lower))
        bound = lower if sign == 1 else -lower
        side = "lo" if sign == 1 else "up"
    else:
        raise ValueError("Unknown exact cut type.")
    return j, side, bound


def apply_cut(core, cut, lo, up):
    j, side, justified = cut_bound(core, cut, lo, up)
    proposed = q(cut["value"])
    if side == "lo":
        require(proposed <= justified, "Unjustified lower bound.")
        require(proposed > lo[j], "Non-improving recorded lower bound.")
        lo[j] = proposed
    else:
        require(proposed >= justified, "Unjustified upper bound.")
        require(proposed < up[j], "Non-improving recorded upper bound.")
        up[j] = proposed


def empty_box(lo, up):
    return any(a > b for a, b in zip(lo, up))


def verify_witness(model, values):
    core = normalize_model(model)
    require(len(values) == core["n"], "Witness length differs.")
    x = list(map(q, values))
    for j, a in enumerate(x):
        require(core["lo"][j] <= a <= core["up"][j], "Witness outside variable bounds.")
        require(not core["integrality"][j] or a.denominator == 1, "Nonintegral integer variable.")
    for row in core["rows"]:
        value = sum((a * x[j] for j, a in row["a"].items()), F(0))
        require(value == row["b"] if row["sense"] == "eq" else value >= row["b"],
                "Witness violates an exact model row.")
    return True


def verify_certificate(model, certificate):
    """Standalone standard-library replay of a complete bound/tree certificate."""
    if isinstance(certificate, (str, Path)):
        certificate = json.loads(Path(certificate).read_text())
    core = normalize_model(model)
    require(certificate.get("schema") == SCHEMA, "Unknown certificate schema.")
    require(certificate["model_sha256"] == model_digest(core), "Certificate/model mismatch.")
    nodes = certificate["nodes"]
    seen = set()
    def visit(identifier, lo, up):
        identifier = str(identifier)
        require(identifier in nodes and identifier not in seen, "Missing/cyclic/duplicate proof node.")
        seen.add(identifier)
        node = nodes[identifier]
        for cut in node.get("cuts", []):
            require(not empty_box(lo, up), "Cut after an already empty box.")
            apply_cut(core, cut, lo, up)
        if node["status"] == "closed":
            terminal = node["terminal"]
            if terminal["type"] == "empty_box":
                require(empty_box(lo, up), "Box is not empty.")
            elif terminal["type"] == "separator":
                require(not empty_box(lo, up), "Unexpected empty separator box.")
                gap = separator_gap(core, terminal["multipliers"], lo, up)
                require(gap > 0, "Nonpositive exact separation.")
                if "gap" in terminal:
                    require(q(terminal["gap"]) == gap, "Wrong recorded gap.")
            else:
                raise ValueError("Unknown proof leaf.")
        elif node["status"] == "split":
            branch = node["branch"]
            j, k = int(branch["variable"]), int(branch["at"])
            require(0 <= j < core["n"] and core["integrality"][j], "Branch on noninteger variable.")
            require(lo[j] <= k < up[j], "Non-exhaustive or non-progressing branch.")
            lu, rl = up.copy(), lo.copy()
            lu[j], rl[j] = F(k), F(k + 1)
            visit(branch["left"], lo.copy(), lu)
            visit(branch["right"], rl, up.copy())
        else:
            raise ValueError("Unclosed node in a claimed complete proof.")
    visit("0", core["lo"].copy(), core["up"].copy())
    require(len(seen) == len(nodes), "Certificate has unreachable proof nodes.")
    return {"status": "PASS_EXACT_MODEL_INFEASIBILITY", "nodes": len(seen),
            "model_sha256": model_digest(core)}


def standardize_model(model):
    """Deterministically reduce inequalities to bounded continuous slacks.

    The exported equality model is equivalent on the original variables.
    No phase weight, slack or other real auxiliary is declared integral.
    """
    core = normalize_model(model)
    n = core["n"]
    rows = []
    rhs = []
    lo, up = core["lo"].copy(), core["up"].copy()
    integer = core["integrality"].copy()
    slack_for_row = {}
    for i, row in enumerate(core["rows"]):
        a = {str(j): s(v) for j, v in row["a"].items()}
        if row["sense"] == "ge":
            slack = len(lo)
            slack_for_row[i] = slack
            a[str(slack)] = "-1"
            lo.append(F(0))
            up.append(max(F(0), support(row["a"], core["lo"], core["up"]) - row["b"]))
            integer.append(0)
        rows.append(a)
        rhs.append(s(row["b"]))
    equivalent = {
        "n": len(lo), "rows": rows, "rhs": rhs, "lo": list(map(s, lo)), "up": list(map(s, up)),
        "integrality": integer, "case": model.get("case"), "id": model.get("id"),
        "theory_scope": model.get("theory_scope", ""),
        "standardized_from": model_digest(core),
        "standardization": "Integer domain rounding; every >= row a*x>=b becomes a*x-s=b with finite continuous slack."
    }
    return equivalent, slack_for_row


def independent_export(model, core, nodes):
    equivalent, slack_for_row = standardize_model(model)
    def translate(identifier):
        node = nodes[str(identifier)]
        translated = {"cuts": []}
        for cut in node.get("cuts", []):
            j = int(cut["variable"])
            if cut["type"] == "row_bound":
                vector, _ = combination(core, cut["multipliers"])
                coefficient = vector[j]
                sign = 1 if coefficient > 0 else -1
                factor = abs(coefficient)
                covector = {str(i): s(q(value) / factor) for i, value in cut["multipliers"]}
            else:
                sign = int(cut["sign"])
                covector = {str(i): value for i, value in cut["multipliers"]}
            translated["cuts"].append({"variable": j, "sign": sign, "covector": covector})
        if node["status"] == "closed":
            terminal = node["terminal"]
            if terminal["type"] == "separator":
                translated["separator"] = {
                    "covector": {str(i): value for i, value in terminal["multipliers"]}}
            # An empty box is independently recognized after the exact cuts.
        else:
            require(node["status"] == "split", "Unclosed translated branch.")
            branch = node["branch"]
            translated["split"] = {
                "variable": int(branch["variable"]), "floor": int(branch["at"]),
                "left": translate(branch["left"]), "right": translate(branch["right"])}
        return translated
    import independent_check
    proof = {"model_sha256": independent_check.model_digest(equivalent), "root": translate("0"),
             "scope": "Exact infeasibility of the same bounded mixed-integer necessary system."}
    receipt = independent_check.verify_proof(equivalent, proof)
    return equivalent, proof, receipt


def _write_complete_proof(model, core, nodes, output):
    certificate = {"schema": SCHEMA, "model_sha256": model_digest(core), "nodes": nodes}
    primary = verify_certificate(model, certificate)
    equivalent, proof, independent = independent_export(model, core, nodes)
    atomic_json(output / "infeasibility_certificate.json", certificate)
    atomic_json(output / "independent_model.json", equivalent)
    atomic_json(output / "independent_proof.json", proof)
    atomic_json(output / "independent_receipt.json", independent)
    return {"primary": primary, "independent": independent}


def _write_witness(model, core, values, output):
    verify_witness(model, values)
    equality, slack_for_row = standardize_model(model)
    lifted = list(map(q, values))
    for i, row in enumerate(core["rows"]):
        if i in slack_for_row:
            require(slack_for_row[i] == len(lifted), "Slack ordering changed.")
            lifted.append(sum((a * q(values[j]) for j, a in row["a"].items()), F(0)) - row["b"])
    import independent_check
    receipt = independent_check.verify_witness(equality, list(map(s, lifted)))
    atomic_json(output / "witness.json",
                {"model_sha256": model_digest(core), "values": values, "exactly_verified": True})
    atomic_json(output / "independent_model.json", equality)
    atomic_json(output / "independent_witness.json", {"values": list(map(s, lifted)),
                "model_sha256": independent_check.model_digest(equality)})
    atomic_json(output / "independent_receipt.json", receipt)
    return receipt

def _candidate(core, model, point):
    if point is None or len(point) != core["n"]:
        return None
    integer_values = {}
    for j, integral in enumerate(core["integrality"]):
        if integral:
            if not math.isfinite(float(point[j])) or abs(float(point[j]) - round(float(point[j]))) > 1e-5:
                return None
            integer_values[j] = F(round(float(point[j])))
    for denominator in (1000, 1000000, 1000000000, 1000000000000):
        try:
            values = [integer_values[j] if j in integer_values else
                      F(float(point[j])).limit_denominator(denominator) for j in range(core["n"])]
            verify_witness(model, values)
            return list(map(s, values))
        except (ValueError, OverflowError):
            pass
    return None


class NumericModel:
    """One sparse representation reused for discovery solves. No proof trusts it."""
    def __init__(self, core):
        import numpy as np
        import scipy.sparse as sparse
        from scipy.optimize import linprog, milp, Bounds, LinearConstraint
        self.np, self.sparse = np, sparse
        self.linprog, self.milp, self.Bounds, self.LinearConstraint = linprog, milp, Bounds, LinearConstraint
        self.core = core
        self.eq_ids, self.ge_ids = [], []
        self.scales = []
        rr, cc, vv = [], [], []
        b = []
        for i, row in enumerate(core["rows"]):
            scale = max([F(1), abs(row["b"])] + [abs(a) for a in row["a"].values()])
            self.scales.append(scale)
            for j, a in row["a"].items():
                rr.append(i); cc.append(j); vv.append(float(a / scale))
            b.append(float(row["b"] / scale))
            (self.eq_ids if row["sense"] == "eq" else self.ge_ids).append(i)
        self.A = sparse.coo_matrix((vv, (rr, cc)), shape=(len(core["rows"]), core["n"])).tocsr()
        self.b = np.array(b, dtype=float)
        self.Aeq, self.beq = self.A[self.eq_ids], self.b[self.eq_ids]
        self.Age, self.bge = self.A[self.ge_ids], self.b[self.ge_ids]
        self.phase_Aeq = sparse.hstack([
            self.Aeq, sparse.eye(len(self.eq_ids)), -sparse.eye(len(self.eq_ids)),
            sparse.csr_matrix((len(self.eq_ids), len(self.ge_ids)))], format="csr")
        self.phase_Aub = sparse.hstack([
            -self.Age, sparse.csr_matrix((len(self.ge_ids), 2 * len(self.eq_ids))),
            -sparse.eye(len(self.ge_ids))], format="csr")
        self.phase_c = np.r_[np.zeros(core["n"]),
                            np.ones(2 * len(self.eq_ids) + len(self.ge_ids))]
        self.solver_calls = 0

    def bounds(self, lo, up):
        result = [(float(a), float(b)) for a, b in zip(lo, up)]
        require(all(math.isfinite(a) and math.isfinite(b) for a, b in result), "Numeric bound overflow.")
        return result

    def call_lp(self, lo, up, seconds, objective=None, phase=False):
        import warnings
        self.solver_calls += 1
        options = {"time_limit": max(0.01, float(seconds)), "threads": 1, "presolve": True}
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message="Unrecognized options detected")
            if phase:
                result = self.linprog(self.phase_c,
                    A_ub=self.phase_Aub if len(self.ge_ids) else None,
                    b_ub=-self.bge if len(self.ge_ids) else None,
                    A_eq=self.phase_Aeq if len(self.eq_ids) else None,
                    b_eq=self.beq if len(self.eq_ids) else None,
                    bounds=self.bounds(lo, up) + [(0, None)] * (len(self.phase_c) - self.core["n"]),
                    method="highs", options=options)
            else:
                result = self.linprog(objective,
                    A_ub=-self.Age if len(self.ge_ids) else None,
                    b_ub=-self.bge if len(self.ge_ids) else None,
                    A_eq=self.Aeq if len(self.eq_ids) else None,
                    b_eq=self.beq if len(self.eq_ids) else None,
                    bounds=self.bounds(lo, up), method="highs", options=options)
        return result

    def multipliers(self, result, denominator):
        """Undo row scaling; clamp only inequality multipliers to nonnegative."""
        entries = []
        if result.eqlin is not None and result.eqlin.marginals is not None:
            for i, value in zip(self.eq_ids, result.eqlin.marginals):
                if math.isfinite(float(value)):
                    a = F(float(value)).limit_denominator(denominator) / self.scales[i]
                    if a:
                        entries.append([i, s(a)])
        if result.ineqlin is not None and result.ineqlin.marginals is not None:
            for i, value in zip(self.ge_ids, result.ineqlin.marginals):
                if math.isfinite(float(value)):
                    a = F(max(0.0, -float(value))).limit_denominator(denominator) / self.scales[i]
                    if a:
                        entries.append([i, s(a)])
        return entries

    def mip(self, lo, up, seconds, seed):
        import warnings
        lower = self.np.array([float(self.core["rows"][i]["b"] / self.scales[i])
                              for i in range(len(self.core["rows"]))])
        upper = self.np.array([lower[i] if self.core["rows"][i]["sense"] == "eq" else self.np.inf
                              for i in range(len(self.core["rows"]))])
        options = {"time_limit": max(0.01, float(seconds)), "presolve": True,
                   "mip_rel_gap": 0.0, "threads": 1, "random_seed": int(seed)}
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message="Unrecognized options detected")
            return self.milp(self.np.zeros(self.core["n"]),
                integrality=self.np.array(self.core["integrality"]),
                bounds=self.Bounds(self.np.array([float(a) for a in lo]),
                                   self.np.array([float(a) for a in up])),
                constraints=self.LinearConstraint(self.A, lower, upper), options=options)


def _propagate(core, lo, up, node, max_sweeps=5, on_cut=None):
    """Cheap exact row bounds; every stored step carries a one-row certificate."""
    for _ in range(max_sweeps):
        changed = False
        for i, row in enumerate(core["rows"]):
            for sign in ((1, -1) if row["sense"] == "eq" else (1,)):
                a = {j: sign * v for j, v in row["a"].items()}
                beta = sign * row["b"]
                contributions = {j: max(v * lo[j], v * up[j]) for j, v in a.items()}
                upper = sum(contributions.values(), F(0))
                if beta > upper:
                    return {"type": "separator", "multipliers": [[i, str(sign)]],
                            "gap": s(beta - upper)}
                for j, v in a.items():
                    if not core["integrality"][j]:
                        continue
                    bound = (beta - (upper - contributions[j])) / v
                    side = "lo" if v > 0 else "up"
                    if core["integrality"][j]:
                        bound = F(ceiling(bound) if side == "lo" else floor(bound))
                    if (side == "lo" and bound > lo[j]) or (side == "up" and bound < up[j]):
                        cut = {"type": "row_bound", "variable": j, "value": s(bound),
                               "multipliers": [[i, str(sign)]]}
                        apply_cut(core, cut, lo, up)
                        node["cuts"].append(cut)
                        if on_cut is not None:
                            on_cut()
                        changed = True
                        if empty_box(lo, up):
                            return {"type": "empty_box"}
        if not changed:
            break
    return None


def _node_bounds(core, nodes, identifier):
    chain = []
    current = str(identifier)
    while current != "0":
        node = nodes[current]
        parent = str(node["parent"])
        chain.append((parent, node["side"]))
        current = parent
    lo, up = core["lo"].copy(), core["up"].copy()
    for parent_id, side in reversed(chain):
        parent = nodes[parent_id]
        for cut in parent.get("cuts", []):
            apply_cut(core, cut, lo, up)
        branch = parent["branch"]
        j, k = int(branch["variable"]), int(branch["at"])
        if side == "left":
            up[j] = min(up[j], F(k))
        else:
            lo[j] = max(lo[j], F(k + 1))
    for cut in nodes[str(identifier)].get("cuts", []):
        apply_cut(core, cut, lo, up)
    return lo, up


def _safe_json_numeric(result):
    report = {"status": int(result.status), "message": str(result.message)}
    for key in ("fun", "mip_gap", "mip_node_count", "mip_dual_bound"):
        value = getattr(result, key, None)
        if value is not None:
            try:
                value = float(value)
                report[key] = value if math.isfinite(value) else str(value)
            except (TypeError, ValueError):
                pass
    return report


def solve_model(model, seconds, output_dir, resume=True, seed=0):
    """Search for a new exact witness or a fully certified model exclusion.

    A wall-time interruption preserves every completed exact deduction and
    unexplored branch. Numeric solver reports are explicitly non-certifying.
    """
    started = time.monotonic()
    deadline = started + max(0.05, float(seconds))
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    core = normalize_model(model)
    digest = model_digest(core)
    checkpoint = output / "checkpoint.json"
    previous = json.loads(checkpoint.read_text()) if checkpoint.is_file() else None
    if previous is not None and (not resume or previous.get("model_sha256") != digest):
        # A nonlinear completion adapter may add a necessary no-good cut.
        # Preserve, rather than mix, receipts from its previous exact model.
        import shutil
        history = output / "history" / (previous.get("model_sha256", "unknown")[:20] + "-" + str(time.time_ns()))
        history.mkdir(parents=True, exist_ok=False)
        for name in ("checkpoint.json", "input_model.json", "result.json", "witness.json",
                     "infeasibility_certificate.json", "independent_model.json",
                     "independent_proof.json", "independent_witness.json",
                     "independent_receipt.json", "numeric_candidate.json", "engine_error.json", "cut_journal.jsonl"):
            path = output / name
            if path.is_file():
                shutil.move(str(path), str(history / name))
        previous = None
    if resume and previous is not None:
        state = previous
        require(state.get("schema") == SCHEMA and state["model_sha256"] == digest,
                "Checkpoint belongs to a different model.")
    else:
        state = {"schema": SCHEMA, "model_sha256": digest, "root": "0",
                 "nodes": {"0": {"status": "pending", "cuts": []}}, "frontier": ["0"],
                 "next_id": 1, "elapsed_seconds": 0, "numeric_reports": [], "mip_attempted": False}
    atomic_json(output / "input_model.json", model)
    state.setdefault("journal_sequence", 0)
    journal = output / "cut_journal.jsonl"
    if journal.is_file():
        raw = journal.read_bytes()
        consumed = 0
        lines = raw.splitlines(keepends=True)
        for index, line in enumerate(lines):
            try:
                entry = json.loads(line)
            except (ValueError, UnicodeDecodeError):
                require(index == len(lines) - 1 and not line.endswith(b"\n"),
                        "Corrupt complete cut-journal record.")
                with journal.open("r+b") as handle:
                    handle.truncate(consumed)
                break
            consumed += len(line)
            sequence = int(entry["sequence"])
            if sequence <= state["journal_sequence"]:
                continue
            require(entry["model_sha256"] == digest and sequence == state["journal_sequence"] + 1,
                    "Cut-journal sequence/model mismatch.")
            identifier = str(entry["node"])
            require(identifier in state["nodes"] and state["nodes"][identifier]["status"] == "pending",
                    "Cut-journal references an invalid active node.")
            state["nodes"][identifier]["cuts"].append(entry["cut"])
            state["journal_sequence"] = sequence
    nodes = state["nodes"]
    report = {"schema": SCHEMA, "case": model.get("case"), "id": model.get("id"),
              "model_sha256": digest, "theory_scope": model.get("theory_scope", ""),
              "status": "UNKNOWN_TIME_LIMIT", "certifies_categorification": False,
              "certifies_categorical_nonexistence": False}
    def save():
        state["elapsed_seconds"] += max(0, time.monotonic() - save.last)
        save.last = time.monotonic()
        atomic_json(checkpoint, state)
        # State now includes every durable cut; stale journal entries are safe
        # if interruption occurs between snapshot replacement and truncation.
        with journal.open("w"):
            pass
    save.last = started
    def record_cut(identifier):
        state["journal_sequence"] += 1
        entry = {"model_sha256": digest, "sequence": state["journal_sequence"],
                 "node": str(identifier), "cut": nodes[str(identifier)]["cuts"][-1]}
        with journal.open("a") as handle:
            handle.write(json.dumps(entry, separators=(",", ":")) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
    def finish(status, **extra):
        report.update(status=status, **extra)
        report["elapsed_seconds"] = round(time.monotonic() - started, 6)
        report["cumulative_seconds"] = round(state["elapsed_seconds"] + time.monotonic() - save.last, 6)
        report["proof_nodes"] = len(nodes)
        report["pending_nodes"] = len(state["frontier"])
        save()
        atomic_json(output / "result.json", report)
        return report
    if (output / "witness.json").is_file():
        previous = json.loads((output / "witness.json").read_text())
        if previous.get("model_sha256") == digest:
            verify_witness(model, previous["values"])
            return finish("EXACT_NECESSARY_WITNESS", witness="witness.json", values=previous["values"])
    try:
        save()
        # Exact deductions precede heavy imports and all numerical search.
        if len(nodes) == 1 and nodes["0"]["status"] == "pending":
            lo, up = _node_bounds(core, nodes, "0")
            terminal = {"type": "empty_box"} if empty_box(lo, up) else _propagate(core, lo, up, nodes["0"], on_cut=lambda: record_cut("0"))
            if terminal:
                nodes["0"].update(status="closed", terminal=terminal)
                state["frontier"] = []
            save()
        if not state["frontier"]:
            verification = _write_complete_proof(model, core, nodes, output)
            return finish("INFEASIBLE_CERTIFIED", proof="infeasibility_certificate.json", proof_path=str(output / "infeasibility_certificate.json"),
                          independent_model="independent_model.json", independent_proof="independent_proof.json",
                          exact_verification=verification)
        if time.monotonic() >= deadline:
            return finish("UNKNOWN_TIME_LIMIT")
        numeric = NumericModel(core)
        if not state["mip_attempted"] and time.monotonic() < deadline:
            lo, up = _node_bounds(core, nodes, "0")
            mip_budget = min(30.0, max(0.05, (deadline - time.monotonic()) * 0.20))
            state["mip_attempted"] = True
            save()
            result = numeric.mip(lo, up, mip_budget, seed)
            state["numeric_reports"].append({"stage": "initial_mip", **_safe_json_numeric(result)})
            candidate = _candidate(core, model, getattr(result, "x", None))
            if candidate is not None:
                receipt = _write_witness(model, core, candidate, output)
                return finish("EXACT_NECESSARY_WITNESS", witness="witness.json",
                              values=candidate, independent_verification=receipt)
            save()
        processed_this_run = 0
        while state["frontier"] and time.monotonic() < deadline:
            identifier = str(state["frontier"][-1])
            node = nodes[identifier]
            lo, up = _node_bounds(core, nodes, identifier)
            terminal = {"type": "empty_box"} if empty_box(lo, up) else _propagate(core, lo, up, node, on_cut=lambda: record_cut(identifier))
            if terminal:
                node.update(status="closed", terminal=terminal)
                state["frontier"].pop()
                save()
                continue
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            result = numeric.call_lp(lo, up, min(20, remaining), phase=True)
            processed_this_run += 1
            if result.success:
                exact_separator = None
                for denominator in (1000, 1000000, 1000000000, 1000000000000):
                    multipliers = numeric.multipliers(result, denominator)
                    gap = separator_gap(core, multipliers, lo, up)
                    if gap > 0:
                        exact_separator = {"type": "separator", "multipliers": multipliers, "gap": s(gap)}
                        break
                if exact_separator:
                    node.update(status="closed", terminal=exact_separator)
                    state["frontier"].pop()
                    save()
                    continue
                point = result.x[:core["n"]]
                candidate = _candidate(core, model, point)
                if candidate is not None:
                    receipt = _write_witness(model, core, candidate, output)
                    return finish("EXACT_NECESSARY_WITNESS", witness="witness.json",
                                  values=candidate, independent_verification=receipt)
                # Objective probes generate rigorous integer cuts from floating
                # dual proposals. At most 12 per node; all cuts replay exactly.
                fractional = [j for j in range(core["n"]) if core["integrality"][j]
                              and lo[j] < up[j] and abs(float(point[j]) - round(float(point[j]))) > 1e-7]
                fractional.sort(key=lambda j: abs((float(point[j]) % 1) - 0.5))
                probes = fractional[:6]
                improved = False
                for j in probes:
                    for sign in (1, -1):
                        remaining = deadline - time.monotonic()
                        if remaining < 0.05:
                            break
                        objective = numeric.np.zeros(core["n"])
                        objective[j] = sign
                        probe = numeric.call_lp(lo, up, min(5, remaining), objective=objective)
                        if not probe.success:
                            continue
                        for denominator in (1000, 1000000, 1000000000):
                            multipliers = numeric.multipliers(probe, denominator)
                            cut = {"type": "objective_bound", "variable": j, "sign": sign,
                                   "multipliers": multipliers}
                            _, side, bound = cut_bound(core, cut, lo, up)
                            if (side == "lo" and bound > lo[j]) or (side == "up" and bound < up[j]):
                                cut["value"] = s(bound)
                                apply_cut(core, cut, lo, up)
                                node["cuts"].append(cut)
                                record_cut(identifier)
                                improved = True
                                break
                        if empty_box(lo, up):
                            node.update(status="closed", terminal={"type": "empty_box"})
                            state["frontier"].pop()
                            break
                    if node["status"] == "closed":
                        break
                save()
                if node["status"] == "closed" or improved:
                    continue
                available = [j for j in range(core["n"]) if core["integrality"][j] and lo[j] < up[j]]
                if not available:
                    atomic_json(output / "numeric_candidate.json", {"model_sha256": digest,
                        "values": [repr(float(v)) for v in point], "exactly_verified": False})
                    return finish("NUMERICAL_CANDIDATE_REQUIRES_EXACT_RECONSTRUCTION",
                                  numeric_candidate="numeric_candidate.json")
                j = fractional[0] if fractional else min(available, key=lambda k: up[k] - lo[k])
                k = floor(F(float(point[j]))) if j in fractional else floor((lo[j] + up[j]) / 2)
                k = max(ceiling(lo[j]), min(k, floor(up[j]) - 1))
                left, right = str(state["next_id"]), str(state["next_id"] + 1)
                state["next_id"] += 2
                node.update(status="split", branch={"variable": j, "at": k, "left": left, "right": right})
                nodes[left] = {"parent": identifier, "side": "left", "status": "pending", "cuts": []}
                nodes[right] = {"parent": identifier, "side": "right", "status": "pending", "cuts": []}
                state["frontier"].pop()
                state["frontier"].extend([right, left])
                save()
            else:
                state["numeric_reports"].append({"stage": "phase_i", "node": identifier,
                                                **_safe_json_numeric(result)})
                save()
                # A failed numerical LP is not an exclusion. Preserve the node.
                return finish("UNKNOWN_NUMERICAL_SOLVER_STATUS",
                              numeric_status=_safe_json_numeric(result))
        if not state["frontier"]:
            verification = _write_complete_proof(model, core, nodes, output)
            return finish("INFEASIBLE_CERTIFIED", proof="infeasibility_certificate.json", proof_path=str(output / "infeasibility_certificate.json"),
                          independent_model="independent_model.json", independent_proof="independent_proof.json",
                          exact_verification=verification)
        return finish("UNKNOWN_TIME_LIMIT", processed_nodes_this_run=processed_this_run)
    except KeyboardInterrupt:
        return finish("INTERRUPTED_CHECKPOINT_SAVED")
    except Exception as exc:
        atomic_json(output / "engine_error.json", {"type": type(exc).__name__, "message": str(exc)})
        return finish("ERROR_CHECKPOINT_SAVED", error_type=type(exc).__name__, error=str(exc))


def self_test():
    import tempfile
    fixtures = [
        ("integer_point", {"n": 2, "rows": [{"0": 1, "1": 1}], "rhs": [3],
                           "lo": [0, 0], "up": [3, 3], "integrality": [1, 1]}, True),
        ("mixed_rational", {"n": 2, "rows": [{"0": 2, "1": 3}], "rhs": [1],
                            "lo": [0, 0], "up": [1, 1], "integrality": [1, 0]}, True),
        ("lp_infeasible", {"n": 1, "rows": [{"0": 1}], "rhs": [2],
                           "lo": [0], "up": [1], "integrality": [0]}, False),
        ("integer_only", {"n": 1, "rows": [{"0": 2}], "rhs": [1],
                          "lo": [0], "up": [1], "integrality": [1]}, False),
        ("coupled_parity", {"n": 2, "rows": [{"0": 1, "1": 1}, {"0": 1, "1": -1}],
                            "rhs": [1, 0], "lo": [0, 0], "up": [1, 1],
                            "integrality": [1, 1]}, False),
        ("exhaustive_branch_tree", {"n": 2,
                                   "rows": [{"0": 1, "1": 1}, {"0": 1, "1": -1}],
                                   "row_lo": ["1/2", "-1/2"], "row_up": ["3/2", "1/2"],
                                   "lo": [0, 0], "up": [1, 1], "integrality": [1, 1]}, False),
        ("row_inequalities", {"n": 1, "rows": [{"0": 2}], "row_lo": [1], "row_up": [1],
                              "lo": [0], "up": [1], "integrality": [0]}, True),
    ]
    reports = []
    with tempfile.TemporaryDirectory() as directory:
        for name, model, feasible in fixtures:
            model.update(case="SELF_TEST", id=name, theory_scope="Finite exact control problem.")
            result = solve_model(model, 15, Path(directory) / name, resume=False)
            if feasible:
                require(result["status"] == "EXACT_NECESSARY_WITNESS",
                        "Feasible control failed: " + name + " " + json.dumps(result))
                witness = json.loads((Path(directory) / name / "witness.json").read_text())
                verify_witness(model, witness["values"])
            else:
                require(result["status"] == "INFEASIBLE_CERTIFIED",
                        "Infeasible control failed: " + name + " " + json.dumps(result))
                verify_certificate(model, Path(directory) / name / "infeasibility_certificate.json")
            reports.append({"fixture": name, "status": result["status"]})
    try:
        normalize_model({"n": 1, "rows": [], "rhs": [], "lo": [0], "up": [None]})
    except (TypeError, ValueError):
        pass
    else:
        raise ValueError("Unbounded variable was accepted.")
    return {"status": "PASS", "fixtures": reports, "unbounded_input_rejected": True,
            "proof_verifier_uses_assertions": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path, nargs="?")
    parser.add_argument("--seconds", type=float, default=3600)
    parser.add_argument("--output-dir", type=Path, default=Path("output"))
    parser.add_argument("--fresh", action="store_true")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--verify", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        print(json.dumps(self_test(), indent=2))
        return
    require(args.model is not None, "Supply a model or --self-test.")
    model = json.loads(args.model.read_text())
    result = verify_certificate(model, args.verify) if args.verify else solve_model(
        model, args.seconds, args.output_dir, resume=not args.fresh, seed=args.seed)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
