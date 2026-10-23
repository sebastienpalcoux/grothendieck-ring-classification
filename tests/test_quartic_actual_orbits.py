"""Independent arithmetic controls for the new actual-orbit/Fourier adapter."""
import math
import os
from pathlib import Path
import unittest

from cases import r928_r941 as q


class ArithmeticControls(unittest.TestCase):
    def test_complete_squared_galois_partition(self):
        orbits = q.actual_orbits()
        self.assertEqual(sorted(e for orbit in orbits for e in orbit), list(range(q.N)))
        squares = {u*u % q.N for u in range(1,q.N,24)
                   if math.gcd(u,q.N) == 1}
        kernel48 = {u for u in range(q.N) if math.gcd(u,q.N) == 1 and u % 48 == 1}
        self.assertEqual(squares,kernel48)
        self.assertEqual(len(squares),24)

    def test_overlap_keeps_semion_charges_separate(self):
        orbit = next(o for o in q.actual_orbits()
                     if len(o) <= 4 and
                     set(o) == {(e+q.N//4) % q.N for e in o})
        packet = orbit+tuple((e+q.N//4) % q.N for e in orbit)
        self.assertEqual(len(packet),2*len(orbit))
        self.assertEqual(q.moment(packet,4),
                         q.field(48).scale(q.moment(orbit,4),2))

    def test_fermion_overlap_uses_set_union(self):
        orbit = next(o for o in q.actual_orbits()
                     if set(o) == {(e+q.N//2) % q.N for e in o})
        packet = set(orbit)|{(e+q.N//2) % q.N for e in orbit}
        self.assertEqual(len(packet),len(orbit))
        self.assertEqual(len(packet) % 2,0)

    def test_genuine_ninth_root_fourier_transform(self):
        f = q.field(144)
        self.assertEqual(f.degree,48)
        # A genuine one-dimensional order9 representation with eigenvalue zeta9^2.
        for eigen in range(9):
            total = f.sum(f.roots[((2-eigen)*k*(144//9)) % 144]
                          for k in range(9))
            self.assertEqual(total,f.scale(f.one,9 if eigen == 2 else 0))

    def test_cached_builder_matches_original_exact_arrays(self):
        import importlib.util
        import sys
        path = Path(__file__).with_name("orbit_baseline.py")
        spec = importlib.util.spec_from_file_location("orbit_baseline_control", path)
        baseline = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = baseline
        spec.loader.exec_module(baseline)
        vendor = Path(__file__).resolve().parents[1]/"vendor"
        a = baseline.build_one(vendor,"R8_3_928",baseline.BRANCHES["R8_3_928"][0],(3,4))
        b = q.build_one(vendor,"R8_3_928",q.BRANCHES["R8_3_928"][0],(3,4))
        for key in ("n","rows","rhs","lo","up","integrality"):
            self.assertEqual(a[key],b[key],key)

    def test_source_and_two_representative_builds(self):
        vendor = Path(os.environ.get("RANK8_VENDOR_ROOT",
                                     Path(__file__).resolve().parents[1]/"vendor"))
        if not (vendor/q.DEPENDENCIES[0]).is_file():
            self.skipTest("set RANK8_VENDOR_ROOT to the package vendor directory")
        report = q.self_test(vendor)
        self.assertEqual(report["status"],"PASS")
        self.assertEqual(len(report["representatives"]),2)


if __name__ == "__main__":
    unittest.main()
