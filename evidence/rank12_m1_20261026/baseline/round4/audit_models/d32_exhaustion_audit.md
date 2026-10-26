# Independent acceptance of the complete dimension-32 reduction

The argument in `../d32/morita_exhaustion.md` has been checked as a
categorical converse, separately from the successful constructions. It
applies to all 24 supplied rings of type 1^8,2^2,(sqrt(8))^2. The exact
adjoint series 32,16,4,1 implies nilpotence for any complex categorification,
so the use of unitary fusion-category structure in the reduction is licensed.

The following are the substantive points reviewed.

1. For the two dimension-two objects in the integral dimension-16 subcategory,
   the restricted Liptrap pairings satisfy B_Y(a,b)=B_X(Pa,b) and
   B_(X*)(a,b)=B_X(b,a), with P^2=1. The first identity follows by comparing
   biderivation at (g,a,b,X) and (gag^-1,g,b,X); the upsilon ratios really
   cancel because b stabilizes every noninvertible. These identities force
   a common P-fixed isotropic involution of the order-four stabilizer.
   The elementary C4 and V4 arguments cover nonsymmetric pairings as well.

2. The object 1+h is an actual separable algebra: fixedness of X trivializes
   the pointed associator on its subgroup. Isotropy trivializes the
   projective commutator for each fixed noninvertible, so the neutral Morita
   dual is pointed of dimension16. This is an algebra argument, not a
   claim that h has a half-braiding. The full dual is generalized TY, of
   type1^16 with either two sqrt(8) objects or eight sqrt(2) objects.
   The reverse connected algebra has dimension2 and is 1+c for an
   invertible involution. The integral tensor requires |C_G(c)|=8.

3. In the two-sqrt(8) case, the dual-paired branch forces an involutive
   cosquare on an abelian group of order8, hence the identity, contradicting
   that centralizer. In the self-dual branch, a generator c inside the
   stabilizer would require both B(c,c) and B(Pc,c) negative, which the
   complete elementary group/form analysis forbids. Thus the source is
   an actual TY category crossed by a coherent C2 action. Orthogonal
   automorphisms and the two parity square coherences exhaust these actions.
   The direct label-fixing tensorator calculation in the proof ensures that
   no unexamined gauge autoequivalence remains; GNN Proposition4.8 alone
   would only give existence, not this completeness conclusion.

4. In the eight-sqrt(2) case, if the image of c were central in the
   order-eight even grading group, multiplication of a dimension-two
   bimodule with an odd bimodule would have a single support orbit and
   coefficient2. This contradicts multiplicity one. Hence that even
   group is D8. The centralizer condition forces the central-extension
   presentation bit a=0, while c^2=1 forces its square bit zero. Both
   remaining conjugation bits b=0 and b=1 must be retained. Odd conjugation
   swaps reflection classes, giving precisely D16 and SD16 as universal
   grading groups. The non-split b=1 branch is essential and yields the
   two newly found positive models.

5. ENO's multiplication-system classification is used with
   Inv(Z(Vec_C2))=C2^2 and the odd electric/magnetic swap. This module is
   Ind_K^U(C2). The Shapiro isomorphism H^2(U,M)->H^2(K,C2) is restriction
   followed by evaluation in one coordinate. Categorically that coordinate
   is forgetting the half-braiding, so it records exactly the central
   extension of the group of invertibles. Thus the physical extension
   class fixes the entire H^2 datum, rather than just a quotient of it.
   The separate 450-variable finite-cochain check in
   `../d32/shapiro_check.json` confirms that all eight classes map
   bijectively to the three extension presentation bits. It supplements
   the categorical identification; it is not a substitute for it.

6. Actual references exist for all four choices (U,b). Consequently ENO
   Theorem1.3 makes all further choices genuine H^3(U,C*) twists of those
   references. The LHS bounds are32 for D16 and16 for SD16. The explicit
   rotation and reflection restrictions attain these bounds; the D16
   mixed cube is independently detected on the other reflection subgroup.
   The inverse subgroup's H^2(C2,C*) vanishes, so no algebra structures are
   omitted. Both lifts of its generator and all remaining admissible
   cocycle parameters are included.

The complete parameter list has been independently recomputed in
`audit_d32_catalog.py`: all96 generalized-Ising parameter choices have every
bimodule axiom, the simple-list completeness, and all1,728 fusion
multiplicities recomputed through monomial Hom equations. All46 TY
action/square choices are recomputed through independent equivariant
Hom fixed spaces. Every one of these142 categories matches one of

    R28,R183,R240,R405,R408,R419,R522,R530.

`audit_d32_nonisomorphism.py` independently checks all16 remaining tensors
against this list. Twelve are separated by elementary basis invariants;
the four remaining candidate pairs are separated by exact directed colored
product-graph isomorphism. This check does not reuse the discovery
backtracking isomorphism routine.

The accepted new general-complex exclusions are therefore

    R128,R144,R147,R173,R237,R275,R285,R294,
    R301,R318,R412,R415,R422,R431,R524,R536.

All identifiers in this note have prefix R12_1_. R419 and R530 are new
unitary models, independently audited from their actual Liptrap source
associators in `d32_nonsplit_independent.json`. No failed associator search,
unitary-only necessary criterion without a gate, or unsupported extension
completeness premise is used in these conclusions.

Primary theorem checks: ENO arXiv:0909.3140v2 Theorem1.3 and Corollary1.2;
Liptrap arXiv:1002.3166v2 Definition4.3/Theorem4/Lemma5.4;
GNN arXiv:0905.3117 Proposition4.8, together with the direct tensorator
kernel proof above. The nilpotent unitarity gate is GHR Theorem5.20.
