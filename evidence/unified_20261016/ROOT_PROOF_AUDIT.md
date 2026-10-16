# Independent review of the inverse-Morita exclusion and the 2D2 extension

This review separates categorical existence/nonexistence from the finite tensor
checks. Both arguments were read independently of their generating scripts.

## R7_3_1022

The new exclusion uses the previously published C3/A4/V4 reduction without
changing its inputs. The missing step is supplied by Schopieray's published
Theorem 1.1 (DOI 10.1112/jlms.12789): the near-group ring for V4 at level 8
has no complex categorification. This theorem is not restricted to unitary
categories.

The commutation-cocycle calculation is algebraic. For the regular V4 algebra,
the induced noninvertible object has a twisted group algebra of dimension
four as its endomorphism algebra. The nontrivial class makes this algebra
M2(C). Its single simple summand then satisfies the forbidden level-eight
near-group multiplication. This forces the commutation class to vanish.

The reversal of the earlier Morita equivalence was checked explicitly. The
internal end of the regular module has exactly the four pointed summands
whose underlying objects contain the unit, each with multiplicity one.
Thus the inverse algebra is supported on the unique V4 subgroup of A4;
pointed support is a conclusion, not a presumed choice of algebra. On the
three noninvertible double orbits, changing either regular-algebra cocycle
cannot change the projective stabilizer class: every automorphism of V4
fixes its two-element second cohomology group. The inverse dual therefore
has twelve noninvertibles of dimension t, whereas the earlier category has
three of dimension 2t. This is a contradiction between Morita inverse
categories. No uniqueness of an arbitrary Haagerup--Izumi categorification
is needed.

The exact source replay was run independently. It checks all 49 products,
the complete dimension vector, the orbit data, both cohomology classes and
all six automorphisms of V4. Its successful output confirms these finite
inputs; the argument above and cited theorem supply the categorical proof.

## R8_2_37

The source equations were checked against Grossman--Izumi--Snyder,
arXiv:2201.11901v1, Theorem 4.1 and equations (3.10), (3.18), and Grossman,
arXiv:1612.07185, Section 4.1. An actual factor automorphism beta is available.
It commutes with the involution used in the crossed product, so extends by
fixing its implementing unitary. The two relations involving beta-rho and
beta squared extend because both implementing intertwiners are odd for
that involution. These signs are essential.

In the crossed product, the new invertible a has a squared equal to the
nontrivial 2D2 invertible g, hence order four. The relation
ara^{-1}=gr gives ra=a^{-1}r. The eight stated sectors are distinct and
closed under multiplication and duality. Their associator and positive
structure are inherited from the concrete endomorphism category. An
unproved coherent order-two action is not used.

The independent replay matches every one of the 512 structure constants,
and checks duality and the faithful grading. This establishes a unitary
model for precisely R8_2_37. A separate general Morita exclusion for R8_2_170 is reviewed below.

## HI(C6) dual realization (R8_2_535)

The independent review checked the published Grossman--Izumi Example 4.5 and Theorem 3.9, and Izumi Proposition 7.4/Theorem 7.5, against the categorical inputs. In particular the center dimension inventory is a theorem; the still conjectural missing modular-data entries in Example 4.5 are not used. The module image has dimension five, so its three-dimensional kernel cannot hide a noncommutative matrix block. Hidden formal codegrees D and D' are excluded by the explicit Perron bound and Galois stability, not by an incorrect uniqueness assumption. Character orthogonality then forces the other three characters, and the reconstruction matches all 512 source coefficients. The independent normal replay passes. Verdict: a unitary categorification exists. No conclusion follows for the other census rings with the same dimensions.

## Three rank-seven Galois reductions

The signed sphericalization proof for R7_4_106, R7_4_2155 and R7_3_146 was reviewed and independently replayed. Its divisibility step uses the codegree 48u with u a quadratic unit; the rational codegrees alone only imply divisibility by 24. The exhaustive signed quotient calculation and scaled characteristic-polynomial test leave only the two Galois conjugates of the Frobenius--Perron global dimension. This is a reduction to pseudo-unitary existence up to Galois conjugation, not an exclusion or construction. The separate two-moment theorem reviewed below subsequently excludes all three.

## Algebraic 2D2 graph-pair obstruction

The root independently replayed the complete source graph identifications, the rotation-one ideal certificate, and the primitive-cube-root contradiction, and reviewed both portable verifiers. The latter works over the abstract field Q(sqrt(5),omega), not a real specialization. The five-equation identity is 1; thus neither primitive rotation can occur. The source graphs force both generated even parts to have rank four. The pivotal linking construction was reviewed against the Schaumann/GMPPS source audit; it uses module traces and dual bases without an ambient star. The rectangular-to-spherical coordinate change is explicit in the final proof. Complex gauge carries every solution to a self-adjoint base, and equality of every positive box dimension rules out additional higher-depth data. The known dual even rank six therefore contradicts the source rank four. Verdict: all four exclusions have general complex scope. This does not classify every category with the neutral rank-four based ring.

## Simple rank-eight spherical and Galois reduction

The root read the signed-lift proof and the independent audit, inspected the source-derived Boolean domains and exhaustive associativity traversal, and checked the theoretical dimension identities. The unique positive signed quotient gives an actual spherical section of the sphericalization. Nonzero simple dimensions exclude b=±1, and b²−7b+1 determines the Galois orbit. This reduction alone supplies no existence decision; the separate unitary constructions are reviewed below.

## Odd-involution Morita reduction: R170

The root independently reviewed the grading twist, all double-orbit stabilizers, the splitting of the two-dimensional free-bimodule endomorphism algebras and the unique noninvertible of dimension 4+2sqrt(5). The terminal alternatives are precisely C4+8 and V4+8. The archived cyclic proof is bound to its actual earlier archive, with all six branches replayed; no later archive identity is asserted. A fresh source and terminal replay passed.

## Twisted half-braiding: R314 and R432

The root independently reviewed the full coherent right-action transport, the projection of multiplication to the regular bimodule summand, and application of the monoidal quasi-inverse. The pointed support 1+g forces one exchange at r and two exchanges at r tensor r. Naturality for the split inclusion r into r tensor r contradicts the distinct direct-sum idempotents. The tensorator and associators preserve those idempotents by naturality. The proof needs no F squared identity, braiding, pivotality or unitarity assumption. Fresh complete source replays passed; two further categorical audits agree.

## Near-group centralizers: R820 and R869

The root inspected Evans--Gannon, arXiv:1208.1500, Proposition 6, Table 2, Proposition 7(b), and the finite verification explicitly stated immediately after Conjecture 2. Order five is included in the established finite result. The centralizer of the five nondegenerate pointed center objects has exactly the displayed eight simples. The root checked the restricted S-block formulas, its global dimension 45(7+3sqrt(5))/2, the exact rational field implementation, and replayed both the Verlinde construction and an independent integer fusion-formula construction. Both identify all 512 coefficients with the source tensors. Categorical existence is inherited from actual unitary near-group centers, not inferred from modular-data feasibility.

## C16 orbifold inversion and reflection dual: R2665

The root read the complete construction and both categorical audits. The corrected parent-center action is inversion. Uniqueness of the cyclic regular algebra makes the parent Morita square regular, and its faithful action on central labels identifies that square with the identity. Central-algebra base change retains its character and inner ambiguities. The monodromy identities T squared = Inn(r) and Inn(r squared) = Id remove those ambiguities; the trivial universal grading supplies action coherence. The pointed cyclic associator has order four, so the integral reflection dual has FS exponent divisible by sixteen. This excludes the V4 Tambara--Yamagami possibility and identifies its invertibles as C4. Free-induction identities then determine the full rank-seven tensor. A fresh root replay checks all 343 source coefficients, the rank-sixteen model and all eight induction identities. The construction proves only R2665; it does not assert the other dihedral cases exist.

## C4 near-group pointed centralizer: R666

The root independently read Grossman--Izumi arXiv:1906.07397v2, Section 3.2.3.1, and Bonderson--Rowell--Wang arXiv:1910.07061, Section 2.4. Their smallest hyperbolic example is explicitly the center of existing C4+4 near-group categories. The conjecture for larger groups is not used. The root reviewed the full cyclotomic-integer S-matrix implementation and replayed all 784 unitarity identities, 1792 restricted Verlinde and closure coefficients, 4096 associativity identities and the complete 512-entry source comparison. The centralizer is a unitary braided fusion category with Tannakian center of order two; no claim of modularity is made.

## Noncyclic inversion descent: R35

The root read the complete companion proof and independent categorical audit, and replayed the exact rank-seven/rank-sixteen models, subgroup data, indicators and eight induction identities. The right internal-end cocycle is explicitly trivial: right whiskering leaves U(g) unchanged, so composition is U(h)U(g)=U(g+h). Thus no false H-squared vanishing assumption is made. The diagonal cyclic subgroup of the established Yu--Zhang C4-squared near-group category has trivial quadratic refinement; an actual order-four complement makes the orbifold's pointed C4 associator trivial. The same monodromy descent supplies a coherent inversion action. The integral reflection dual has FS exponent dividing four, while Shimizu's fourth indicator for TY(C4) is 1 plus or minus i. Its invertibles therefore form V4. The root's fresh replay identifies all 343 coefficients with R35.

## Simple-center induction lattice: R601

The root read the categorical proof and every line of the portable exact verifier, checked LPR Section 5 against the primary source, and ran a fresh complete replay. Integrality supplies positive spherical dimensions; nonbraiding follows from modular divisibility or the negative group class-sum coefficient, not an unjustified extension of the unitary Schur criterion. The simple integral center permits only non-prime-power divisors of 360. The complete character table fixes all seven induced-unit dimensions. Exact nonnegative PSD pruning enumerates 336 blocks; an exhaustive integer box covers every remaining restriction row, and exact rank-one PSD filtering is necessary. Each branch has a verified mod-2 or mod-3 functional annihilating every admissible outer product but not its residual Gram matrix. All repetitions remain covered. The independent fresh replay passes all 336 certificates.

## Forced quantum-group inverse Morita dual: R342

The root read the proof and complete standard-library reconstruction, checked the general monoidal scope of Feng--Ming--Rowell Theorem 5.1 and the type-A gauge kernel in Edie-Michell, and replayed the source-bound finite certificate. All signed module representations and bounded right-action matrices are enumerated. Joint linking identities leave one set; ten forced product matrices span the full fourteen-dimensional algebra and determine every hidden coefficient. The forced rank-seven neutral tensor is PSU(3)_5, with regular restricted module and nontrivial duality conjugation. Its quantum type-A classification, trivial gauge kernel and trivial universal grading fix the action up to Galois conjugation. The actual internal-end algebra 1+u supplies the required coherent crossed product and identifies the original category as its equivariantization. The existing centralizer model has this action and self-dual fusion ring R666, contradicting R342's non-self-dual pair. No braiding or pivotality assumption is imposed on the original category.

## Pivotal parity and inverse Morita: R49

The root read the full categorical proof and exact source verifier, reviewed the independent pivotal/associator audit, and ran a fresh complete replay. The published two-dimension theorem supplies a Galois pseudo-unitary categorification before any pivotal structure is used. Duality reverses the identical factors of a tensor power; the resulting self-dual form has indicator sign equal to the power of the simple indicator, without a braiding. Its odd-dimensional self-dual isotypic forms force the same sign. The unit and all four pointed simples occur once in the cube of source simple 6, forcing positive indicators. Thus the moved involution has trivial pointed associator and an actual regular algebra. The two pointed double orbits and single free noninvertible double orbit give the already excluded order-four, level-eight near-group alternatives. The cyclic terminal certificate is independently replayed. This proves general nonexistence for R49; the even-multiplicity ring R412 is not decided by the argument.

## Unified Fibonacci sphericality: R190 and R489

The root read the theoretical proof and exact source verifier and replayed both full tensor presentations, the odd cube identities and the nonintegral-ratio arithmetic. Chosen sphericalization lifts make the invertible positive, normalize the Fibonacci square, and force all simple-product commutation signs by nonzero dimensions. Duality removes the unequal coefficients for R190; formal-codegree divisibility and the irreducible nonmonic degree-four ratio polynomial remove them for R489. The normalized positive signed tensor gives an actual spherical section. Its four dimension characters form the Frobenius–Perron Galois orbit. Odd cube multiplicities give R489's actual regular involution algebra. These are necessary reductions; the separate character-parity theorem reviewed below supplies the categorification decisions. Neither a central lift nor a Fibonacci tensor factor is presumed.

## Sharpened R9 Morita frontier

The root read the final source-bound reduction and its two independent audits and ran the portable enumeration. Odd cubes force the involution's actual regular algebra. Its four-orbit module action is the regular 2D2 based module; the complete order-four quadratic enumeration uses coefficient sum four without imposing the original census bound. The total second indicator is Morita invariant by the center formula. This leaves precisely the self-R9 class-two branch or the specified anomalous R477 branch. The canonical known 2D2 dual action returns the standard Haagerup–Izumi category and has the wrong total indicator, so it is correctly rejected as a proposed model. This was an intermediate necessary reduction; the general R9 exclusion below subsequently closes its remaining alternative.

## Fibonacci character parity: R190 and R489

The root read the complete theoretical proof and portable arithmetic verifier, checked the canonical character labelling in Ostrik's Example 2.9 and the definition preceding Theorem 2.13, and replayed the full source-bound certificate. The two equal-codegree characters have forced restrictions in the same two-element set. A third actual character takes equal values on that set, so symmetry of the center matrix forces equal values of the paired characters on its restriction. Independence of 1 and the Fibonacci dimension then forces equal multiplicities in each invertible pair, contradicting the odd total three in the final pair. Equal formal codegrees are not used as a substitute for actual character labels. The preceding theoretical spherical/Galois reduction gives general complex scope. Two independent categorical and arithmetic audits agree.

## Staged twisted-V4 Morita exclusion: R2591

The root read the complete proof and every line of the source/group verifier and ran a fresh replay. Twisting the inverse regular algebra does not change character restriction to the order-two stabilizer, which forces preservation of the inverse V4 subgroup. The irrational dual pair forces its duality shift outside that subgroup, excluding the dihedral pointed group by the square obstruction in Aut(V4). A fixed involution in the remaining abelian group supplies an actual subalgebra. Its bimodule category retains the free rank-sixteen type, and the original inverse algebra becomes a connected separable algebra of dimension two. The resulting reflection Morita context necessarily has opposite dihedral reflection classes; the central rotation exchanges the two irrational support orbits, contradicting individual fixedness by every source invertible. The replay checks all initial tensor hypotheses, all group automorphisms and all sixteen final reflection configurations. The relative-algebra step is categorical, not inferred from a numerical model. No pivotality hypothesis is used.

## Common quadratic two-moment exclusion: R106, R2155 and R146

The root read the complete proof, conductor and residue refinements, finite two-moment hull, categorical audit and every line of the portable verifier. The separating matrix spectra justify a Galois automorphism flipping the dimension field while fixing all other characters; rational codegrees alone would not suffice. Character-level Galois transport pairs complete forgetful rows. The already saturated twist-one block forces conductor-level twists on rows with nonrational dimension ratio, and the Gauss-sum refinement fixes the primitive quadratic-residue sign. The unrestricted two-moment hull covers roots of every order, so no finite root-order cutoff is assumed. Pivotal adjoint-word forms determine all possible second-indicator signs. Exact source reconstruction yields 194, 194 and 1323 low blocks; modular span excludes 21, 21 and 235, and four fixed integer covectors exclude all remaining 346, 173 and 2176 signed trace systems. The root's fresh full replay passes. The 1072 distinct R146 targets are only a deduplicated representation of all 1088 branches; the portable replay checks every branch. This gives general complex exclusions through the separately audited signed sphericalization/Galois theorem, and completes rank seven through multiplicity three.

## A theoretical conductor-seventeen indicator balance: five rank-eight cases

The root independently read the entire proof and source verifier, reopened Ostrik's Remark 2.11 and Theorem 2.13 to check the noncommutative normalization, and ran a fresh source replay. The Casimir eigenvalue is dim(E) times the ordinary formal codegree; the corresponding central dimension is D/f_E. Thus the two simple quadratic eigenvalues and the remaining rational codegrees suffice in both commutative and noncommutative cases. The known twist-one block saturates the conductor-seventeen compression bound. Every nonrational high dimension ratio consequently has primitive seventeenth-root twist, whose first and second relative traces agree because two is a square modulo seventeen. Positive induction from an order-n invertible forces its twists to have order dividing n squared, so high rows containing invertibles instead have rational dimension ratio and nonpointed multiplicity four times their pointed multiplicity. Summing the trace difference gives the single exact indicator balance. Its right side has absolute value at least four, while each source has at most two self-dual noninvertibles. This excludes R33, R36, R76, R412 and R446 without any candidate enumeration, optimization, or unitarizability assumption. The two-dimension Galois theorem supplies general complex scope; two independent audits and normal/optimized replays agree.

## General spherical and Galois scope for R630 and R671

The root read the complete argument, every line of the exact verifier, and the independent audit, and ran a fresh source-bound replay. Choosing positive second-indicator lifts in the actual sphericalization gives a fully symmetric signed quotient. The odd-channel constraint fixes repeated triples modulo four. Complete associativity enumeration leaves only the original positive tensor: 27 Boolean variables for R630 and 27 Boolean variables plus one ternary all-distinct channel for R671. The full eight-character table is checked on every product. Every dimension character outside the FP pair vanishes on a simple, so a spherical dimension character lies in the FP Galois orbit. This proves the general-complex scope bridge used by the following exclusions, without identifying either category with a known HI(C6) example.

## A unified saturated Galois indicator lemma and R630

The root independently derived and read the weighted trace lemma, reviewed the complete R630 proof and verifier, and ran a fresh replay. A rational functional on the quadratic dimension field annihilating the global dimension kills exactly the central dimensions with rational ratio to that global dimension. Conductor saturation bounds all other twists. A cyclotomic automorphism with a field-preserving residue therefore transforms the first weighted trace into the corresponding higher trace. The Chinese remainder construction works even if that power is not coprime to the larger center exponent. The resulting exact indicator balance unifies the five conductor-seventeen exclusions with R630. In the latter, source cubic invariant dimensions leave precisely three one-dimensional rotation spaces with weights 1,1,4, contradicting the triangle inequality. No reality or positivity of third indicators is asserted. The structural sphericality bridge supplies general complex scope. Independent categorical and optimized arithmetic audits agree.

## Character-labelled two-moment exclusion for R2603

The root read the complete proof, the all-root quadratic moment-hull argument and every line of the portable verifier, and ran a fresh full replay. The complete source character table justifies a Galois automorphism fixing the non-FP character field while flipping sqrt(5). Character reciprocity forces exactly two induced-unit blocks. General Galois symmetry pairs complete restriction rows and preserves relative moments; it does not presume that the central permutation itself has order two. The algebraic-integer test uses the full ring of integers of Q(sqrt(5)), including half-integral coefficients. Every root order is covered by the proved seventeen-vertex hull. A single explicit integer covector is nonnegative on every candidate column and negative on both targets. The audited dihedral Morita reduction supplies Galois pseudo-unitary scope. The independent categorical audit and optimized replay agree, giving a general exclusion.

## Conductor-forty center trace exclusion for R671

The root read the full proof, exact nine-vertex unrestricted moment hull, source enumeration and certificate verifier, and ran a fresh full replay. All eight characters are checked directly and the immutable tensor hash is bound. Their field separation justifies full-row Galois transport. The saturated dimension block restricts nonrational rows to conductor-forty twists; the quadratic residue refinement determines the primitive sign. Positive second indicators constrain rows meeting the pointed involution. Exact character reciprocity and positive-semidefinite pruning enumerate six induced-unit frames. Exhaustive bounded row enumeration, algebraic-integrality tests and paired Gram subtraction cover every possible high row. Two fixed integer covectors have nonnegative values on all admissible columns and strictly negative values on the six targets. This yields a general-complex exclusion through the separately audited sphericality/Galois bridge. Independent proof and optimized arithmetic audits agree.

## R9 pointed-associator refinement

The root independently read the full scoped proof, every line of the standard-library verifier and the separate audit, and ran a fresh exact replay. Fourth induction traces force primitive eighth-root twists above the two order-four invertibles in pointed class two. Their first two relative moments vanish. Character-labelled reciprocity leaves exactly eight low frames; full-row Galois transport and the arbitrary-root moment hull cover every high row. A single integer covector is nonnegative on every exact column and has target value -6432 in all eight frames. All positive-semidefinite pruning uses exact rational arithmetic. The full quadratic ring of integers is used. Simultaneously incompatible pointed supports are harmlessly retained by the relaxation. This proves that R9 has trivial pointed associator and leaves only its specified anomalous R477 Morita alternative. This intermediate refinement alone made no classification decision; the subsequent general R9 argument below excludes the remaining class.

## General R9 exclusion by cyclic induction phase multiplicities

The root read the complete general proof and every line of its portable verifier, independently derived the cyclic Fourier lemma, and ran a fresh source-bound replay of all sixteen branches. For an order-n invertible, positivity forces exactly n possible induction-twist phases; the lower indicators vanish, so every phase has dimension mass D/n independently of the pointed associator. For the two order-four source invertibles in R9, comparing the nonnegative constant coefficients in each phase gives the new multiplicity bound v_a<=1. The already checked character-labelled rows, full Galois pairing and arbitrary-root moment hull now leave 405 columns per frame in class zero. One small integer covector has nonnegative values on all of them and target -64. The independent class-two covector has target -6432. Both apply to all eight exhaustive low frames. The two possible pointed classes are therefore excluded. A second independent full proof/code audit and optimized replay agree. This closes the formerly surviving R477 Morita alternative without presuming its associators, and establishes general complex nonexistence for R9 through the published two-dimension Galois theorem.

## Forced higher indicators at the rank-six R1660 frontier

The root read the full proof and complete standard-library verifier and ran a fresh source-bound replay. The known six-dimensional twist-one space has one copy of each saturated quadratic torus character. Exhaustion of the 532 certified local-character pairs leaves precisely two rank-one fixed-space irreducibles for each of the conductor-twelve and conductor-twenty-four sectors. Orthogonal projection of the central unit into the relevant summand is w/4; this justifies the conversion from a character average to the required modular matrix coefficient. The low-row Galois formula and exact dimension coordinates then convert those coefficients into ordinary indicators. Two mixed choices give impossible traces on the three-dimensional third-rotation space; the two conjugate choices force nu_3(T)=2 and nu_3(X)=nu_3(gX) in {2+omega,2+omega^2}. Fifth and seventh indicators satisfy their source bounds. All field arithmetic, character averages, compression eligibility and source invariant dimensions are regenerated exactly. The independent audit and optimized replay agree. This is a necessary-condition refinement, not a categorification decision; both rank-six entries remain unresolved.

## Full center STS closes R18 and the R2053 Morita endpoint

The root reviewer read the complete source-derived R18 verifier and each of its
three integer covectors, independently checked the full modular STS identity,
and executed a fresh optimized-Python replay. All eight character-labelled low
frames and all three pointed-associator classes pass: 24 separating inequalities
have minimum column pairing zero and target pairing -256. Classes 1 and 3 have
identical relative phase constraints. Every row bound and positive-semidefinite
check is rational and exhaustive; no floating-point elimination is a premise.

The reviewed categorical steps are: the two-FP-dimension Galois reduction;
Ostrik's actual character labels for all center rows; the normalized low-low STS
identity with its unweighted restriction Gram; full Galois and duality row
orbits; the cyclic Fourier multiplicity bound; maximal-order integrality of
D/dim(Z); the spherical Cauchy theorem restricting twist primes to 2 and 5;
and the rational relative trace of the fourth indicator. In particular,
nu_4(X) lies in Q(i), so its normalized trace to Q(sqrt(5)) is rational, and
ell(a+b*d)=2*a-b annihilates D times that trace. No assumption that higher
indicators of self-dual objects are real is used. The complete first, second
and fourth relative phase domain consists of the thirteen vectors from roots
of order dividing 40 and the all-zero vector. Equality of these relative
moments across a Galois row orbit follows from the squared Galois twist action
and the fact that every squared automorphism fixes Q(sqrt(5)).

The root also read the complete R2053-to-R18 structural proof and its independent
source verifier, and freshly replayed that verifier under Python -O. The actual
reflection-algebra Morita reduction, the rotational Frobenius--Schur exponent
contradiction, and the remaining full fusion subcategory identify R18 by all
512 tensor coefficients. Self-duality of the two inverse irrational simples
forces the a=1 branch because their stabilizers are trivial. The endpoint
exclusion therefore rules out R7_4_2053 over C without an initial pivotality
assumption. Together these decisions complete rank seven through multiplicity
four and rank eight at multiplicity one. They make no claim about the two
remaining rank-six cases or R8_2_24.

## R24: projective inner-square obstruction

The root accepts the revised minimal proof of R8_2_24 after reading its
integrated argument and independent audits of the signed, reindexed saturated
indicator lemma, canonical pivotal form defects, incoming-loop orientation,
paired right frames, restricted tetrahedral coefficients, annular unit corner,
three diagonal resolutions and projective normalizer. A fresh optimized replay
checks the immutable tensor, all sixteen dual slots, complete linear constraint
ranks, three polynomial contractions, and both nonzero scalar branches.

The argument retains arbitrary decorated cubic phases. Only two diagonal D
flips are used, in which each phase cancels as its own cube. The unit-channel
contribution is 1/d = sqrt(5)-2. No equality of the decorated phases, incoming
rotation-order claim, C*-structure, classification of arbitrary 2D2 associators,
or identification of pseudo-unitarity with unitarizability is used. The
character-weighted saturation lemma is justified by signed Galois reindexing,
including inversion of the twist exponent; it does not assume the Galois
permutation is involutive.

The source generator a has a^2=g and fixes all neutral labels by conjugation.
It therefore forces the actual tensor autoequivalence Ad(a), with square
Ad(g), contradicted by the local projective symmetry theorem. The two-FP-
dimension Galois reduction applies to the entire ambient category first, so the
conclusion excludes all complex categorifications. This closes rank eight
through multiplicity two. The two rank-six questions remain open.

## Rank-six witness refinement

The root read the complete exact Verlinde argument rejecting the single
historical rank-37 R6_8_1660 witness, its independent audit, and the portable
standard-library checker, and freshly replayed it under Python -O with PASS.
The phase-four fiber has two equal forgetful rows, with its symmetric line in
the visible twelve-dimensional irreducible and its antisymmetric line in a
one-dimensional hidden irreducible. Character averages give respective fusion
expectations 2 and -1; the mixed term is zero. Thus the diagonal coefficient
on either original simple label is 1/2. This is a genuine obstruction to this
fixed restriction/twist/representation witness, independent of numerical
S-matrix reconstruction. It does not cover every profile. The old witness
still solves all 1,536 equations of its stated weaker necessary system, and
neither rank-six general ledger decision changes.
