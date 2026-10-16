# Independent audit of the R8_2_489 scope reduction

Status: **PASS for sphericality, Galois pseudo-unitarity, and existence of
the regular pointed C2 algebra**. This is not a classification decision.

I reviewed the proof and complete standard-library verifier and independently
ran the latter in optimized Python. The replay passes; its receipt is
`fib_r489_independent_O.json`. The source hash is
`23cae0639e4ce7e54428705a66098747319e26d5f29ad8dff05914a6d43caef1`.

The signed-quotient enumeration is exhaustive under the stated
positive-indicator normalization in canonical sphericalization. All
multiplicity-two channels have a repeated label, and their modulo-four
restriction removes the possible zero coefficient. Repeated channels of
multiplicity one are forced positive. The remaining sixteen Boolean signs
therefore cover every quotient. The checker derives all associativity
equations, reduces sign squares using the Boolean relations, and enumerates
both signs at every unforced node. The four outputs are each checked
against all tensor channels to be a coboundary. Because every coefficient
has full unsigned absolute value, changing lifts by that coboundary gives
an actual tensor-closed spherical section, not merely a dimension character.

The strengthened indicator argument is best stated inside that closed
section. Its simple indicators are the coboundary signs s_i, and only
s_g and s_(g tau) could be negative. The self-dual simples x and tau have
positive forms. The odd-power homogeneous-form lemma, applied to the
checked parity of x^3, forces s_(g tau)=+1. Applied next to (g tau)^3,
it forces s_g=+1. Dualization reverses identical component forms, so
this lemma does not require a braiding. Thus all simple indicators in
the obtained section are positive.

The dimension-character dichotomy is complete: g has dimension +/-1,
tau satisfies t^2=t+1, and x is determined by its stated quadratic
relation. The h=+1 branch consists of the four roots of the displayed
quartic, whose irreducibility is checked modulo three. They are one
Galois orbit containing the FP character. For h=-1, the categorical
global dimension is 4(t+2), while the h=+1 character with the same t
has formal codegree 2(t+2)(1+d^2). Central induction forces their ratio
2/(1+d^2) to be integral. The elimination polynomial is verified over
the integers; the rational reconstruction of d from d^2 proves its
degree is four, so its primitive leading coefficient five indeed rules
out algebraic integrality. The appropriate reference for the induction
step is Ostrik, *Pivotal fusion categories of rank 3*, Theorem 2.13;
the author was notified to correct the draft's paper title.

Galois conjugation to the positive dimension character produces a
pseudo-unitary category with the positive spherical structure. The
indicator of g remains +1. For a pointed C2 category that indicator
detects the nontrivial associator class, so 1+g is an actual connected
separable algebra. Existence transports back under Galois conjugation.
This supplies a module-category/Morita operation, but no central lift,
de-equivariantization, or Deligne factorization is inferred.

No gap was found in the finite coverage or the categorical scope.
