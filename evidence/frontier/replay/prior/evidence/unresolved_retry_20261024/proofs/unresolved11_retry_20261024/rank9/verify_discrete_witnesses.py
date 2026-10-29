"""Portable exact check of saved necessary-system feasibility witnesses.

These are witnesses to a bounded central-induction relaxation. They are not
fusion categories, modular categories, or associator solutions.
"""
from pathlib import Path
from fractions import Fraction
import gzip
import hashlib
import json

HERE = Path(__file__).resolve().parent
EXPECTED = {
    ("R9_2_137",-1,4):(248,21984),
    ("R9_2_137",1,4):(248,22231),
    ("R9_2_1607",-1,4):(214,21887),
    ("R9_2_1976",-1,4):(188,21697),
}
expected_names = {f"{rid}_tau{tau}_h{height}_discrete_clifford_system.json.gz"
                  for rid,tau,height in EXPECTED}
paths = sorted(HERE.glob("*_discrete_clifford_system.json.gz"))
if {path.name for path in paths} != expected_names:
    raise ValueError("Missing or unexpected discrete witness system files")
receipts = []
seen = set()
for path in paths:
    data = json.loads(gzip.decompress(path.read_bytes()))
    A, b = data["A"], data["b"]
    if not A or not A[0] or len(A) != len(b) or any(len(row) != len(A[0]) for row in A):
        raise ValueError("Empty, truncated, or nonrectangular system")
    if any(type(x) is not int for row in A for x in row) or any(type(x) is not int for x in b):
        raise ValueError("The portable system must be integral")
    witness = [(j,Fraction(x)) for j,x in data["witness"]]
    if any(x < 0 for _,x in witness) or len({j for j,_ in witness}) != len(witness):
        raise ValueError(f"Invalid nonnegative witness: {path.name}")
    if any(not 0 <= j < len(A[0]) for j,_ in witness):
        raise ValueError("Witness column out of range")
    if not all(sum(row[j]*x for j,x in witness) == y for row,y in zip(A,b)):
        raise ValueError(f"Failed exact equation: {path.name}")
    sha = hashlib.sha256(json.dumps([A,b],separators=(',',':')).encode()).hexdigest()
    report_path = path.with_name(path.name.replace("_system.json.gz",".json"))
    report = json.loads(report_path.read_text())
    case = (report["source"],report["tau"],report["height"])
    if case not in EXPECTED or case in seen or (len(A),len(A[0])) != EXPECTED[case]:
        raise ValueError("Incorrect or duplicate source/sign/height/system size")
    seen.add(case)
    rec = next((r for r in report["branch_records"] if r.get("system_sha256") == sha),None)
    if rec is None or rec.get("exact_witness") != data["witness"]:
        raise ValueError("Report and portable system disagree")
    if any(Fraction(x) not in (Fraction(-1),Fraction(1,2))
           for x in rec["projected_indicators"]):
        raise ValueError("Projected indicator outside Clifford set")
    receipts.append({"source":report["source"],"tau":report["tau"],
                     "height":report["height"],"rows":len(A),"columns":len(A[0]),
                     "nonzero_variables":len(witness),"system_sha256":sha,
                     "projected_indicators":rec["projected_indicators"],
                     "all_equations_exact":True})
if seen != set(EXPECTED):
    raise ValueError("Not all four expected cases were replayed")
out = {"classification_change":False,"scope":"Exact feasibility of necessary relaxations only",
       "receipts":receipts}
(HERE/"discrete_witness_replay.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
