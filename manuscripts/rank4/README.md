# Grothendieck rings of complex fusion categories: rank 4

**[Read the revised manuscript · 50 pages](../rank4.pdf)** ·
[Standalone TeX source](../rank4.tex) ·
[Hexagon source archive](../hexagon/hexagon-rank-4-source.zip) ·
[Exact verification package](../../supplements/rank4/sphericality/README.md)

Revised 19 November 2026, by Sébastien Palcoux. [Revision letter](../hexagon/revision-letter.pdf).

## The result and its dependencies

The paper treats arbitrary complex fusion categories of rank four, with no initial pivotality assumption or bound on fusion multiplicities. Every such category admits a spherical structure. Applying the pivotal classification of Dong, Palcoux and Plessis then gives exactly fifteen based rings, each with a unitary realization. The sharp bounds are global Frobenius–Perron dimension at most `24 + 12√3` and multiplicity at most `6`, with equality precisely for `NG(C₃,6)`.

Sphericality is established before the pivotal classification is invoked. The six non-self-dual rings are also recovered directly by central induction and positive twist moments. A hypothetical nonspherical category must be self-dual and have quadratic or quartic Frobenius–Perron dimension below `1000`, with multiplicities at most `31`.

## The finite calculation

The ordinary census contains **1,692 rings**: 1,642 self-dual and 50 with a dual pair. Structural and arithmetic conditions leave 41 ordinary inputs to the local descent. They give 1,798 signed tuples and 623 distinct pairs of an ordinary ring and a signed Casimir polynomial. Joint norm divisibility leaves two pairs, both for the same ordinary ring. Their inverse-square codegree sums are `1` and `23/24`, both larger than the necessary bound `7/8`. No nonspherical candidate remains.

The replay also checks the 14 short quadratic rows, 372 endpoint comparisons, both quartic estimates, and all fifteen model tensors and positive dimension characters. Its unpruned and small-box comparisons test enumeration coverage. The earlier global bank of 92,795 signed orbits and its full exclusion ledger are not inputs to this revised proof.

From the repository root:

```sh
cd supplements/rank4/sphericality
python3 verify.py --manuscript ../../../manuscripts/rank4.tex
```

Requirements: Python 3.10 or later, SymPy, and a C++17 compiler. See the [verification README](../../supplements/rank4/sphericality/README.md) for the exact scope of each check. The mathematical arguments remain subject to independent human review; finite replay is not proof-assistant verification.

## Earlier papers and related work

- [Earlier unrestricted and finite-range articles](papers/README.md), retained with their original sources and data.
- [Earlier unrestricted verification](../../supplements/rank4/unrestricted/README.md).
- [Finite census through multiplicity 128](../../supplements/rank4/PUBLIC_REPLAY.md).
- Dong–Palcoux–Plessis, [pivotal classification](https://arxiv.org/abs/2609.33272) and its [dedicated repository](https://github.com/sebastienpalcoux/pivotal-fusion-categories-rank-four).
- [All manuscripts](../README.md).
