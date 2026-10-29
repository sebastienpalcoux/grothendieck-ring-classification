# R928 pattern 40: a congruence and signed-Galois obstruction

29 October 2026. **Pattern 40 is excluded, conditional on the separately
derived phase and invariant-block data stated below. Pattern 186 and the
fusion ring R8_3_928 remain unresolved.**

This argument uses all irreducibles of SL2(Z/24), including both central
signs. It does not assume that all simple objects, or all objects in the
complement, are self-dual.

## Categorical inputs and their scope

The R928 analysis supplies a positive modular factor of rank 23 for pattern 40.
Use its normalized S matrix s and t=theta/gamma, where gamma=zeta_24 and
the multiplicative central charge is gamma^3=zeta_8. The supplied phase
reduction gives ord(t)=96, and the following two invariant summands:

1. A six-dimensional summand containing the four H objects, the canonical
   bosonic vector f of twist 1, and the pair-difference vector of twist
   zeta_8^7. Its existence is a linear consequence of the previously forced
   low S rows and modular relations; no identification with a Weil
   representation is needed for this proof.
2. A two-dimensional summand spanned by e=(B0+B1+B2+B3)/2 and W, with
   s=2^(-1/2)[[1,1],[1,-1]] and theta=diag(1,i).

After removing these summands the remaining representation has dimension 15
and the following t spectrum, with exponents modulo 24:

    3:2, 9:2, 11:1, 12:4, 15:2, 17:1, 20:1, 23:2.

In the full rank-23 representation, the entire t=-1 eigenspace consists of
four simple-object coordinates A1,...,A4. Each has theta=zeta_24^13 and

    s_(0,Ai) = 1/(4 sqrt(3)).

These statements are categorical necessities derived in the R928 phase/block
work, not consequences of the character-table computation below. They are
the precise dependencies to audit before applying this branch exclusion.
The source's previously established sphericalization/Galois reduction is
also needed when interpreting a positive-center contradiction as an
obstruction for a general complex categorification.

## Why the complementary representation has level dividing 24

Dong–Lin–Ng, *Congruence property in conformal field theory*,
arXiv:1201.6644v7, Theorem II(i), gives a representation of SL2(Z/96)
for the full modular data. It is not enough merely to observe that the
complementary t has order 24. Here the required stronger conclusion follows
from a short group argument.

By the Chinese remainder theorem, the reduction kernel from level 96 to
level 24 is the kernel K of SL2(Z/32) -> SL2(Z/8). Its matrices are

    I+8M, with M in Mat2(Z/4), tr(M)=0 mod4.

Because 8^2=0 modulo 32, multiplication in K is addition of M. Thus
K is the additive group sl2(Z/4), of order 64. In SL2(Z/32), T^24 cubed
is I+8E12. Conjugating by S gives -E21, and conjugating by
L=[[1,0],[1,1]] gives -H+E12-E21, where H=diag(1,-1). These three
directions generate sl2(Z/4). Hence K is the normal closure of T^24.
The action of T^24 on the complement is trivial, so the complement factors
through SL2(Z/24).

## The complete finite character calculation

The frozen project tables list all 30 irreducibles of SL2(Z/8) and all
7 irreducibles of SL2(Z/3). Their 210 tensor products are all the
irreducibles of SL2(Z/24). The validation rechecks:

* all concrete group elements, conjugacy orbits, and class multiplication;
* every class-algebra character equation and every character inner product;
* degree-square sums 384 and 24, and all T multiplicities and central signs.

The T spectrum above has exactly four nonnegative irreducible
decompositions. In the frozen table indexing, each is the sum of

    V_(8,2) + 3 V_(1,2)

and one choice from each of

    V_(15,5)  or  V_(15,1)+V_(15,2),
    V_(5,5)   or  V_(5,1)+V_(5,2).

The degrees are respectively 2, 1, 6, 3+3, 4, and 2+2. The split
3+3 and 2+2 choices have negative central sign; they were retained.
V_(1,2) is the one-dimensional sign representation

    s=-1, t=-1.

There is also a direct linear proof of this forced multiplicity, found in
the independent audit. Let n_j denote a t-eigenvalue multiplicity. Exactly
12 of the 210 irreducibles have their T spectra contained in the prescribed
spectrum. On these 12 columns the following identities hold:

    2 n_20 - n_23 - n_11 + n_17 = 2(m_(1,1)+m_(1,5)),
    2 n_12 - n_3  - n_15 + n_9  = 2(m_(1,2)+m_(1,5)).

Their values on the target are 0 and 6. Nonnegative multiplicities imply
m_(1,1)=m_(1,5)=0, and then m_(1,2)=3. Both identities are checked
exactly against every eligible irreducible, with no central-sign restriction.

Thus every possible complement contains a three-dimensional sign
isotypic subspace U. The independent 142-node decomposition search is a
cross-check, not needed for the linear proof. Neither step involves
associator equations or reconstruction of new character tables.

## The contradiction

Let sigma_5 act on Q(zeta_96) by zeta_96 -> zeta_96^5. By
Dong–Lin–Ng Theorem II(iii),(iv),

    G_5 = sigma_5(s) s^(-1) = t^5 s t^77 s t^5 s^(-1)

is a signed permutation matrix. Since 5*77=1 modulo96, this is the
specified Galois matrix. On every sign representation the word evaluates
to +1. Therefore G_5 has at least three fixed vectors inside the t=-1
eigenspace.

On the other hand, Galois symmetry preserves this eigenspace, because
sigma_5^2(-1)=-1. It consists of exactly the four Ai coordinates.
The first column of s on those coordinates is constant
1/(4 sqrt(3)), and sigma_5(sqrt(3))=-sqrt(3). The signed permutation
formula therefore forces G_5=-P on that four-dimensional space for
some permutation matrix P.

The dimension of the +1 eigenspace of -P is the number of even cycles
of P. A permutation of four elements has at most two even cycles.
Thus G_5 has at most two fixed vectors on this space, contradicting
the three forced by U. Pattern 40 is impossible.

This proof requires neither full S reconstruction nor integrality of any
uncomputed Verlinde coefficients. It excludes this center pattern only.

More generally, suppose an m-object twist fiber is preserved by a Galois
matrix and all its signs are negative. Then that matrix has at most
floor(m/2) fixed vectors on the fiber. Any independently forced invariant
representation contributing more fixed vectors in that fiber excludes the
candidate modular data. The present proof applies this general obstruction
with m=4 and three forced sign characters.

## Replay and provenance

Run, using Python 3 and SymPy:

    python verify_level24_inputs.py
    python verify_r928_pattern40.py

The first command takes approximately four seconds and verifies the
previously stored complete tables. The second takes less than one second,
re-enumerates all spectral decompositions, verifies the 64-element
congruence-kernel calculation, the Galois word, and the permutation bound.
Both use explicit exceptions; no assertion is needed for correctness.

Original inputs:

* sl2_8.json: repository path
  supplements/rank6/research/frontier/new_research/r155_modular/sl2_8.json,
  SHA256 611f5fde5aabbd4d24d2aee3d0ce23b2e58d500d8d363f89ef42bdba9780e92e.
* sl2_3.json: repository path
  evidence/frontier/replay/prior/evidence/theoretical_20261016/rank6/r1660_modular_witness/inputs/sl2_3.json,
  SHA256 818c8f1aa9f9368c57e30b03e4a4e8a62dacc98abbd0b15a62fabbc734e5f1a6.
* finite_spectra48.py: existing project character-table verification
  routines from supplements/rank6/research/round5/m8_modrep/finite_spectra48.py.

The verification wrapper supplies the elementary require/evaluate helpers
locally, so no enclosing historical project checkout is required.

Primary categorical reference:
https://arxiv.org/pdf/1201.6644 (Theorem II, p.3).
