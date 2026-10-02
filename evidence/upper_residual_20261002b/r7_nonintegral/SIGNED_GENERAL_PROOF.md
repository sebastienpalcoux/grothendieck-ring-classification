# Four complete signed sphericalization exclusions

The following rings admit no fusion-category categorification over the complex
numbers, without a pivotality hypothesis:

| Census identifier | Complete normalized oriented signed tables |
| --- | ---: |
| R7_3_1036 | 8 |
| R7_3_1044 | 24 |
| R7_4_2510 | 4 |
| R7_4_2706 | 48 |

The proof uses sphericalization and formal-codegree divisibility, followed by
finite exact enumeration of their necessary consequences. It does not construct
induction matrices or modular data. All source tensors are reread from the
pinned complete census by `case_source.py`; the full proof trees are the four
`R7_*_general.json` files.

## Necessary signed tables

For a hypothetical fusion category C, let C~ be its canonical sphericalization.
We use the standard construction recalled in Ostrik, *Pivotal fusion categories
of rank 3*, [arXiv:1309.4822](https://arxiv.org/abs/1309.4822), Section 5.1.
Choose dual-compatible lifts X_i^+ of the simples, with the unit lift fixed. The
other lift is X_i^- = epsilon tensor X_i^+, where epsilon has dimension -1 and
is central of order two. In the quotient by epsilon = -1, write the product
coefficients as T_ij^k. If the two lift multiplicities are a and b, then
N_ij^k=a+b and T_ij^k=a-b. Consequently

    |T_ij^k| <= N_ij^k,   T_ij^k = N_ij^k modulo 2.

For each self-dual simple, the two lifts have opposite second indicators: the
definition of the indicator operator contains the inverse pivotal structure
map once, so replacing that map by its negative negates its trace. Choose the
lift of indicator +1. A simple of indicator -1 has even multiplicity in Y*Y,
by the pivotal Fuchs--Runkel--Schweigert parity theorem, in the form of
Liu--Palcoux--Ren--Vercleyen, *Triangular prism equations and categorification*,
[arXiv:2203.06522v5](https://arxiv.org/abs/2203.06522), Theorem 3.9. Thus b is
even in every square channel for a self-dual output, and

    T_(j,j*)^i = N_(j,j*)^i modulo 4.

This normalization chooses lifts in C~. It imposes no pivotal structure on C.
The inherited rank-six manuscript explains the same normalization in
`supplements/rank6/research/exclusions/m9_completion/case8785/general_proof_8785.tex`.

The quotient retains the unit, duality and ordered associativity. Its trace
coefficients t_abc=T_ab^(c*) are identified only by cyclic rotation and dual
reflection:

    (a,b,c) -> (b,c,a),   (a,b,c) -> (c*,b*,a*).

In particular, the enumeration does not impose commutativity on a hypothetical
signed quotient. All signed tables returned for these four inputs happen to be
commutative; this is checked for every table before using character arithmetic.

## Dimension-character obstruction

The spherical dimension character of C~ factors through T. Let its values be
d_i. Every d_i is nonzero and d_(i*)=d_i. Put delta=sum_i d_i*d_(i*).
Then dim(C~)=2 delta. The two epsilon eigenspaces give the algebras R and T;
their formal codegrees are doubled when regarded as characters of K_0(C~).
Ostrik's Theorem 2.13 and Corollary 2.14 therefore imply

    delta / f is an algebraic integer

for every formal codegree f of either R or T. The factors of the Casimir
characteristic polynomial compute these codegrees exactly for the commutative
signed tables here.

The elementary norm consequence checked in each certificate is as follows.
For nonzero algebraic integers u,v, set e_u=[Q(u):Q] and
n_u=|N_(Q(u)/Q)(u)|, and similarly for v. If u/v is integral, then for every
prime p,

    v_p(n_u) * e_v >= v_p(n_v) * e_u.

Indeed, take a number field L containing u and v. The p-adic valuation of
|N_(L/Q)(u/v)| is nonnegative; the tower formula gives the displayed inequality
after dividing by [L:Q]. In this application u=delta and v=f. The strict reverse
inequality is recorded by a codegree polynomial and a prime, and recomputed
from their exact constant terms and degrees. Every algebraic conjugate in an
irreducible character component has the same norm witness.

For every enumerated signed table, the checker constructs a separating
element, factors its characteristic polynomial over Q, and reconstructs the
values of every simple in every irreducible character component. Every
component fails at least one of: a zero simple dimension; unequal dual
dimensions; the preceding norm inequality. No positive-dimension assumption,
pseudo-unitary inequality or unverified modular-data filter is used.

## Complete finite exhaustion

`oriented_signed.problem` constructs one integer variable for each nonzero
cyclic/dual-reflection orbit. Its domain contains every bounded parity-compatible
coefficient satisfying the square-channel congruences above. It substitutes
these variables into all ordered associativity equations. The generated C++
search prunes an equation only once all its variables are assigned. A checked
absolute bound below 2^62 ensures that its integer arithmetic cannot overflow.
Every complete solution is emitted. Nonzero exits and timeouts raise errors.

`verify_nonintegral_results.py` recompiles and reruns this search, compares its
complete list with the certificate, validates every resulting signed tensor,
and reconstructs every character and obstruction. Removing one table or
changing a norm witness is rejected. The same checker succeeds with Python
optimization enabled; no classification check depends on `assert`.

Since an actual categorification necessarily yields one of these signed
tables and a surviving spherical dimension character, the exhaustive absence
of such a character proves the four general exclusions.

## Four separately scoped pivotal obstructions

`pivotal_certificates.json` covers R7_4_1212, R7_4_1213, R7_4_1417 and
R7_4_1420. A pivotal dimension function is an ordinary ring character with
nonzero simple values. Its global dimension is sum_i d_i*d_(i*), and formal
codegrees divide that global dimension by Ostrik's Corollary 2.14. All ordinary
character components fail a zero-dimension or norm test. Dual equality is not
imposed in these four pivotal tests.

Therefore these four rings have no pivotal categorification and, in particular,
no spherical, pseudo-unitary or unitary categorification. Their general complex
categorification status remains unresolved. The checker rejects any attempt to
promote these scoped records to general exclusions.
