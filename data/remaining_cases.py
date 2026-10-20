"""Exact fusion tensors of the current open general-complex cases.

N[i][j][k] is the coefficient of basis object k in the product i * j.
Basis indices are zero-based; index 0 is the unit. Each named tensor is a
plain Python list of lists of lists. No third-party dependency is needed.
Example: from remaining_cases import R6_4_155, DUALS

These fusion rings are unresolved; tensor consistency does not construct
a fusion category. AI-generated research: independent human verification
and Lean formalization are pending. Use the results and data with caution.
Tensor hashes use UTF-8 JSON with separators=(',', ':') and no trailing newline.
"""

R6_4_155 = [
    [
        [1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1],
    ],
    [
        [0, 1, 0, 0, 0, 0],
        [0, 4, 4, 0, 1, 1],
        [1, 4, 4, 1, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
    ],
    [
        [0, 0, 1, 0, 0, 0],
        [1, 4, 4, 1, 0, 0],
        [0, 4, 4, 0, 1, 1],
        [0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
    ],
    [
        [0, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1, 0],
    ],
    [
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0],
    ],
    [
        [0, 0, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 0],
        [1, 0, 0, 0, 0, 0],
    ],
]

R6_8_1660 = [
    [
        [1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1],
    ],
    [
        [0, 1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1],
    ],
    [
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [1, 0, 3, 3, 0, 4],
        [0, 1, 3, 3, 0, 4],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 4, 4, 1, 6],
    ],
    [
        [0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 1, 3, 3, 0, 4],
        [1, 0, 3, 3, 0, 4],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 4, 4, 1, 6],
    ],
    [
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 1],
        [1, 1, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0],
    ],
    [
        [0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 4, 4, 1, 6],
        [0, 0, 4, 4, 1, 6],
        [0, 0, 1, 1, 0, 0],
        [1, 1, 6, 6, 0, 8],
    ],
]

DUALS = {'R6_4_155': [0, 2, 1, 3, 4, 5], 'R6_8_1660': [0, 1, 2, 3, 4, 5]}

METADATA = {
    "R6_4_155": {
        "rank": 6,
        "multiplicity": 4,
        "index": 155,
        "status": "unresolved",
        "unit_index": 0,
        "source": "supplements/rank6/data/unresolved_tensors.json",
        "source_sha256": "cf1f3ac0d2b05062861f036932bdb140a5a5f0055dd054689b6e1fa67924d203",
        "tensor_sha256": "012ef716d19b96a2a800d7bcbb33f3ae5e99e3c6a223f6e14bcd20144d4072a3",
        "selection": "JSON record with this id"
    },
    "R6_8_1660": {
        "rank": 6,
        "multiplicity": 8,
        "index": 1660,
        "status": "unresolved",
        "unit_index": 0,
        "source": "supplements/rank6/data/unresolved_tensors.json",
        "source_sha256": "cf1f3ac0d2b05062861f036932bdb140a5a5f0055dd054689b6e1fa67924d203",
        "tensor_sha256": "697ec27fe203356199bfcf674587be9c71455dbb681f2e086a076f726b03d267",
        "selection": "JSON record with this id"
    }
}

TENSORS = {'R6_4_155': R6_4_155, 'R6_8_1660': R6_8_1660}
