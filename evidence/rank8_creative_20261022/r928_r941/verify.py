#!/usr/bin/env python3
"""Read-only exact replay of the quartic refinements, including under python -O."""
from pathlib import Path
import argparse, concurrent.futures, hashlib, json, os, subprocess, sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TASKS = [
    ["dimension_mask.py", "--ring", str(n), *option]
    for n in (928, 941)
    for option in ([], ["--conductor"], ["--spectral"])
] + [
    ["r982_mask.py", "--conductor"], ["r982_mask.py", "--spectral"],
    ["complex_semion.py"], ["packet_closure.py"],
]

def require(condition, message):
    if not condition:
        raise ValueError(message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write this new evidence manifest after exact replay")
    args = parser.parse_args()
    own = sorted(p for p in HERE.iterdir() if p.suffix in (".py", ".md", ".json")
                 and p.name not in ("verification.json", "R941_packet_closure_8.json"))
    sources = [
        "evidence/rank8_frontier_20261021/quartic_integer_center/source.json",
        "evidence/rank8_frontier_20261021/quartic_integer_center/gram_cubic.json",
        "evidence/rank8_frontier_20261021/quartic_integer_center/r941_charges.json",
        "evidence/rank8_frontier_20261021/quartic_integer_center/r941_paired_rotation.py",
        "evidence/rank8_frontier_20261021/quartic_integer_center/r941_paired_rotation.json",
        "evidence/rank8_frontier_20261021/r928_semion_rotation/pair_rotation.py",
        "evidence/rank8_frontier_20261021/r928_semion_rotation/pair_rotation.json",
        "evidence/rank8_frontier_20261021/review/r941_fusion_traces.json",
        "evidence/rank8_next_20261021/semion_fermion/charged_quartic_pair.json",
        "evidence/rank8_next_20261021/semion_fermion/integer_pair_completion.json",
        "evidence/rank8_next_20261021/semion_fermion/quartic_pair.py",
        "evidence/rank8_next_20261021/r982/joint_phase_system.json",
        "evidence/rank8_frontier_20261021/commutative_integer/R8_3_982_profile.json",
        "evidence/rank8_creative_20261022/unified/composite_verification.json",
    ]
    paths = own + [ROOT / p for p in sources]
    hashes = {str(p.relative_to(ROOT)): sha(p) for p in paths}
    path = HERE / "verification.json"
    saved = None if args.write else json.loads(path.read_text())
    if saved is not None:
        require(saved["bindings"] == hashes, "evidence/input binding changed")

    env = {**os.environ, "OPENBLAS_NUM_THREADS": "1", "OMP_NUM_THREADS": "1"}
    def run(task):
        command = [sys.executable] + (["-O"] if sys.flags.optimize else [])
        command += [str(HERE / task[0]), *task[1:]]
        result = subprocess.run(command, cwd=ROOT, env=env, text=True, capture_output=True)
        require(result.returncode == 0, "replay failed: " + " ".join(task) + "\n" + result.stdout[-1500:] + result.stderr[-1500:])
        print("PASS " + " ".join(task), flush=True)
        return {"command": task, "result": "PASS"}

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        replay = list(pool.map(run, TASKS))
    for n, count in ((928, 10), (941, 14)):
        for kind in ("dimension", "conductor", "spectral"):
            data = json.loads((HERE / f"R{n}_{kind}_mask.json").read_text())
            require(len(data["cases"]) == count, "complete prior pattern domain")
            require(all(c["decision"]["status"] == "exact_feasible_relaxation" for c in data["cases"]), "phase outcome")
    complex_data = json.loads((HERE / "R928_complex_semion.json").read_text())
    require(len(complex_data["cases"]) == 10, "complete oriented semion domain")
    require(all(c["decision"]["status"] == "exact_feasible_relaxation" for c in complex_data["cases"]), "complex phase outcome")
    closure = json.loads((HERE / "R941_packet_closure.json").read_text())["records"]
    require(len(closure) == 14, "complete fermionic closure domain")
    require(all(c["degree_two_span_rank"] == 15 and c["generator_products_tested"] == 75
                and c["zero_residual_count"] == 55 and not c["forced_fusion_failures"]
                and not c["closed_generated_algebra"] for c in closure), "forced product outcome")
    output = {"status": "PASS", "bindings": hashes, "exact_replays": replay,
              "R928_patterns": 10, "R941_allocations": 14,
              "R941_forced_products_per_allocation": 55,
              "scope": "Exact necessary relaxations and forced fusion products; these calculations provide no categorification or new exclusion."}
    if args.write:
        path.write_text(json.dumps(output, indent=2) + "\n")
    else:
        require(output == saved, "deterministic verification result")
    print("PASS quartic refinements", flush=True)

if __name__ == "__main__":
    main()
