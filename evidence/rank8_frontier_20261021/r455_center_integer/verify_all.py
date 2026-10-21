"""Canonical complete R455 general-exclusion arithmetic replay."""
from pathlib import Path
import json
import verify,pair_tensors,joint_rotation
HERE=Path(__file__).resolve().parent
actual=json.loads(json.dumps(verify.run(),default=int))
verify.need(actual==json.loads((HERE/'results.json').read_text()),'complete integer/cubic/spectrum/parity receipt')
print('PASS R455 complete812 integer Grams ->24 cubic ->12 parity patterns.',flush=True)
actual=pair_tensors.run()
verify.need(actual==json.loads((HERE/'pair_tensors.json').read_text()),'complete integer low-pair receipt')
print('PASS R455 all120 low-pair integer decompositions.',flush=True)
joint_rotation.run(False)
print('PASS complete R455 arithmetic exclusion replay; general scope uses the certified Galois-pseudo-unitary gate.',flush=True)
