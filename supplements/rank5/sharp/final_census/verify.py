"""Regenerate the joint sharp window and verify every categorification decision."""
from collections import Counter
from pathlib import Path
import json
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
GENERATOR = ROOT / "generator"
sys.path.insert(0, str(GENERATOR))
from export_tables import tensor
sys.path.insert(0, str(ROOT / "criteria"))
from exact import require
from rings import canonical, codegree_poly, flat, validate
from model_registry import build_model_registry, match_model
from decisions import verify
from dimension_test import at_most_sharp_bound


def generate(directory):
    bounded = {}
    all_classes = set()
    bands = Counter()
    passing_bands = Counter()
    for kind in ("selfdual", "nonselfdual"):
        binary = directory / kind
        source = GENERATOR / f"enumerate_{kind}.cpp"
        compile_args = ["g++", "-O3", "-std=c++17"]
        if kind == "selfdual":
            compile_args.append("-fopenmp")
        subprocess.run([*compile_args, str(source), "-o", str(binary)], check=True)
        run = subprocess.run([str(binary), "4"], check=True, text=True, capture_output=True)
        for line in run.stdout.splitlines():
            N = tensor(5, line, GENERATOR)
            validate(N)
            key = canonical(N)
            m = max(flat(N))
            require(key not in all_classes and m <= 4, "overlap or excess in generation")
            all_classes.add(key)
            bands[m] += 1
            if at_most_sharp_bound(codegree_poly(N).all_coeffs()):
                bounded[key] = m
                passing_bands[m] += 1
    require(bands == {1:16, 2:37, 3:82, 4:134}, "unexpected multiplicity bands")
    require(len(bounded) == 114, "unexpected joint window size")
    return bounded, bands, passing_bands


def main():
    if not __debug__:
        raise RuntimeError("Run the verifier with Python assertions enabled")
    with tempfile.TemporaryDirectory() as tmp:
        bounded, bands, smaller = generate(Path(tmp))
    records = json.loads((ROOT / "data" / "bounded_witnesses.json").read_text())
    require(len(records) == len(bounded), "wrong witness count")
    models = build_model_registry()
    seen_models = set()
    overview = Counter()
    by_m = Counter()
    for record in records:
        N = record["N"]
        validate(N)
        key = canonical(N)
        require(key in bounded, "duplicate or out-of-window witness")
        m = bounded.pop(key)
        if "model" in record:
            require("exclusion" not in record, "conflicting decisions")
            computed = match_model(N, models)
            require(computed == record["model"] and computed is not None, "model map failed")
            require(computed["model"] not in seen_models, "repeated model")
            seen_models.add(computed["model"])
            overview["model"] += 1
            by_m[m,"model"] += 1
        else:
            certificate = record["exclusion"]
            verify(N, certificate)
            overview[certificate["kind"]] += 1
            by_m[m,"excluded"] += 1
    require(not bounded and seen_models == set(range(17)), "incomplete decisions")
    require(overview == dict(dnumber=76,subring=2,induction=10,finite_indicator_traces=4,fp_norm=3,fp_dimension_field=2,model=17),
            "unexpected decision group sizes")
    print("mu | generated | within dimension bound | excluded | realized")
    for m in sorted(bands):
        print(m, bands[m], smaller[m], by_m[m,"excluded"], by_m[m,"model"], sep=" | ")
    print("Verified all 97 exclusions and all 17 based-ring model identifications.")
    print("Exclusions by type:", {kind:n for kind,n in sorted(overview.items()) if kind != "model"})


if __name__ == "__main__":
    main()
