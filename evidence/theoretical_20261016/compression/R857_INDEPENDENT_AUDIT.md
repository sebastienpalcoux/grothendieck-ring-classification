# Independent audit: the general exclusion of R8_2_857

Date: 2026-10-16. Audited by the rank-eight multiplicity-one research agent,
independently of the author of `R857_GENERAL_PROOF.md`.

**Verdict: PASS.** The argument excludes every complex fusion category with
this Grothendieck ring. It does not assume pivotality, sphericality,
pseudo-unitarity, braiding, or a classification of trivalent categories.
No unresolved categorical step was found.

The source tensor SHA-256 is
`cfd21669455748b2e8b1d9628c1e1cde5d22f442edbac56ed946e9b8eb4333dc`.
The audited ordering is `(0,1,7,2,5,4,3,6)`.
The source-bound verifier `verify_R857_general.py` was also read and rerun;
it returned PASS. The argument below is a mathematical audit, not a claim
that finite arithmetic alone proves categorical nonexistence.

## 1. Compression and the field constraint

The full induced-unit inequality in `full_I1_compression.tex` correctly
retains all the distinct simple coordinates `A_E` in the twist-one
projection of `s w_chi`. Their coordinates are the Fourier transforms of
`1/f_E`. Multiplicity in the induced object is not multiplicity of a
coordinate, so no factor `dim(E)` should be inserted.

The local operator estimate used here was checked directly against
[Schopieray, arXiv:2609.35287v1](https://arxiv.org/html/2609.35287v1),
Lemma 4.1 and the proof of Theorem 5.1. It is a bound on the entire projected
vector and therefore permits this stronger retained-coordinate conclusion.
The proof uses the unitary modular representation of the center, which
does not require the fusion category itself to be unitary. No assertion
about a dimensional grading is needed.

For `zeta = exp(2 pi i/32)` and `L = Q(zeta + zeta^-1)`, the identity

    1/D = (2 - zeta - zeta^-1)/16

shows `Q(D)=L`, not merely `D in L`. In particular the formal codegrees
`2 sigma(D)` in the positive sign sector force `L` into the spherical
dimension field `K` of a sphericalization. The standard induced-unit
formula gives all formal codegrees in `K`.

Take a primitive even Dirichlet character `chi` modulo 32. The sum of the
constant term in `1/D` vanishes. The two remaining terms, when summed over
representatives of the units modulo sign, give exactly one full primitive
Gauss sum, rather than twice or half that sum. Hence

    ghat(chi) = -tau(chi)/16,
    |ghat(chi)|^2 = 32/16^2 = 1/8.

The character inflated to `Gal(K/Q)` still has conductor 32: its kernel
fixes the same primitive-character subfield of `L`. Each fiber over
`Gal(L/Q)` has `e=[K:L]` elements. The eight translated Fourier sums have
equal absolute values. Thus their total squared norm is `e^2` for the
original ring, against the upper bound `e/4`, excluding spherical
categorifications. In the sphericalization each formal codegree is
doubled, so that total becomes `e^2/4`. The same upper bound then forces
`e=1` and `[K:Q]=8`.

This computation uses eight distinct irreducible characters. Distinctness
follows already from the eight distinct conjugates of
`d_1 = 1 + zeta + zeta^-1`; the ring has rank eight. Repeated numerical
codegrees, if present in another application, would not justify dropping
coordinates, but no such ambiguity affects this case.

## 2. The sign normalization is justified

[Ostrik, arXiv:1309.4822](https://arxiv.org/pdf/1309.4822), Section 5.1,
supplies the sphericalization, its sign object, the signed coefficient
bounds, and the tensor-section criterion. Both lifts of each self-dual
simple here are self-dual. Their nonzero spherical dimensions have
opposite signs, while duality preserves spherical dimension.

Changing the sign of the pivotal isomorphism of a self-dual lift changes
its second Frobenius--Schur indicator by a minus sign. Consequently one
can choose indicator `+1` for every initial lift, including the unit.

The necessary odd-square-channel theorem is proved, not conjectural:
[Liu--Palcoux--Ren--Vercleyen, arXiv:2203.06522v5](https://arxiv.org/pdf/2203.06522),
Theorem 3.9. In a pivotal fusion category, an odd multiplicity of a
self-dual simple `Y` in `X* tensor X` forces `nu_2(Y)=+1`. Its proof uses
the nondegenerate bilinear form of Proposition 3.10. The conjecture
mentioned nearby concerns a stronger even-multiplicity assertion and is
not used here.

For the opposite lift of `X_j`, whose indicator is `-1`, its multiplicity
`m_-` in a square must therefore be even. Thus

    T_ii^j = N_ii^j - 2 m_- = N_ii^j (mod 4).

This forces `T_jj^1=1` for `j=1,...,6`. Self-duality and Frobenius
reciprocity identify these with the six interior diagonal entries
`T_1j^j`. There is no circular assumption of positivity of the eventual
signed table.

The later change of signs of basis elements may change their indicators,
but that causes no problem. With the sign of `X_1` fixed, it leaves every
entry `T_1j^j` unchanged. Along the path, successive choices of signs make
every off-diagonal entry positive. The unit and `X_1` stay fixed because
their first edge already has coefficient one.

## 3. All possible endpoints are excluded

After normalization the only unknown entry of the generator matrix is
the last diagonal `t in {-2,0,2}`. The source zeros and signed coefficient
bounds rule out every other possible entry. In each case the first seven
columns give the same polynomial recurrence for the basis elements.

* `t=-2`: the bottom-right entry of `J_t^2-J_t-I` equals
  `(1+4)-(-2)-1=6`; the source bound is 2. This is an immediate
  contradiction independent of any dimension choice.
* `t=0`: the characteristic polynomial factors into degrees `1,1,2,4` as
  displayed in the proof. Every possible value of `dim(X_1)` has degree at
  most four. The polynomial recurrence makes every other simple dimension
  an integer polynomial in this value, including after the sign change.
  Thus it generates `K`, contradicting the previously forced degree eight.
* `t=2`: the recurrence determines every multiplication matrix from `J_t`,
  so the entire signed tensor equals the source tensor. Each signed
  difference equals the unsigned sum of the two lift multiplicities,
  forcing the opposite-lift multiplicity to vanish. The selected lifts
  form a tensor subcategory. The forgetful functor restricts to an
  equivalence with the original category, transferring a spherical
  structure and contradicting the spherical exclusion.

There is no surviving branch, and the passage from a hypothetical
arbitrary categorification to its sphericalization closes the general
nonpivotal case.

## Scope of the audit

The proof is theoretical. The exact verifier checks the fixed source
tensor, cyclotomic dimension identities, Fourier norms, polynomial
recurrence, and endpoint identities. It does not enumerate associators
or invoke existence of any modular data. The optional observation about
the remaining sign-sector codegrees at equality is unnecessary and was
not used to establish the verdict.
