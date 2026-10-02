# Rank-eight Grothendieck rings through multiplicity two

The complete census contains 96 rings of exact multiplicity one and 877 of exact multiplicity two. It is pinned at commit `b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726` of [fusion-ring-census](https://github.com/sebastienpalcoux/fusion-ring-census); the uncompressed tensor digest is `97b86d2de8ca0352c5c6e14686cd1d43dbd52180dc53b2ff1ccf7a61788c9600`.

| Exact multiplicity | Fusion rings | Generally excluded | Unitarily realized | Generally unresolved |
|---:|---:|---:|---:|---:|
| 1 | 96 | 45 | 48 | 3 |
| 2 | 877 | 801 | 24 | 52 |
| Total | 973 | 846 | 72 | 55 |

These realization counts are lower bounds for complex Grothendieck-ring types. Read the [manuscript source](paper/rank8.tex) and [PDF](paper/rank8.pdf). The authoritative `data/classification.json` records every census tensor and status; `data/realized_models.json` records independent model tensors and exact basis permutations. Each positive comparison checks all 512 ordered coefficients.

The [latest residual stage](../../evidence/upper_residual_20261002b/README.md) adds twelve unitary models and fourteen general exclusions. The models include pointed equivariantizations, affine-group representations, bosonic quotients, D14, a Morita dual, charge-conjugation defects, a Davydov–Runkel extension and the unitary Haagerup–Izumi C7 dual. General obstructions use prime descent, semisimple Hopf algebras, rank-one modules and an adjoint criterion in dimension twenty-eight and a unified two-object orbit obstruction in dimension ninety-six, and an order-four action obstruction in dimension one hundred eight.

Seven additional rings have unitary obstructions, and R8_2_312 has a pseudo-unitary obstruction. They remain generally unresolved. For R8_1_9, R8_1_18 and R8_1_49, general, pivotal, spherical and pseudo-unitary *existence* are equivalent by Galois conjugacy to a pseudo-unitary category; this does not assert every realization is pseudo-unitary. None admits a braiding. Their unrestricted existence remains open. No bosonicity conclusion is inferred from a possible central lift.

From the repository root:

```bash
python3 tools/verify_upper_residual_20261002b.py
python3 -O tools/verify_upper_residual_20261002b.py
```

The stage checks source hypotheses, complete independent model tensors, scoped certificates and preservation of previous decisions. The earlier [46-decision stage](../../evidence/residual_20261002/README.md) and [AnyonWiki evidence](../../evidence/anyonwiki/README.md) retain separate reports. The current stage automatically replays the historical constructors against isolated copies of their original ledgers and model catalogues. Original entry points are retained for provenance; they require their historical snapshots and should not be run directly against the expanded current catalogue.

The original `software/analyze.py` and `software/verify.py` retain the initial census analysis and full certificate checks. Later stages have their own exact replays; discovery timeouts never constitute exclusions. See the [verification guide](../../docs/VERIFY.md) for current synchronized release commands.
