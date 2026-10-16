"""Single specification of the finite proof's scope and file locations."""
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]
SPEC = json.loads((ROOT / "scope.json").read_text())
if SPEC.get("schema") != 1 or type(SPEC.get("bound")) is not int or not 1 <= SPEC["bound"] <= 128:
    raise ValueError("invalid finite-proof scope")
BOUND = SPEC["bound"]
CATALOG = ROOT / "data" / SPEC["catalog_file"]
MANIFEST = ROOT / "data" / SPEC["manifest_file"]
CERTIFICATES = ROOT / "data" / SPEC["certificate_file"]
