"""Independent F4 character enumeration for the two formerly unresolved rank-five tensors.

Inputs: verified local classification_tensors.json. F4=F2[w]/(w^2+w+1),
represented by two-bit integers a+2b*w.
"""

import itertools
import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data/classification_tensors.json"


def add(a, b):
    return a ^ b


def mul(a, b):
    x, y = a & 1, a >> 1
    u, v = b & 1, b >> 1
    return (x * u ^ y * v) | ((x * v ^ y * u ^ y * v) << 1)


def main():
    rows = json.loads(DATA.read_text())
    targets = {(18, 5073), (18, 5076)}
    if {(row["m"], row["j"]) for row in rows if (row["m"], row["j"]) in targets} != targets:
        raise ValueError("both tensors required for independent audit")
    for row in rows:
        if (row["m"], row["j"]) not in targets:
            continue
        N = row["N"]
        chars = []
        for other in itertools.product(range(4), repeat=4):
            d = (1,) + other
            # Build every RHS in F4 using XOR, avoiding Python integer sums.
            valid = True
            for i in range(5):
                for j in range(5):
                    rhs = 0
                    for k in range(5):
                        if N[i][j][k] & 1:
                            rhs = add(rhs, d[k])
                    if mul(d[i], d[j]) != rhs:
                        valid = False
                        break
                if not valid:
                    break
            if valid:
                delta = 0
                for v in d:
                    delta = add(delta, mul(v, v))
                chars.append((d, delta))
        print(row["m"], row["j"], chars)


if __name__ == "__main__":
    main()
