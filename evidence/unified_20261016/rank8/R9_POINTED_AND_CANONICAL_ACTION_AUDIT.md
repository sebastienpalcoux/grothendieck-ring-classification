# Independent audit: pointed Morita classes and the canonical-action warning for R9

The corresponding sections of
`work/unified/rank8_subcategories/R9_MORITA_FRONTIER.md` pass independent
categorical review. This audit is restricted to those sections; the
module enumeration and the full indicator induction argument have a
separate reviewer.

## Pointed dichotomy

The forced positive indicator of the C4 involution restricts the pointed
class k to 0 or 2 in H³(C4,C*). The pointed subcategory of the A-bimodule
dual is precisely the Morita dual of the source pointed category along
H=C2, because its four invertibles have pointed support and all other
simples have irrational dimension.

For k=0, simple H-bimodules in Vec_C4 are indexed by a coset q in C2
and a character chi in H-hat. Their product is componentwise, so the
group is V4. The nonsplit C4 extension survives as the associator

    omega((q,chi),(q',chi'),(q'',chi''))=(-1)^(chi*q'*q'').

Changing choices may give a cohomologous cocycle or exchange coordinates;
neither affects the conclusion. Its restriction to an involution (q,chi)
is (-1)^(chi*q), so exactly one nonidentity object has negative second
indicator. In particular, the dual associator must not be silently set
to zero despite the original pointed category being strict.

For k=2, the source pointed category has FS exponent 4*2=8. The same
holds for its Morita dual. Every pointed V4 category has exponent
dividing four: each cyclic subgroup has order at most two and each
restricted third-cohomology class has order at most two. Thus the dual
group is C4, and its class must again have order two, namely k=2.

## Canonical 2D2 action

The proposed action fixing M and negating the crossed-product unitary
lambda is exactly the dual action, not an unrelated gauge action.
Grossman, arXiv:1612.07185, **Lemma 4.3**, explicitly identifies the
standard C4 Haagerup--Izumi category P1 with the equivariantization of
Q1 by this action. Section 4.2, immediately after Lemma 4.6, explicitly
identifies its crossed extension as P3, the Morita dual of P1 along
1+alpha2. These statements independently settle the Takai-duality issue.

P1 has total second indicator 2+4d: its two self-dual invertibles have
positive indicator and all four noninvertibles are positive by the
odd-cube lemma. Therefore the crossed extension P3 has this same total.
Its pointed one-anomaly V4 contributes two, so all four noninvertibles
must have positive second indicator. It cannot yield R9, whose total
is 2+2d, along any Morita algebra.

The nontrivial scalar three-cocycle twist of the faithful C2 grading
negates the second indicators of all self-dual odd objects. There are
two odd noninvertibles and two odd nontrivial invertibles. Thus the
noninvertible signs become two positive and two negative, the pointed
signs become all negative, and the total is -2. This variant likewise
cannot yield R9.

No conclusion is made about other categorifications of the R477 ring,
or about the remaining R9 self-Morita branch. The scope is a necessary
reduction and rejection of these specific construction attempts.
