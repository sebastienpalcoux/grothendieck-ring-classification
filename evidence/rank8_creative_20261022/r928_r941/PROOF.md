# Quartic center refinements and forced fusion products

These calculations apply genuinely new consequences of the saturated dimension
block to the complete surviving center domains. They provide exact rational
feasibility certificates, **not new categorifications or exclusions**. The
independent E21 construction of R982 is in `../r982`; its categorical existence
bridge is recorded in `E21_CATEGORICAL_BRIDGE.md`.

## Domains and inherited hypotheses

The source rings have
\[
 D=144+96\sqrt2+80\sqrt3+56\sqrt6.
\]
The existing spherical/Galois reduction allows their hypothetical centers to be
tested in the positive dimension embedding. The complete induction, character,
Gram, cubic, charge, indicator and linked rotation domains are taken from the
frozen `rank8_frontier_20261021` and `rank8_next_20261021` evidence. Specifically,
we retain all ten R928 pattern indices
\[
40,44,49,58,186,191,196,243,245,248
\]
and all fourteen R941 charge allocation indices
\[
8,19,21,31,34,43,45,56,60,72,73,77,79,85.
\]
The R982 phase system is the entire surviving frame2/indicator4 system; frame3
is its identical counterpart. No chosen list of small root orders replaces
these domains.

## Saturated masks

For a center simple of dimension \(d=a+b\sqrt2+c\sqrt3+e\sqrt6\), put
\[
 L_{12}=3c-a-b,\qquad L_{24}=6e-a-2b.
\]
The conductor-support theorem and its signed equality-space refinement are
proved in `../unified/SATURATED_CONDUCTOR.md` and
`../unified/COMPOSITE_SIGNED_SUPPORT.md`. They imply that a nonzero \(L_f\)
forces the twist to have order dividing \(f\), and give exact spectral weights
of the two endpoint representations. Their norms give
\[
 \sum_{\theta_Z=\zeta_f^k}L_f(d_Z)^2
 =4f\bigl(t_f w^-_{f,k}+(1-t_f)w^+_{f,k}\bigr),
 \qquad 0\leq t_f\leq1.
\]
For a conjugate pair of exponents, \(k\) and \(-k\), the sum of the two
endpoint weights agrees. Therefore the conjugate-fibre capacities contain no
unknown mixture parameter. In particular, the capacities at twists ±1 are4
for f=12, and at twists ±1,±i are4 for f=24. The original dimension-block
restriction on additional twist-one objects is retained as a separate condition.

`dimension_mask.py` applies these restrictions to every column of both complete
noncommutative domains. A twist-one high column can occur only when both linear
forms vanish; among the forty paired unknown types, only12 and23 have this
property. For all other types the conductor bounds make the permitted trace
atoms finite. Conjugate fibres are recovered exactly from those atoms, with an
explicit uniqueness check. `r982_mask.py` applies the same argument to each
duality orbit of its complete sparse phase system, counting the orbit size.

Every system has a nonnegative rational solution, checked by exact arithmetic.
Thus the new necessary restrictions exclude no further pattern. The R982 result
is also consistent with its independent E21 realization.

## Oriented complex semion cone for R928

The earlier R928 cone used the real field \(K=\mathbb Q(\sqrt2,\sqrt3)\).
The refinement `complex_semion.py` works in
\(L=K(i)=\mathbb Q(\zeta_{24})\), preserving the orientation of each semion
pair. Choose the central semion twist to be i, which is harmless after complex
conjugation. A positive-charge object of twist \(\theta\) and its negative-charge
translate have twists \(\theta,i\theta\). Their linked moments are consequently
\((1+i^k)\theta^k\), k=1,...,6.

The already established categorical Cauchy condition permits only the primes2
and3 in twist orders. For six linked moments, relative traces to L are exhausted
by the roots of order dividing \(2^5 3^2=288\), together with the simultaneous
zero trace tail. Indeed a larger 2-adic depth cannot be reduced to the conductor
depth3 by any k≤6, and a larger 3-adic depth cannot be reduced to depth1. The
relative trace then vanishes at all six powers. This is an all-order trace
argument, not an upper bound288 on the actual categorical exponent.

The script independently constructs \(\mathbb Q[x]/\Phi_{288}(x)\), averages
over all units congruent to1 mod24, and checks all eight coordinates of every
trace. Its real projections agree with the former complete paired domain.
The conductor masks replace a supported atom by its unique actual root in L.
The five known semion translates are fixed, rather than relaxed as unknowns.

In addition to all the previous real equations, the system imposes imaginary
STS for every pair of distinguished induction objects, both components of STS
between the central semion and each distinguished object, and every individual
spectral-fibre equation above. The two independent mixture parameters have
nonnegative complements, enforcing their interval bounds.

Here is the normalization in the additional central row. If a source irreducible
character E has degree \(n_E\), formal codegree \(f_E\), and central charge
\(m_E\), its distinguished object has dimension \(D/f_E\) and S-row scale
\(\beta_E=D/(f_E n_E)\). Dividing the unnormalized STS identity by this scale
gives
\[
 \sum_Z m_Z\theta_Z d_Z\,\chi_E(FZ)
 =-iD\,m_E n_E=-iD\,\chi_E(g).
\]
The source character equality \(\chi_E(g)=m_E n_E\) is checked explicitly,
including the degree-two character. The right side has one factor n_E.

All ten complete R928 patterns still have exact nonnegative rational witnesses.
This checks the specified distinguished and central rows, not all unknown rows
of a modular S-matrix. It also leaves the multiplicities of trace atoms rational;
integer counts, full modular relations, complete center fusion, and associators
are not supplied by these witnesses.

## A new forced-product test for R941

The frozen charged pair-product calculation uniquely determines the coordinates
of all words of degree at most two in the distinguished self-dual objects
\(A_1,...,A_4\) and the central involution G. There are30 listed words:
\(1,G,A_i,GA_i,A_iA_j,GA_iA_j\), with i≤j in the last two families.
Identical physical coordinate rows are kept with their multiplicity weights.

For a word w, its character value at a center simple Z is the product of the
known eigenvalues \(S_{A_i,Z}/d_Z\) and the charge of G. The center Plancherel
measure is \(d_Z^2/D^2\). Thus spectral moments compute all word inner products.
The script checks every one of the900 entries of the degree-two Gram matrix
against the physical coordinates, separately in every allocation.

The following elementary principle is the extra criterion. Let B be an
independent family of words with known physical coordinates and positive Gram
matrix H. For an additional word u, set \(v_j=\langle B_j,u\rangle\). Then
\[
 r=\langle u,u\rangle-v^tH^{-1}v\geq0.
\]
If r=0, u equals \(\sum_j(H^{-1}v)_jB_j\). Its coordinates in the simple basis
are therefore forced and must be nonnegative integers. This conclusion requires
no conjecture about closure or unknown fusion products. It is the orthogonal
projection identity in the positive based-ring inner product.

In each of the fourteen allocations the degree-two span has dimension15.
For its15 chosen basis words, multiplication by each of \(A_1,...,A_4,G\)
gives75 tests. Exactly55 have zero residual and their forced coordinates are
nonnegative integers. The other20 have positive residual. Thus this test gives
neither a contradiction nor a closed generated algebra. In particular, the
conditional packet-multiplication branch in the script is never used to claim
a complete fusion ring.

## Exact replay and scope

From the repository root run

```sh
python3 evidence/rank8_creative_20261022/r928_r941/verify.py
python3 -O evidence/rank8_creative_20261022/r928_r941/verify.py
```

Both commands are read-only. They bind the evidence and direct source inputs,
rebuild every refined matrix, verify all saved rational witnesses, and recompute
the physical/spectral Gram and projection identities. The matrix and right-side
hashes additionally bind the effective arithmetic imported from earlier stages.
No floating-point feasibility decision is accepted without its exact witness.
These finite calculations exhaust the indicated domains of necessary conditions;
they do not exhaust categorification or justify a claim of true exoticity.
