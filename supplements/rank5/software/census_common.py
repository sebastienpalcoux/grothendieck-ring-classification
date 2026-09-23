"""Tensor axioms and exact isomorphism matching against the pinned census.

The pinned rank-five repository table is the census input. The local tensor
ledger keeps historical basis choices only to address classification witnesses.
"""
import csv
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import numpy as np
from exact import require

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / 'data/pinned_repository/rank5/tables.txt.gz'
COUNTS = ROOT / 'data/pinned_repository/rank5/counts.csv'
TABLES_SHA256 = '4542c0871498337ef38ce3903407933289699a5ff06c85ad0f6c2bd57da823fb'
PERMS = [(0,) + p for p in itertools.permutations(range(1, 5))]
MAPS = np.array([[25*p[i] + 5*p[j] + p[k]
                  for i in range(5) for j in range(5) for k in range(5)]
                 for p in PERMS])


def canonical(N):
    flat = np.asarray(N, dtype=np.int64).ravel()
    require(flat.shape == (125,), 'rank-five tensor shape')
    return min(tuple(map(int, row)) for row in flat[MAPS])


def check_axioms(N):
    require(isinstance(N, list) and len(N) == 5, 'rank-five tensor expected')
    require(all(type(x) is int and 0 <= x <= 32 for mat in N for row in mat for x in row),
            'integer tensor bound 0..32')
    A = np.array(N, dtype=np.int64)
    eye = np.eye(5, dtype=np.int64)
    require(A.shape == (5, 5, 5), 'tensor shape')
    require(np.array_equal(A[0], eye) and np.array_equal(A[:, 0], eye), 'unit equations')
    du = np.argmax(A[:, :, 0], axis=1).tolist()
    require(all(du[du[i]] == i for i in range(5)), 'involutive duality')
    require(np.array_equal(A[:, :, 0], eye[du]), 'duality coefficients')
    for i, j, k in itertools.product(range(5), repeat=3):
        require(A[i, j, k] == A[j, i, k] == A[du[i], k, j] == A[k, du[j], i],
                'Frobenius reciprocity')
    for i, j in itertools.product(range(5), repeat=2):
        require(np.array_equal(A[i] @ A[j], np.tensordot(A[i, j], A, axes=1)),
                'associativity')


def pinned_prefix(bound=18):
    """Read the pinned repository table, enforcing unique canonical classes."""
    require(hashlib.sha256(TABLES.read_bytes()).hexdigest() == TABLES_SHA256,
            'pinned repository tensor-file SHA-256 mismatch')
    classes, counts = set(), {}
    with COUNTS.open(newline='') as stream:
        for row in csv.reader(stream):
            if row and row[0].isdigit() and int(row[0]) == 5:
                counts[int(row[1])] = int(row[2])
    require(all(m in counts for m in range(1, bound + 1)), 'missing pinned count')
    by_m = {}
    with gzip.open(TABLES, 'rt') as stream:
        for line in stream:
            N = json.loads(line.replace('{', '[').replace('}', ']'))
            m = max(x for mat in N for row in mat for x in row)
            if m > bound:
                continue
            check_axioms(N)
            key = canonical(N)
            require(key not in classes, 'pinned repository has duplicate isomorphism classes')
            classes.add(key)
            by_m[m] = by_m.get(m, 0) + 1
    require(all(by_m.get(m, 0) == counts[m] for m in range(1, bound + 1)),
            'pinned repository tensor/count mismatch')
    return classes, {m: counts[m] for m in range(1, bound + 1)}
