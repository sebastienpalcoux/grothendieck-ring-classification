# Independent audit: signed general exclusions and the D12 model

## Verdict

APPROVED for the four general exclusions R7_3_1036, R7_3_1044,
R7_4_2510 and R7_4_2706, for the separately scoped four pivotal
exclusions, and for the unitary modular model R7_2_240.

This audit reread the proof, the original oriented enumeration engine,
the character and exact norm checker, the reconstructed certificates,
and the model constructor. It also checked the cited primary sources
directly. Fresh normal and optimized replay receipts accompany this file.

## General versus pivotal scope

Ostrik arXiv:1309.4822 Section5.1 explicitly applies sphericalization to
an arbitrary fusion category, supplies two lifts of every simple, and
states that both lifts of a self-dual simple are self-dual. The minus
unit has dimension-1 and order2. Thus non-self-dual lifts can be chosen
in dual pairs; the self-dual lifts can be chosen to have positive second
indicator. This does not require a pivotal structure on the original
category. Negating its pivotal structure map changes that indicator's
sign. Liu--Palcoux--Ren--Vercleyen arXiv:2203.06522 Theorem3.9 applies
to a pivotal category and states precisely the odd-multiplicity parity
condition for a self-dual simple in X*X. It is applied only in the
sphericalization, where its pivotal hypothesis is satisfied. The
resulting square-channel congruence modulo4 is therefore valid generally.

The engine enumerates cyclic trace and dual-reflection orbits; it does
not identify arbitrary transpositions of inputs. It imposes all ordered
associativity equations using the row-matrix composition convention,
checks an absolute integer bound before compiling, and prunes only
fully assigned equations. Its complete output is compared with the
certificate. Every output table in these four cases is commutative;
the character constructor checks this, rather than assuming the
sphericalization of a commutative ring must remain commutative.

Ostrik Theorem2.13 applies to the sphericalized category. Its epsilon
eigenspaces give the original and signed quotient algebras, with
doubled formal codegrees. Its global dimension is twice the quotient's
dimension character value. Hence the tested quotient delta/f is integral.
The norm inequality is a necessary consequence of integrality in a
common number field; multiplying minimal degrees is exactly the tower
norm formula used by exact.check_norm. No positivity, pseudo-unitary
bound, or modular-data assumption occurs in the four proof trees.
All their character branches use only zero, duality or norm witnesses.

The four separate pivotal certificates intentionally omit spherical
dual-dimension equality. Their zero/norm witnesses are valid for a
pivotal dimension character, and the records retain general_status
unresolved. The verifier expressly rejects scope promotion.

## D12 existence and transcription

Morrison--Peters--Snyder arXiv:1003.0022 Theorem2.2 supplies a unitary
D2n subfactor planar algebra; Proposition2.4 identifies its even part
with the modularization of the even quantum sl2 category and proves
that it is modular. Thus existence is stronger than a formal fusion
table identification. Their arXiv:0808.0764 Theorem4.14 gives the
published fusion rules, including the even-n exceptional products.

For n=6, the products are P^2=Q+f2+f6, Q^2=P+f2+f6 and
PQ=f0+f4+f8; P and Q are dual. The published even-object action
agrees with the constructor's reversed index range. Folding the bulk
SU(2)_20 products correctly identifies f_(20-a) with f_a and
f10 with P+Q. The supplied model-to-census map is a bijection and
all343 coefficients,2401 elementary associativity relations, and
exceptional dualities are freshly checked.

## Limitations

This certifies the stated finite inputs and scopes. It does not claim
that all fusion categories are pivotal, or that the remaining census
has been classified. Enumeration failure or timeout is an exception,
never an exclusion. The source-pinned engine receipts and tampering
controls are part of the evidence.
