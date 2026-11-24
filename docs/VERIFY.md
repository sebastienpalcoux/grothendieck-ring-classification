# Verify the current publication

> **AI-generated research; independent human verification pending.** Exact checks establish only their stated computational scope.

## Rank-five sharp classification (24 November 2026)

The current rank-five paper proves sphericality and Galois pseudo-unitarity
and classifies all seventeen based rings, without an initial pivotality
assumption. From the repository root:

```sh
python3 -m pip install sympy==1.14.0 numpy==2.3.5
cd supplements/rank5/sharp
python3 verify.py
```

Use Python 3.12 and a C++17 `g++` compiler with OpenMP support. Run ordinary
Python with assertions enabled, without `-O`. The replay checks eighteen
structural calculations, regenerates 269 rings of multiplicity at most four,
retains 114 within the sharp dimension bound, and verifies 97 exclusions
and seventeen model identifications. The categorical reductions and finite
search bounds are proved in the paper; matching model tensors does not
replace the cited categorical constructions. See the
[reading guide](../manuscripts/rank5/README.md),
[paper](../manuscripts/rank5.pdf) and
[exact replay and optional checks](../supplements/rank5/sharp/README.md).

## Revised ranks 2–4 series (19 November 2026)

Ranks two and three have computer-free proofs. The rank-four paper has a compact local sphericality replay, followed mathematically by the cited pivotal classification. After cloning the repository:

```sh
cd supplements/rank4/sphericality
python3 verify.py --manuscript ../../../manuscripts/rank4.tex
```

Use Python 3.10 or later, SymPy and a C++17 compiler. This freshly regenerates the 1,692-ring ordinary census, checks the local descent to zero nonspherical candidates, verifies the analytic estimates, and checks all fifteen model tensors and the printed model table. See the [complete scope](../supplements/rank4/sphericality/README.md) and [paper](../manuscripts/rank4.pdf).

## Earlier atlas and frontier verification

The following workflow retains its separate atlas and frontier scope. After cloning the classification repository:

~~~sh
python3 -m pip install sympy==1.14.0 numpy==2.3.5 pypdf==6.10.0
python3 tools/restore_data.py
python3 tools/verify_current_publication.py
python3 tools/verify_current_publication.py --metadata-only
python3 evidence/frontier/replay/current/run_checks.py --include-native --receipt /tmp/fusion-frontier-current.json
python3 evidence/frontier/replay/run_checks.py
~~~

The first command installs the verification dependencies; the second restores checksummed data. The next two validate the current ledgers, documents, website copies, profile scopes and tensors; full mode also recomputes structural ring properties. The current runner replays 28 finite checks, including the new R137 certificates and exact B20-02148 comparison. The final command separately replays twelve frozen predecessor checks, including the six complete-domain R1768 separators. Neither runner performs optimization or an associator search. Run it with ordinary Python, since some short matrix verifiers use assertions.

For runtime dependencies and the explicit inherited mathematical premises, read [the current proof index](../evidence/frontier/README.md) and [R1768 replay instructions](../evidence/frontier/replay/new/r1768/REPLAY_README.md).

Earlier categorical certificates stay in their frozen rank-specific contexts. The current replay does not claim to repeat every previous exclusion or establish external hypotheses by arithmetic alone. [Manuscripts](../manuscripts/README.md) identify the corresponding proof for each rank.

