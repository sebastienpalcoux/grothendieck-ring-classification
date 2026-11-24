"""Replay the structural bound and the classification within that bound."""
import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
BOUNDS = (
    "verify_quintic_trace.py", "verify_quadratic_120.py", "verify_biquartic.py",
    "verify_cyclic_quartic.py", "quartic_fields.py",
    "exchange_cut.py", "cubic_polar_sieve.py",
    "verify16.py", "verify_quartic_moments.py", "verify15.py", "quartic_five_twists.py",
    "quartic_generator_bound.py",
    "biquad_sieve.py", "cyclic_dimension.py", "small_simple.py",
    "verify_exchange.py", "quadratic_profiles.py", "small_cubic.py",
)


def main():
    if not __debug__:
        raise RuntimeError("Run the verifier with Python assertions enabled")
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--bounds-only", action="store_true")
    group.add_argument("--classification-only", action="store_true")
    args = parser.parse_args()
    if not args.classification_only:
        for program in BOUNDS:
            print(program, flush=True)
            subprocess.run([sys.executable, str(ROOT / "checks" / program)], check=True)
        print(f"All {len(BOUNDS)} structural checks passed.", flush=True)
    if not args.bounds_only:
        print("Classification within both sharp bounds", flush=True)
        subprocess.run([sys.executable, str(ROOT / "final_census" / "verify.py")], check=True)


if __name__ == "__main__":
    main()
