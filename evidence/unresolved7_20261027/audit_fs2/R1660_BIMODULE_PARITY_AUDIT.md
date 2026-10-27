# Independent audit: two R1660 module realizations fail Frobenius parity

Date: 27 October 2026.

**Accepted with precise scope:** the conditional module realizations
`III_mixed0` and `IV_mixed1` cannot occur over a pseudo-unitary
categorification of R6_8_1660. This does not exclude the ring, another
realization of the same dual based ring, the surviving IV mixed module,
or the retained rank-eight Morita candidate.

## Categorical step

Choose the symmetric separable Frobenius internal-end algebra A associated
with a simple module object and the positive module trace. The forgetful
functor U from A-bimodules to C is a pivotal Frobenius monoidal functor.
A direct primary source is Mulevicius, *Condensation inversion and Witt
equivalence via generalised orbifolds*, TAC 41 (2024), Example 4.18,
https://www.tac.mta.ca/tac/volumes/41/36/41-36abs.html .
The example explicitly assumes a symmetric separable Frobenius algebra
in a pivotal multifusion category and states the pivotal property.
Positive module traces and the compatible positive pivotal Morita
structure are provided by Schaumann, *Traces on Module Categories over
Fusion Categories*, arXiv:1206.5716. These are pseudo-unitary, not
C*-unitary, hypotheses.

A pivotal Frobenius functor preserves dual pairs and the transpose
operation on duality morphisms. Thus the image of a selfdual simple has
a nondegenerate form of one uniform transpose sign epsilon=+1 or -1.
For a selfdual source simple of indicator eta, its multiplicity space
has form sign epsilon*eta. Opposite signs require that multiplicity to
be even. An image containing an odd number of both a positive-indicator
simple and a negative-indicator simple is therefore impossible, regardless
of the unknown indicator epsilon of the original bimodule simple.

The relevant source indicators are `(1,1,1,1,-1,1)` in the order
`1,g,X,gX,sigma,T`. The negative sigma sign is the established positive
Ising sign; X and T signs are independently read from the exact order-two
indicator certificate, and gX has the same sign as X.

## Independent reconstruction of the restrictions

I rebuilt each source action N_i from its Ising-block parameters, without
importing the author's new checker. I then read the old frozen dual action
matrices Q_j and computed

    [U(Q_j):X_i] = (N_i Q_j)[0,0].

This is linking-category adjunction at the chosen module object m_0.
Because all source simples are selfdual, the formula also equals the
ordinary inner product of the zeroth columns of N_i and Q_j.

The decisive rows are:

| Module realization | Dual simple | Selfdual? | Underlying object |
|---|---:|---|---|
| III_mixed0 | 4 | yes | sigma + T |
| IV_mixed1 | 2 | yes | X + gX + sigma + T |

The two rows mix opposite-indicator source simples with odd multiplicity.
The first would need epsilon=-1 from sigma and epsilon=+1 from T; the
second has the same contradiction. There is no inference that U preserves
the numerical value of an indicator on arbitrary decomposable objects.

## Exact replay and controls

`verify_r1660_bimodule_parity.py` verifies all source module products
against the current 216-coefficient tensor, all archived dual action
products against their complete tensors, and every recorded duality by
matrix transpose. It checks the complete restriction columns, not only
the displayed entries, and binds the old action and indicator certificates
by SHA-256. It passes under normal and optimized Python; explicit exceptions
remain active. Each run takes approximately one second.

`IV_mixed0` has no parity violation. `III_same0`, the retained rank-eight
case, also passes: its odd-sigma rows belong to a nonselfdual pair, to
which the selfdual-form test does not apply. These controls prevent an
incorrect exclusion of all modules or of the ring.

See `r1660_bimodule_parity_receipt.json` for the full independent receipt.
