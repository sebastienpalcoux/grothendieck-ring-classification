# The pointed associator distinguishes R439 and R567

This is an additional necessary-structure theorem. Neither source is
excluded or constructed.

The independently replayed general Galois-pseudo-unitary reductions in
`../noncommutative_followup/additional_scope_gates.py` apply to every
complex categorification of both rings. Work in that pseudo-unitary
Galois conjugate with its canonical positive spherical structure. The
complete central-image and full-character-S calculation leaves exactly
one low induction frame for each source. On it, the complete height-six
joint-rotation test excludes seven of eight allowed indicator tuples,
with exact rational separating rays, and retains an exact primal witness
for the eighth. The required source-bound replays are
`additional_central_constraints.py` and `additional_joint_rotation.py`.

In source order1,...,7, the forced tuples are

    R439: (0,0, 1,1,1,1,1),
    R567: (0,0, 0,0,-1,-1,-1).

The three order-two invertibles of S3 are indices3,6,7 for R439 and
5,6,7 for R567. Thus all their indicators are+1 for R439 and-1 for
R567. The distinction concerns the canonical positive spherical
structure, not a freely changed pivotal sign.

Let omega be the pointed associator class in H3(S3,C*). Its restriction
to C3 is zero in both sources: either noninvertible is fixed by C3, so
the one-simple pointed module on that object supplies a2-cochain whose
coboundary is the restricted associator. This exact fixed-object
hypothesis is rechecked in `pointed_s3_scope.py`.

For a normalized pointed C2 category with positive spherical dimensions,
nu2(g)=omega(g,g,g). The two classes in H3(C2,C*) have values+1 and-1;
this follows directly from the scalar duality/pivotal evaluation for
g tensor g=1, or from Schauenburg, arXiv1502.02906, Definition2.2 and
Proposition4.1 with H=1 (the inverse convention has no effect on a sign).
Consequently omega restricts trivially to each C2 for
R439 and nontrivially for R567.

There is no missing component of H3(S3,C*): if both Sylow restrictions
vanish, corestriction after restriction yields multiplication by the
subgroup index; this works for arbitrary subgroups, as in Brown,
*Lectures on the Cohomology of Groups*, Section3.3, equation(3.12),
printed pp21--22, https://pi.math.cornell.edu/~kbrown/papers/cohomology_hangzhou.pdf.
Thus2 omega=0 from C3 and3 omega=0 from C2, forcing
omega=0. Hence the full pointed class is trivial for R439 and nontrivial
for R567. Galois conjugation acts on scalar cocycles by a field
automorphism, preserving zero and nonzero classes. In particular a
chosen trivializing cochain and the resulting subgroup algebra can be
transported back by the inverse automorphism.

It follows that **every** complex categorification of R439 admits the
full subgroup algebra sum(S3). Its Morita dual necessarily has the
rank-five based ring R5_3_40, by the complete conditional derivation
`S3_FULL_CONDENSATION.md` and the four freshly replayed negative
rank-five alternatives. Moreover it cannot be tensor equivalent to the
known Izumi C3+6 inversion-equivariantization category: that category
has a nontrivial central invertible, whereas R439 has Inv Z(C)=1, as
proved in `KNOWN_MODEL_ROUTES.md`. Thus an R439 model, if one exists,
would require a different associator category on this positive based
ring. This is not a proof that such a category exists or is new.

For R567 the full-S3 subgroup algebra is impossible, so that particular
condensation route is closed. Its C3 algebra still exists and its
previously computed rank-eight same-based-ring Morita route remains
valid. The nontrivial C2 restriction has not been turned into a general
categorification obstruction.

Canonical replay: run all dependencies listed in
`pointed_s3_scope.json`, then `pointed_s3_scope.py`, in normal and
optimized Python. The final script is an exact source/hypothesis bridge;
the dependent joint-rotation replay checks all fourteen separating rays
and both exact surviving primal witnesses.
