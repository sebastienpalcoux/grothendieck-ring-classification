"""Regenerate the bounded unit-square lists and independently check every dual."""
from pathlib import Path
import json

from positive_dnumber_squares import enumerate_ratios
from sextic_polytope import verify

base = Path(__file__).resolve().parent
for conductor, counts in [(7, (369, 284)), (9, (271, 206))]:
    data = enumerate_ratios(8, conductor, 200)
    all_ratios = data["candidates"]
    assert (len(all_ratios), sum(a["degree"] == 6 for a in all_ratios)) == counts
    verify(8, conductor)
    out = json.loads((base / f"sextic_8_{conductor}_polytope.json").read_text())
    assert out["survivors"] == []
print("All 490 primitive ratios excluded exactly.")
