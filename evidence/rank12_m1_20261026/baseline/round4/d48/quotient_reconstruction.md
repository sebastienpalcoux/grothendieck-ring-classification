# Exhaustive reconstruction of the rank-twelve dimension-24 quotients

This check does not assume that the supplied rank-twelve census is
complete. It reconstructs every possible quotient based ring from the
actual dimension-48 source tensor and the simple-orbit formula.

Suppose C=D^C2, and its canonical boson b fixes exactly the two
2-dimensional and two4-dimensional source simples. Each of C's eight
invertibles belongs to a free b-pair, yielding four fixed invertibles
of D. Each b-fixed2-dimensional simple forgets to a free pair of
invertibles of D; each b-fixed4-dimensional simple forgets to a free
pair of2-dimensional simples. Thus D has eight invertibles and four
2-dimensional simples. The tensor action p fixes four invertibles,
interchanges the other four in two pairs, and acts on the four
noninvertibles as two transpositions.

Identifying X with bX in K0(C) gives exactly the invariant-orbit ring
K0(D)^p, whose basis consists of sums over p-orbits. Quotient products
are computed directly from all source coefficients. The four resulting
isomorphism types of invariant-orbit rings are frozen with every source
and central involution binding in quotient_reconstruction.json.

For each such ring, quotient_reconstruct.py does the following finite
exhaustion, using only the five elementary groups of order8.

1. Enumerate every involutive automorphism of the invertible group with
   exactly four fixed elements. Enumerate every identification of its
   invariant group-ring orbit sums with the pointed part of the given
   invariant-orbit ring. The identity and orbit dimensions are preserved.
2. Enumerate every group homomorphism G->S4 using images of an actual
   generating set and the complete group multiplication table. These
   supply every possible left action on the four noninvertibles.
   Right actions are the corresponding antihomomorphisms. Retain all
   commuting pairs compatible with p and every prescribed orbit product.
3. Enumerate all possible dual involutions on the four noninvertibles.
   Frobenius reciprocity fixes every coefficient with an invertible
   index. Check all such reciprocity, duality, and orbit equations.
4. The remaining coefficients have three noninvertible indices. Every
   coefficient is at most1: each occurs with a positive coefficient in
   an invariant-orbit product whose coefficient at a noninvertible orbit
   is at most1. Impose Frobenius reciprocity, duality, p-invariance, and
   every associativity equation with an invertible factor. The equalities
   leave at most THREE binary variables for each possible module/duality
   datum. Exhaust all of them, then check dimensions, every orbit product,
   and every associativity equation exactly.

The invariant-orbit rings are checked to be commutative; this permits
the same preliminary action filter on either side. The final checks
still impose every left and right product separately. No assertion
that the reconstructed full based ring is commutative is imposed.

The four runs retain336,16,336,16 labeled tables, respectively. After
based-ring isomorphism they give one table each: R351, R513, R351, R513.
Those identifiers are merely checked against frozen known tensors after
the exhaustion; they are not a source of candidate tables.

The verifier is portable with quotient_inputs.json and ring_utils.py.
It also checks all twenty full source tensors, exact integer dimensions,
trivial universal grading, every possible central order-two invertible,
and non-isomorphism with the four conditional group-theoretical models.
All checks remain active under python -O. Run:

    python -O quotient_reconstruct.py

The necessary categorical hypotheses for the two surviving quotient
rings are proved separately in ../audit_models/d24_c3_pointed_extension_lemma.md,
../audit_exclusions/R351_neutral_associator.md, and
../audit_exclusions/R513_GT_proof.md. The finite reconstruction supplies
the previously missing exhaustive source-to-quotient binding.
