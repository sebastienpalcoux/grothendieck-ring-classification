# Independent audit of sphericality and Galois pseudo-unitarity

Auditor: `rank6_center`, 2026-10-16. Status: **PASS**.

I read `HI6_PAIR_GALOIS_PU.md` and the complete standard-library verifier.
The optimized independent replay passed for both R8_2_630 and R8_2_671;
its full receipt is `hi6_pair_galois_pu_rank6_independent_optimized.json`.
This result by itself makes no categorification or nonexistence decision.

The source tensors are self-dual. In the sphericalization, the two lifts
of each simple have opposite nonzero dimensions and opposite second
indicators. Choosing indicator +1 therefore gives a self-dual lift of
each simple. Frobenius reciprocity makes the resulting signed quotient
fully symmetric. Its coefficients obey the usual absolute-value and
parity bounds. The odd-channel parity theorem says that the number of
negative lifts in a square of a chosen lift is even, yielding
N_jj^i-T_jj^i divisible by four. This explains every domain used in the
verifier, including the ternary all-distinct multiplicity-two channel
for R671. It does not impose a positive pivotal structure in advance.

The program uses one variable for each unordered triple, with its
coefficient magnitude recorded separately. Boolean products are
correctly represented by XOR of masks. It generates every associativity
equation with nonunit inputs and output; those involving the unit are
identities by the fixed unit rule. Its two-valued depth-first branching
is exhaustive and rejects only fully evaluated nonzero equations.
The sole solution is the original nonnegative tensor in each ring.
Consequently the selected lifts close under tensor product and give a
spherical section. No associator is being inferred from a merely
associative candidate tensor: the lifts are actual objects of the
sphericalization of the hypothetical category throughout.

The exact arithmetic uses the basis (1,sqrt3,sqrt10,sqrt30), and its
multiplication rule is correct. All eight displayed distinct characters
are checked on every source product, so semisimplicity and commutativity
make the table complete. All six characters outside the FP conjugate
pair vanish on at least one simple. A spherical dimension character
cannot do so. It must therefore be one of the two FP conjugates; an
automorphism of a number field of definition takes it to the positive
FP character. This establishes Galois pseudo-unitarity, not unitarity.

The archive hash and prescribed lexicographic indexing bind the proof
to the original two census tensors. The argument does not identify
either category or center with the known HI(C6) category.
