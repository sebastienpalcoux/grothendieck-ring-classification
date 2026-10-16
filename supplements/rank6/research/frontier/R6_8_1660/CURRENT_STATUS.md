# R6_8_1660: unresolved Ising-based ring

> **AI-generated research · independent verification pending.** The proofs and
> data have not been independently human-verified or Lean-formalized. Exact
> computations establish only their stated scope.

The commuting generators satisfy `g²=1`, `gσ=σ`, `σ²=1+g` and
`X²=1+(3(1+g)+4σ)X`. The simple basis is `1,g,X,gX,σ,T`, where `T=σX`.
The positive dimension of X is `d=3+2√2+2√3+√6`, with global dimension `4(1+d²)`.

A hypothetical categorification has one possible relative-center based ring,
up to exchanging its Ising factors. The bounded domain satisfying the exact
phase Gram constraints contains **640 labelled restriction-data profiles**,
in branches **68, 286, 286**. These are necessary restriction data, not
categories, associators or complete modular fusion matrices.
Every indecomposable module category has six simples. Exact Morita and
indicator restrictions leave three possible dual based rings: the original
rank-six ring, a rank-six ring containing Ad(E6), and a noncommutative
rank-eight ring. None of these necessary alternatives supplies associators.

In the positive spherical representative, saturated modular representations
determine all indicator sequences and every central phase mass, with indicator
period dividing 48. The eight spin objects form four dual pairs; each has
restriction `2X+2gX+σ+3T`. These formulas include `nu_3(T)=2` and two conjugate
options for `nu_3(X)`. The [phase-mass chapter](../../../../../manuscripts/rank6/papers/chapters/frontier_1660_phase_masses.tex)
states the hypotheses and the exact profile domain.

An exact Verlinde calculation rejects a rank-37 candidate because
one fusion coefficient is 1/2; other profiles remain possible. The twist-one
support is the six simple summands of the induced unit, and the recorded
arguments give fully-faithful tensor-functor rigidity. No general exclusion
or categorification is established.

The [current manuscript](../../../../../manuscripts/rank6/papers/manuscript.pdf)
and [verification guide](../../../../../docs/VERIFY.md) give the integrated
proofs and replay paths. A subdirectory's profile count describes that
component's input or output, not the total current domain. No timeout or
surviving necessary-condition system decides categorification.

The [source-bound evidence package](../../../../../evidence/rigidity_20261017/rank6/README.md)
provides exact indicator, Fourier mass and profile-allocation checks. From the
repository root, run `python3 evidence/rigidity_20261017/rank6/run_checks.py --repo .`.
These checks do not construct compatible categorical structures.
