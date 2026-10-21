#!/usr/bin/env python3
"""Read-only independent replay of the even pointed R1795 obstruction.

No optimizer, file writes, or import of the mutable discovery result.
Recomputes the source Gram, phase mask and every explicit column pairing.
"""
from fractions import Fraction as Q
import itertools
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
FOLLOWUP = HERE.parent / "pointed_followup"
sys.path.insert(0, str(FOLLOWUP))
from c2_fibres import PointedCone, setup, st


def need(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    raw = json.loads((FOLLOWUP / "R8_3_1795.json").read_text())
    odd = json.loads((FOLLOWUP / "R1795_pointed_associator_obstruction.json").read_text())
    need(raw["status"] == "all_parities_exact_infeasible" and
         [r["metadata"]["pointed_second_indicator"] for r in raw["parities"]] == [-1,1],
         "Incomplete terminal parity coverage")
    need(raw["parities"][0] == odd["record"] and raw["tensor_sha256"] == odd["tensor_sha256"],
         "Terminal odd branch differs from the independently audited snapshot")
    source, base, _ = setup(1795)
    R = source["tensor"]
    need(source["tensor_sha256"] == raw["tensor_sha256"], "Source mismatch")
    need(st.encode(base.meta) == raw["base_metadata"], "Base metadata mismatch")
    dual = [next(j for j in range(8) if R[i][j][0]) for i in range(8)]
    B = [[sum(R[j][i][a]*R[a][dual[j]][k] for j in range(8) for a in range(8))
          for k in range(8)] for i in range(8)]
    need(B == base.a["B"].tolist(), "Direct induction Gram mismatch")
    need(R[1][1] == [1,0,0,0,0,0,0,0] and B[0][1] == 0 and B[1][1] == 8,
         "Pointed Fourier hypotheses")
    C = PointedCone(base, 1)
    record = next(r for r in raw["parities"] if r["metadata"]["pointed_second_indicator"] == 1)
    need(st.encode(C.meta) == record["metadata"], "Filtered metadata mismatch")
    report = C.meta["Fourier_fibre_filter"]
    accepted = set(report["retained_high_indices"])
    need(report["fibre_mass"] == (270,120) and report["dimension_coordinate_scale"] == 1,
         "Unexpected mass coordinates")
    # Independently generate finite packings by adding successive individual
    # constituents, keeping their Gram degree, until no state can be added.
    candidates = {j:(int(v[0])**2, int(v[0])*int(z[0]), int(v[0])*int(z[1]))
                  for j,(v,z) in enumerate(base.a["high"]) if v[0]}
    alive = set(candidates)
    while True:
        triples = {candidates[j] for j in alive}
        states = {(0,0,0)}
        frontier = set(states)
        while frontier:
            new = {(q+c,x+a,y+b) for q,x,y in frontier for c,a,b in triples
                   if q+c <= 8 and x+a <= 270 and y+b <= 120} - states
            states.update(new)
            frontier = new
        good = {q for q in range(9) if (q,270,120) in states and (8-q,270,120) in states}
        retained = {j for j in alive if any((q-candidates[j][0],270-candidates[j][1],
                    120-candidates[j][2]) in states for q in good)}
        if retained == alive:
            break
        alive = retained
    need(alive == accepted and len(alive) == 1187, "Independent packing domain differs")
    allowed = set(range(base.offset)) | set(range(base.high_end,base.nvars))
    phases = {tuple((Q(t),Q(0)) for t in row) for row in ((1,1,1,1),(-1,1,-1,1))}
    for orbit, members in enumerate(base.orbits):
        for ti, traces in enumerate(base.types):
            if all(not base.a["high"][j][0][0] or
                   (j in accepted and tuple(traces) in phases) for j in members):
                allowed.add(base.offset+orbit*base.nt+ti)
    need(allowed == C.allowed and len(allowed) == 59261, "Independent phase domain differs")
    choices = sorted(list(ep) for ep in st.old.ht.indicator_choices(R) if ep[0] == 1)
    forced = [i for i in range(1,8) if any(R[j][dual[j]][i] % 2 for j in range(8))]
    need(dual == list(range(8)) and forced == [5,6,7], "Self-duality or forced-indicator domain differs")
    direct_choices = sorted([1,*free,1,1,1] for free in itertools.product((-1,1),repeat=3))
    need(choices == direct_choices, "Independent indicator enumeration differs")
    need(len(choices) == 8 and sorted(b["indicators"] for b in record["branches"]) == choices,
         "Eight-branch coverage differs")
    rays = []
    for branch in record["branches"]:
        need(branch["status"] == "exact_infeasible", "Unproved branch")
        cert = branch["certificate"]
        y = [Q(t) for t in cert["y"]]
        need(all(t.denominator == 1 for t in y), "Separator coordinates must be integral")
        y = [int(t) for t in y]
        need(len(y) == C.nrows, "Ray length")
        rhs = sum(t*Q(b) for t,b in zip(y,C.rhs_for(branch["indicators"])))
        need(rhs == Q(cert["bTy"]) and rhs < 0, "Invalid rhs separation")
        need(C.check_farkas(cert["y"],branch["indicators"]) == cert["bTy"],
             "Factorized oracle differs")
        rays.append(y)
    print("Independent packing and eight factorized separators PASS", flush=True)
    minima = [None]*8
    # Explicit sparse columns independently test the factored score oracle.
    for count,index in enumerate(sorted(allowed),1):
        column = C.column(index)
        values = [sum(y[row]*a for row,a in column.items()) for y in rays]
        need(all(t >= 0 for t in values), "Negative explicit column pairing")
        minima = [v if m is None else min(m,v) for m,v in zip(minima,values)]
        if count % 10000 == 0:
            print("Explicit columns", count, flush=True)
    need(record["status"] == "all_indicator_branches_exact_infeasible", "Snapshot status")
    print("PASS R1795 trivial pointed C2 associator excluded; 59261 columns, 8 rays; "
          "combine with independently audited odd branches for complete exclusion", flush=True)


if __name__ == "__main__":
    main()
