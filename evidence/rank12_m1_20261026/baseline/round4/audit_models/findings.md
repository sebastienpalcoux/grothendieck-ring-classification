# Fresh audit of the 148 retained rank-twelve models

This audit separates categorical existence, correctness of the reconstruction,
and identification with the supplied tensor. The baseline is the frozen
`Rank12_Multiplicity1_Theoretical_Continuation_2026-10-26` package. No online or
previous-round source was edited. The accepted model inventory is copied in
`ledger_models.json`.

No false realization has been found. The ordinary first-round replay checks all
381 stored model alternatives, rather than just one preferred name per ring.
Together with the 21 independently reconstructed Liptrap certificates these
account for 402 witnesses on 127 distinct rings. The additional 21 rings are
covered by the specialized audits below. The inherited rank-eight source review
also passes, including a new direct unitarization of the actual pseudo-PSU
associator tables used for the central-lift and flip constructions.

## First-round ordinary constructions

`replay_first_models.py` rebuilds every ordinary first-round witness, checks the
physical source hash, checks the unit-preserving basis permutation and all
1,728 coefficients, and explicitly checks which categorical half-braiding
licenses each selected zest current. Its fresh optimized-Python run passes in
`first_model_reaudit.json`. Constructor arithmetic is reused for the ordinary
families; the categorical premises were reviewed separately.

Pointed categories use actual finite groups. The SU(2), its even subcategories,
ordinary representation, and TY constructions use their standard unitary
realizations. Products use the stated positive lower-rank categories, with the
left tensor checked against its named standard construction. The lower-rank
multiplicity-one models through rank six are covered by Liu--Palcoux--Ren,
arXiv:2010.10264, whose positive statements are unitary existence statements.
They include the non-self-dual Ising and SO(5) zests; no categorical existence
is inferred from passing necessary tests.

For the half-even-metaplectic model the actual source is the closed subcategory
of SO(28)_2 with objects 1,h,g,hg,X_0,...,X_5,V_1,V_2. Gustafson--Rowell--Ruan,
arXiv:1808.00698v3, Section 3.3, gives the applicable N=0 mod4 formulas. The
constructor uses V_1^2=1+h+sum X_i and V_1 V_2=g+hg+sum X_i, as follows by
tensoring with g. The explanatory V_1 V_2 example in that paper has a typographic
`h` in place of `g`; the code uses the mathematically consistent formula.
All these simples are self-dual. The rank is twelve and dimension is 56.

The generalized Haagerup model R326 is justified by Grossman--Izumi,
arXiv:1501.07679v2, Section 2.4 and Example 4.5, which state existence of two
C6 categories and provide their structure constants in `solutions.nb`.
The conjectural/numerical qualification in Example 4.5 concerns the center
modular data, not existence of the fusion categories. The standard C6
generalized-Haagerup tensor is rebuilt and fully matched.

## Actual actions and actual central lifts

A group automorphism acts strictly on the untwisted pointed category. The TY
actions preserve the actual nondegenerate symmetric bicharacter and tau;
therefore they preserve all the skeletal associator coefficients, including
the Fourier block, with identity tensorator. The optional negative square
coherence is the monoidal TY parity character. It is invariant under the
action, so the group-action coherence holds. The odd equivariant structures
have eigenvalues plus or minus i when that coherence is negative. This phase
is included in the tensor formula. The family agent supplies the fresh
independent TY coefficient audit.

The additional model R449 uses the same strict inversion functor on TY(C5),
now as a coherent C4 action. Its carry cocycle has value the odd parity
character on crossing 4. `audit_c4_equivariant.py` checks the carry coherence,
constructs all orbit/stabilizer objects, and independently reconstructs all
Hom fixed spaces by monomial linear equations. It does not reuse the prior
Fourier trace implementation. All 1,728 coefficients pass.

For associative C2 zesting, the premise is an actual unitary central
invertible in the neutral component, not a basis element commuting in the
ring. Put lambda(1,1)=h and other normalized values equal to the unit. The
object cocycle identity compares h with itself; the remaining normalized
pentagon defect is scalar. It is removed by a unit-modulus square root,
equivalently H^4(C2,U(1))=0. Delaney--Galindo--Plavnik--Rowell--Zhang,
arXiv:2005.05544v2, Definition 3.2 and Proposition 3.4, then give a unitary
fusion category. This argument also handles a semionic lift; no blanket
boson/fermion assumption is needed.

All 138 first-round zest alternatives were checked for the categorical source
of their selected lift. Braided standard factors have their canonical lift.
An unbraided product factor is never silently assigned a braiding: the chosen
current is in the braided left factor unless the right factor is one of the
explicitly reviewed braided families. On an Ising graded pullback the current
is exactly (fermion,1), and its half-braiding restricts from the ambient
product. On the metaplectic character crossed product it is the canonical
Rep(C2) boson, whose half-braiding is preserved by the actual character action.

Matching C2 degrees in Ising times a genuine rank-eight category is a full
fusion subcategory. Closure, the complete label list, and every grading
channel are checked. The character action on TY(C5)^C2 multiplies its
equivariance map by minus one only on the TY-odd component; monoidality of
parity makes this a coherent tensor involution, so the crossed product exists.

The delicate rank-eight dependencies 6,7,11,14,25,42 were freshly checked.
`audit_psu_sources.py` reconstructs the free-boson quotient for R8_1_6 and
the ordinary PSU(2)6 flip extensions for R8_1_14 and R8_1_25, checking all
512 coefficients against the actual frozen inputs used by the rank-twelve
pullbacks. Edie-Michell, arXiv:1709.04721v2, Lemma 4.10 constructs the tensor
involution on Ad(A7). The fusion rules imply Aut_tensor(Id)=1, so its square
isomorphism is unique and coherent. Reutter's Theorems 1--2 supply a unitary
action. The fixed central lift of the nontrivial invertible is likewise
unique, and the central-twist obstruction vanishes in H^4(C2,U(1)).

For the pseudo-PSU inputs there is a stronger new source check.
`audit_pseudo_source.py` checks the actual two frozen associator tables,
rather than assuming they are equivalent to the published unitary examples.
For every associator matrix F and every nonzero coefficient it verifies

    (F^-1)_(f,e) / conjugate(F_(e,f))
      = w_(a,b,e) w_(e,c,d) / (w_(b,c,f) w_(a,f,d)).

All channel weights are explicitly positive: rational powers of 2 and
1+sqrt(2), with exponents recorded in `pseudo_source_reaudit.json`.
The corresponding positive diagonal gauge makes every one of the 136
associator blocks unitary. Both tables independently satisfy all 2,688
pentagons, the unit and rigidity conditions, and all 24 half-braiding
hexagons. The actual flip tensorator and coherent square are then replayed,
and the resulting full tensors are bound to R8_1_7, R8_1_11 and R8_1_42.
Thus no missing equivalence from a complex pentagon solution to a unitary
category remains in these positive dependencies. Exact frozen inputs and
their hashes are included under `pseudo_source`.

## Fresh Liptrap reconstruction and the two dimension-forty duals

`audit_liptrap.py` is a new transcription of Liptrap's Definition 4.3 and
Lemma 5.4, arXiv:1002.3166v2. It checks the complete serf group, lord action,
common stabilizer, all phase keys, quasisymmetry, biderivation, tau
normalization and nondegenerate symmetric bicharacters. It derives the gamma
formula independently and checks every nonscalar Fourier block by exact
cyclotomic row orthogonality. All scalar coefficients have modulus one and
the nonscalar blocks are unitary with the required stabilizer normalization.
Thus Theorem 4 reconstructs actual unitary categories; complex pentagon
solvability alone is not being called unitarity.

The fresh optimized run checks all 21 retained rank-twelve Liptrap witnesses,
including the variable-tau modulus-432 cases, and all five dimension-forty
feudal precursor witnesses. Its receipt is `liptrap_reaudit.json`.

For R156 and R263, `audit_d40_models.py` checks all seven scalar associator
cases used by the subgroup algebra, the actual regular C2 algebra, all module
axioms, pairwise Hom dimensions and the global-dimension exhaustion of the
simple list. For R263 it also checks the grading and the actual D8 cocycle.
It then reconstructs every balanced tensor product through monomial
intertwining equations, independently of the discovery character projection.
Both full tensors pass in `d40_model_reaudit.json`. Algebra existence and
separability are genuine categorical inputs, not conclusions from the tensor.

## Later-round models

The ordinary R541 model is Rep(C3 semidirect C8), with C8 acting by inversion.
`audit_rep541.py` constructs its eight linear and four induced characters,
checks complete orthogonality and the dimension sum 24, and computes all
1,728 tensor multiplicities by exact character inner products in Q(zeta24).
This is independent of the prior direct fusion-rule formula and passes.

The D48 family audit rechecks the actual groups/subgroups for R25,R30,R417.
It also checks all cocycle equations, exact subgroup restriction and balanced
bimodules for R428,R513,R597 (and R351 as a control). See the neighboring
`d48/earlier_model_audit.json`. Its separate round-three replay covers
R414,R531. These constructions use normalized unitary cocycles and actual
connected separable subgroup algebras.

R142,R361,R444 were independently audited in round three using complete
frozen monomial bimodules, full cocycle checks and all Hom coefficients;
the current root audit rechecks the same D120 categorical construction.
The complete frozen four-class independent replay, including R25 as a
control, also passes afresh under optimized Python in
`d120_replay/all_graph_twists_independent.json`.
R240 and R408 have fresh optimized replays in `d32/prior_model_reaudit.json`:
their sources are matched-grading subcategories of Ising times a twisted
pointed category on D16 or SD16. The actual 3-cocycle and its exact trivial
restriction to the chosen C2 algebra are checked. Each source is an actual
unitary category, and complete balanced-Hom reconstruction gives the target.

R79,R80 and R322,R323 are rechecked in `d144/positive_model_audit.json`.
The fresh audit inspected every relevant block of the source THF
arXiv:1503.06812v2 Equation 6.53, including its m=0 case. Categorical
existence comes independently from Cui--Galindo--Plavnik--Wang,
arXiv:1510.03475v3, Section 6.2 and Proposition 3, together with the gauging
H^3(S3) torsor. The two zests use the actual canonical central sign charge.
No completeness claim for all possible triality categorifications or
autoequivalence lifts is needed or made.

## Two additional round-four positive models

R419 and R530 have independently verified models. Their predecessors are
actual generalized-Ising categories with sixteen invertibles and eight
sqrt(2)-dimensional simples, with a non-split central extension in the
invertible group. The two respective grading groups are D16 and SD16.
`audit_d32_nonsplit.py` checks the complete Liptrap certificate independently:
34,816 defining equations and 512 exact unitary Fourier blocks per source.
It checks every grading channel and all 65,536 equations of each actual
unitary twisting cocycle. The seven scalar recouplings used by the
subgroup-bimodule operations are transcribed from Liptrap's Lemma 5.4.
The regular C2 algebra has exactly trivial restricted associator; module
axioms, simplicity, inequivalence, and dimension exhaustion are checked.
Every target coefficient is then computed independently using balanced
quotients and complete monomial Hom equations. R405 and R522 pass as
untwisted controls. The frozen inputs, checksums, and receipt are under
`d32_nonsplit_frozen` and `d32_nonsplit_independent.json`.

This proves two new existence statements only. A classification of all
possible generalized-Ising predecessors or of all graded associators is
not inferred from these examples.

## Scope

These checks establish the retained existence claims under their cited
categorical theorems. They are not a formal proof-assistant verification of
the entire literature. In particular no converse, exclusion, or completeness
claim is inferred from a successful model construction. Negative results
and any new round-four classification decisions are audited separately.

The subsequent complete audit is recorded in `additional_theory_audit.md`.
It adds the actual R320 construction and accepts the39 new D32/D48/D144
exclusions. Together with the separately root/D120-audited R332 exclusion,
the final global accounting is478 excluded,151 modeled, and3 unresolved.
The baseline148 models remain retained without withdrawals.
