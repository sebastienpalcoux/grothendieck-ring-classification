#!/usr/bin/env python3
"""Check the recovery checkpoint. This does not replay the inaccessible original36 proofs."""
import argparse
import collections
import gzip
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASELINE = "7c78b88486d5412adeed10d77275e3eaa2de0b7d"

def require(condition, message):
    if not condition:
        raise ValueError(message)

def fingerprint(tensor):
    return hashlib.sha256(json.dumps(tensor, separators=(",", ":")).encode()).hexdigest()

def flat(tensor):
    return tuple(x for matrix in tensor for row in matrix for x in row)

def read_source(root, rank):
    path = root / "supplements" / ("rank%d" % rank) / "data" / ("rank%d_tables.txt.gz" % rank)
    packed = path.read_bytes()
    if rank == 7:
        require(hashlib.sha256(packed).hexdigest() ==
                "6ddea4c66de7fbe077e9552e71e8cf95ec3fec5bbd30a615e68e2d8fcb9ae9c9",
                "rank7 source archive digest")
    raw = gzip.decompress(packed)
    if rank == 8:
        require(hashlib.sha256(raw).hexdigest() ==
                "97b86d2de8ca0352c5c6e14686cd1d43dbd52180dc53b2ff1ccf7a61788c9600",
                "rank8 source text digest")
    tensors = [json.loads(line.replace("{", "[").replace("}", "]"))
               for line in raw.decode().splitlines() if line.strip()]
    grouped = collections.defaultdict(list)
    for tensor in tensors:
        grouped[max(flat(tensor))].append(tensor)
    expected = {1: 43, 2: 319, 3: 1059, 4: 2780} if rank == 7 else {1: 96, 2: 877}
    require({m: len(rows) for m, rows in grouped.items()} == expected, "source counts")
    # Rank7 IDs preserve raw source order; rank8 IDs use sorted full tensor order.
    if rank == 8:
        for rows in grouped.values():
            rows.sort(key=flat)
    return {"R%d_%d_%d" % (rank, m, j): tensor
            for m, rows in grouped.items() for j, tensor in enumerate(rows, 1)}

def validate_ring(tensor):
    n = len(tensor)
    require(all(len(matrix) == n and all(len(row) == n for row in matrix)
                for matrix in tensor), "tensor shape")
    require(all(type(v) is int and v >= 0 for v in flat(tensor)), "tensor coefficients")
    dual = []
    for i in range(n):
        hits = [j for j in range(n) if tensor[i][j][0]]
        require(len(hits) == 1 and tensor[i][hits[0]][0] == 1, "unique dual")
        dual.append(hits[0])
    require(all(dual[dual[i]] == i for i in range(n)), "dual involution")
    for i, j in itertools.product(range(n), repeat=2):
        require(tensor[0][i][j] == tensor[i][0][j] == int(i == j), "unit")
    for i, j, k in itertools.product(range(n), repeat=3):
        require(tensor[i][j][k] == tensor[dual[j]][dual[i]][dual[k]], "dual reciprocity")
        require(tensor[i][j][k] == tensor[dual[i]][k][j], "Frobenius reciprocity")
    for i, j, k, l in itertools.product(range(n), repeat=4):
        left = sum(tensor[i][j][s] * tensor[s][k][l] for s in range(n))
        right = sum(tensor[j][k][s] * tensor[i][s][l] for s in range(n))
        require(left == right, "associativity")
    return dual

def adjoint_closure(tensor, dual):
    result = {0}
    for i in range(len(tensor)):
        result.update(k for k, coefficient in enumerate(tensor[i][dual[i]]) if coefficient)
    changed = True
    while changed:
        old = set(result)
        for i, j in itertools.product(old, repeat=2):
            result.update(k for k, coefficient in enumerate(tensor[i][j]) if coefficient)
        changed = old != result
    return sorted(result)

def check_r694(tensor):
    dual = validate_ring(tensor)
    dims = [1, 1, 1, 1, 2, 4, 4, 4]
    for i, j in itertools.product(range(8), repeat=2):
        require(sum(c * dims[k] for k, c in enumerate(tensor[i][j])) == dims[i] * dims[j],
                "R694 exact dimension product")
    require(sum(x * x for x in dims) == 56, "R694 global dimension")
    require(adjoint_closure(tensor, dual) == list(range(8)), "R694 adjoint whole")
    require(fingerprint(tensor) ==
            "cad504d4abf1b34f332a7184d3cbf725d4e04d1fcb955fde654aa1516ec86831",
            "R694 census fingerprint")
    return {"global_dimension": 56, "dimensions": dims, "adjoint_whole": True}

def hi7_dual_tensor():
    n = 8
    tensor = [[[0] * n for _ in range(n)] for _ in range(n)]
    def b(x):
        x %= 7
        return None if x == 0 else 1 + min(x, 7 - x)
    def c(x):
        x %= 7
        return None if x == 0 else 4 + min(x, 7 - x)
    def add(v, k, q=1):
        if k is not None:
            v[k] += q
    def fill(i, j, v):
        tensor[i][j] = list(v)
        tensor[j][i] = list(v)
    for i in range(n):
        v = [0] * n
        v[i] = 1
        fill(0, i, v)
    fill(1, 1, [1] * n)
    for i in range(1, 4):
        v = [1] * n
        v[0] = v[b(i)] = 0
        fill(1, b(i), v)
        v = [1] * n
        v[0] = 0
        v[c(i)] = 2
        fill(1, c(i), v)
    for i, j in itertools.product(range(1, 4), repeat=2):
        v = [1] * n
        v[0] = 0
        fill(b(i), c(j), v)
        v = [1] * n
        v[0] = int(i == j)
        v[1] = int(i != j)
        add(v, b(i + j), -1)
        add(v, b(i - j), -1)
        fill(b(i), b(j), v)
        v = [1] * n
        v[0] = int(i == j)
        v[1] = 1 + int(i == j)
        add(v, c(i + j))
        add(v, c(i - j))
        fill(c(i), c(j), v)
    return tensor

def exact_dimension_products(tensor):
    # Coordinates in Z[d], d^2=1+7d; the chosen real d>7 makes all dimensions positive.
    dims = [(1, 0), (0, 1)] + [(-1, 1)] * 3 + [(1, 1)] * 3
    def multiply(x, y):
        a, b = x
        c, d = y
        return a * c + b * d, a * d + b * c + 7 * b * d
    for i, j in itertools.product(range(8), repeat=2):
        value = tuple(sum(tensor[i][j][k] * dims[k][a] for k in range(8)) for a in (0, 1))
        require(value == multiply(dims[i], dims[j]), "R868 exact dimension product")

def check_r868(census):
    tensor = hi7_dual_tensor()
    require(fingerprint(tensor) ==
            "02c8f84da2ea39eb781f4fb542565f4d90fc91c7f7b9246dd04c16f5a1b8152a",
            "R868 model fingerprint")
    validate_ring(tensor)
    exact_dimension_products(tensor)
    p = [0, 3, 1, 2, 4, 5, 7, 6]
    require(all(tensor[i][j][k] == census[p[i]][p[j]][p[k]]
                for i, j, k in itertools.product(range(8), repeat=3)),
            "R868 complete tensor identification")
    return {"model_to_census": p, "coefficients_matched": 512,
            "associativity_relations": 4096, "exact_dimension_products": 64}

def controls():
    require(hashlib.sha256(b"abc").hexdigest() ==
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad", "hash control")
    tensor = hi7_dual_tensor()
    validate_ring(tensor)
    bad = json.loads(json.dumps(tensor))
    bad[1][1][0] = 0
    try:
        validate_ring(bad)
    except ValueError:
        pass
    else:
        raise ValueError("negative dual control accepted")
    require(fingerprint(bad) != fingerprint(tensor), "tamper control")
    return ["hash_control", "valid_HI7_tensor", "corrupt_duality_rejected", "tamper_digest_changes"]

def verify(root):
    checkpoint = json.loads((HERE / "checkpoint.json").read_text())
    require(checkpoint["baseline_commit"] == BASELINE, "wrong published baseline")
    for name, digest in json.loads((HERE / "source_files.json").read_text())["sha256"].items():
        require(Path(name).name == name, "unsafe manifest path")
        require(hashlib.sha256((HERE / name).read_bytes()).hexdigest() == digest,
                "checkpoint file digest: " + name)
    sources = read_source(root, 7)
    sources.update(read_source(root, 8))
    old7 = json.loads((root / "supplements/rank7/output/rank7_ledger.json").read_text())
    old8 = json.loads((root / "supplements/rank8/data/decisions.json").read_text())
    old = {row["id"]: row for row in old7 + old8}
    require(len(old) == 5174, "published ledger coverage")
    for row in old7:
        require(row["tensor"] == sources[row["id"]], "rank7 published source binding")
    for row in old8:
        require(row["tensor_sha256"] == fingerprint(sources[row["id"]]),
                "rank8 published tensor digest")
    previous = json.loads((HERE / "previous_records.json").read_text())
    previous_ids = {row["id"] for row in previous}
    require(len(previous) == len(previous_ids) == 140, "original open inventory")
    require(previous_ids == {row["id"] for row in old.values() if row["status"] == "unresolved"},
            "open source inventory mismatch")
    for row in previous:
        rank = int(row["id"].split("_")[0][1:])
        if rank == 7:
            require(row == old[row["id"]], "rank7 previous record changed")
        else:
            prior = {k: v for k, v in row.items() if k not in ("rank", "census_tensor")}
            require(prior == old[row["id"]], "rank8 previous record changed")
            require(row["census_tensor"] == sources[row["id"]], "rank8 input tensor changed")
    decisions = json.loads((HERE / "decisions.json").read_text())
    require(len(decisions) == len({row["id"] for row in decisions}) == 38, "decision inventory")
    require(collections.Counter(row["status"] for row in decisions) ==
            {"excluded": 25, "unitarily_realized": 13}, "decision counts")
    statuses = {k: row["status"] for k, row in old.items()}
    for row in decisions:
        require(row["id"] in previous_ids, "transition outside original open cases")
        require(row["census_tensor"] == sources[row["id"]], "new decision source tensor")
        require(row["census_tensor_sha256"] == fingerprint(sources[row["id"]]),
                "new decision tensor digest")
        if row["status"] == "excluded":
            require(row["scope"] == "general_complex", "scoped obstruction promoted to general")
        else:
            require(row["scope"] == "unitary", "model scope")
            p = row["model_to_census"]
            require(p[0] == 0 and sorted(p) == list(range(row["rank"])), "basis map")
        validate_ring(row["census_tensor"])
        statuses[row["id"]] = row["status"]
    for rank in (7, 8):
        for summary in checkpoint["rank%d" % rank]:
            prefix = "R%d_%d_" % (rank, summary["multiplicity"])
            counts = collections.Counter(value for key, value in statuses.items() if key.startswith(prefix))
            require(counts == collections.Counter({"excluded": summary["excluded"],
                               "unitarily_realized": summary["models"],
                               "unresolved": summary["unresolved"]}), "checkpoint status totals")
    remaining = json.loads((HERE / "remaining_ids.json").read_text())
    require(len(remaining) == len(set(remaining)) == 102, "remaining inventory")
    require(set(remaining) == {key for key, value in statuses.items() if value == "unresolved"},
            "remaining IDs mismatch")
    return {"status": "PASS", "decision_source_bindings": 38,
            "rank7_source_records": 4201, "rank8_digest_records": 973,
            "working_general_unresolved": {"rank7": 42, "rank8": 60},
            "R694": check_r694(sources["R8_2_694"]),
            "R868": check_r868(sources["R8_2_868"]),
            "controls": controls(),
            "scope": "checkpoint integrity, counts, ring axioms, R694 premises and R868 model only",
            "original36_full_proof_replay": "pending workspace recovery",
            "manuscript_website_publication": "pending"}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, default=HERE.parents[1])
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    result = {"status": "PASS", "controls": controls()} if args.self_test else verify(args.repository.resolve())
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
