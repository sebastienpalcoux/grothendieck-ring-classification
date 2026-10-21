# Pure invertible restrictions with trivial forgetful kernel

This adapter applies only to a commutative source fusion ring. Its
distinguished summands A_E in I(1) have multiplicity one. If a central
simple Z has F(Z)=n·1, adjunction gives multiplicity n of Z in I(1),
hence n=1. Thus, when the distinguished FP dimensions beta_E contain
no value1 except the central unit, the forgetful kernel is Vec.
The code checks commutativity and this dimension-one condition explicitly.

Under that hypothesis, if F(Z)=n·g for an invertible source simple g,
then F(ZZ*)=n²·1. Every simple summand of ZZ* belongs to the forgetful
kernel, so ZZ*=n²·1. Since Z is simple, the unit has multiplicity one
in ZZ*, and n=1. If Z and W both lift g, then ZW* forgets to1, hence
ZW*=1 and Z=W. Consequently a pure k·g high column with k>1 has
count zero, and the unique pure g high column has count at most one.
Complete duality orbits preserve this convention.

For R65 the saved exact integer witness respects these strengthened
bounds. R3472 has no source invertible other than1, so its high
restrictions (whose unit coefficient is zero) contain no such column.
The actual Fib tensor Vec(C4) positive control has a nontrivial Rep(C4)
forgetful kernel; the adapter correctly declines to impose the rule.
No unrestricted noncommutative version is asserted by this implementation.
