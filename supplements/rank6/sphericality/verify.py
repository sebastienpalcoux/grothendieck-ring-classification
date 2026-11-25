"""Reproduce the finite computations in Sphericality in Rank Six.

Run python verify.py from the extracted source, or use --list to see the tasks.
The input files are copied to a temporary directory before regeneration.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
from time import monotonic


CHECKS = """
short_orbit_check.py
golden_orbit_check.py
golden_two_pairs_check.py
golden_rational_two_check.py
golden_witness_parity.py
verify_conductor_twelve_rows.py
folded_twelve_check.py
folded_silver_check.py
silver_four_distinct_check.py
silver_small_check.py
silver_residual_check.py
silver_four_sixteen_check.py
silver_large_pairs_check.py
verify_quartic_bounds.py
verify_quartic_half_ten.py
quartic_more/verify.py
verify_quartic_silver_fields.py
generic_quartic/verify_quartic_fields.py
generic_quartic/golden_biquadratic.py
generic_quartic/cyclic_five.py
generic_quartic/c15_lattice.py
generic_quartic/three_five.py
generic_quartic/short24/height.py
generic_quartic/short24/verify.py
generic_quartic/short24/large_mass.py
generic_quartic/general24/verify.py
field_checks/twentyfour/ordinary_silver.py
field_checks/sixteen/nonhalf_height.py
field_checks/sixteen/nonhalf_verify.py
field_checks/sixteen/half_silver.py
field_checks/sixteen/short_height.py
field_checks/sixteen/irr_verify.py
field_checks/forty/verify.py
field_checks/half/verify.py
field_checks/forty/quadratic40.py
field_checks/forty/joint8.py
field_checks/forty/primitive9.py
field_checks/moments/moments24.py
field_checks/moments/quartic24.py
field_checks/moments/quartic24_two_primes.py
field_checks/moments/moments16.py
field_checks/moments/quartic16.py
generic_quartic/sixteen.py
quartic24_nonhalf_height.py
quartic24_nonhalf_check.py
quadratic_conductor_check.py
quadratic_trace_bounds.py
quadratic_24_28_checks/quadratic_twenty_eight_mass_audit.py
quadratic_24_28_checks/quadratic_twenty_four_imaginary_audit.py
quadratic_24_28_checks/quadratic_twenty_four_rational_audit.py
quartic_quadratic_dimension_check.py
odd_degree_checks/cubic_codegree_gap.py
odd_degree_checks/cubic_height_check.py
odd_degree_checks/cubic_ratio_bound.py
odd_degree_checks/cubic_ratio_fourier.py
odd_degree_checks/cubic_seven_lattice_check.py
odd_degree_checks/higher_degree_quintic.py
quartic_rational_frontier/verify_rational_frontier.py
sextic_height_bound.cpp
sextic_certificates/verify_sextic.py
sextic_complement/verify_complement.py
field_checks/moments/adjacent16.cpp
""".split()


def run(command, cwd, env):
    result = subprocess.run(command, cwd=cwd, env=env, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(f"{' '.join(map(str, command))} returned {result.returncode}\n{result.stdout}")
    return result.stdout


def verify_task(root, filename, env):
    path = root / filename
    started = monotonic()
    if path.suffix == ".py":
        # The full-degree drivers use relative paths for intermediate work.
        local = path.parent.name in {"sextic_certificates", "sextic_complement"}
        args = [sys.executable, str(path)]
        if path.name == "verify_complement.py":
            args += ["--jobs", "1"]
        output = run(args, path.parent if local else root, env)
    else:
        binary = root / (path.stem + "-verifier")
        run(["c++", "-std=c++17", "-O3", path, "-o", binary], root, env)
        if path.stem == "sextic_height_bound":
            output = run([binary, "200"], root, env)
            if not re.search(r"EXCLUDED; denominator=200; nodes=8312559; moment_leaves=3200466;", output):
                raise RuntimeError("Unexpected sextic height totals\n" + output)
        else:
            output = run([binary], root, env)
            visited = [int(n) for n in re.findall(r"visited (\d+)", output)]
            if visited != [13777, 3471, 2531, 2397, 2373, 2375, 2375, 2373]:
                raise RuntimeError("Unexpected conductor-sixteen interval counts\n" + output)
    return monotonic() - started, output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="list all checks and exit")
    parser.add_argument("--jobs", type=int, default=2, help="number of checks to run concurrently (default 2)")
    parser.add_argument("--verbose", action="store_true", help="show the calculations printed by each verifier")
    args = parser.parse_args()
    if args.list:
        print("\n".join(CHECKS))
        return 0
    if args.jobs < 1 or not __debug__:
        parser.error("use unoptimized Python and a positive worker count")
    src = Path(__file__).resolve().parent
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", OPENBLAS_NUM_THREADS="1",
               MKL_NUM_THREADS="1", OMP_NUM_THREADS="1")
    env.pop("PYTHONOPTIMIZE", None)
    failed = []
    with TemporaryDirectory(prefix="rank-six-") as tmp:
        root = Path(tmp)
        for path in src.rglob("*"):
            if path.is_file() and path.suffix in {".py", ".cpp", ".json"}:
                destination = root / path.relative_to(src)
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(path, destination)
        with ThreadPoolExecutor(max_workers=args.jobs) as executor:
            tasks = {executor.submit(verify_task, root, path, env): path for path in CHECKS}
            for task in as_completed(tasks):
                path = tasks[task]
                try:
                    seconds, output = task.result()
                except (OSError, RuntimeError) as exc:
                    failed.append(path)
                    print(f"FAIL {path}\n{exc}", file=sys.stderr, flush=True)
                else:
                    if args.verbose:
                        print(output.rstrip(), flush=True)
                    print(f"PASS {path} ({seconds:.1f} s)", flush=True)
    if failed:
        print(f"{len(failed)} of {len(CHECKS)} checks failed.", file=sys.stderr)
        return 1
    print(f"All {len(CHECKS)} checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
