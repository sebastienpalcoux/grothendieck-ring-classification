# Graded-family investigation: accepted results

The complete D40 family is resolved: three unitary models and six exclusions from arbitrary complex categorification.

| Result | Permanent source IDs |
|---|---|
| Unitary models | R12_1_156, R12_1_263, R12_1_449 |
| General complex exclusions | R12_1_309, R12_1_383, R12_1_467, R12_1_470, R12_1_501, R12_1_514 |

`results.json` contains the nine accepted decisions, exact input hashes, the positive full tensors/basis maps, and six precise exclusion certificates. `d40_classification.md` is the complete theoretical proof. Independent human verification remains pending.

The unified argument first shows that the integral part becomes pointed after Morita reduction by the actually existing algebra1+g. This follows from a new common-stabilizer/internal-end criterion, with no assumption that the original D10-type subcategory has its classical associator. The full precursor is then a feudal category with20 invertibles and four sqrt5 objects. An elementary double-coset commutativity lemma rules out the dihedral group alternative; the group of invertibles must be F20. The Brauer-Picard group of Vec(C5), together with coprime averaging and ENO's graded-extension classification, forces universal grading D8 and reduces every categorical possibility to an associator twist of one explicit unitary precursor. All relevant complex3-cocycles are covered by the sixteen relative mu4 cohomology representatives. All sixteen inverse Morita constructions yield R156 or R263, so the remaining six inputs are impossible.

The positive models are:

* R156: actual1+c bimodules in an explicit Liptrap feudal category with invertibles F20, four lords and C5 stabilizer; c is a noncentral involution.
* R263: the same construction after a normalized unitary D8-grading3-cocycle twist trivial on the subgroup<c>.
* R449: C4-equivariantization of TY(C5,chi), generator inversion, with fourth-power coherence kappa_m=-1 on the TY-odd object and kappa_a=1 on invertibles.

The converse proof concerns every original complex categorification, not only the supplied unitary models. No failed finite phase search is used as an exclusion.

## Replay and independent audits

Run `python verify.py` or `python -O verify.py`. The accepted replay needs the unchanged first-round folder beside the round-two folder. It checks exact source dimension characters and structural premises, the six independent integral-part models, a complete Liptrap phase/Fourier replay, all relative cohomology representatives, every complete Morita tensor, and a separate exact Phi8 Fourier projection for the C4-equivariantization. Both modes pass in roughly nine seconds.

Separate implementations and mathematical reviews are retained outside this directory:

* `../family_quadratic/audit_graded_models.py`: independently reconstructed mixed F-blocks,480000 relevant scalar pentagons,64 unitary Fourier blocks, and all balanced-product Hom dimensions for the accepted positive alternatives.
* `../audit_exclusions/audit_d8_cohomology.py`: fresh matrices and a different unit-pivot/even-F2 algorithm; the relative cocycle kernel has order2^87, coboundaries order2^83, so the quotient has exactly16 classes; all provided representatives are pairwise inequivalent modulo mu4 boundaries.
* `../audit_exclusions/audit_d40_duals.py`: independent F reconstruction, C2 module construction, and normalized involution-trace projection; all sixteen dual tensors match R156 or R263.
* `../family_cubic/`: independent categorical converse review, independent binary-lifting cohomology coverage and complete16-twist replay.

The relative mu4 list covers all complex associator classes; it is not claimed to list16 distinct U(1)-cohomology classes. The coefficient extension can identify pairs.

## Other initially assigned families

The separate positive-construction audit independently identifies R12_1_541 (D24) with Rep(C3 rt C8), where a C8 generator inverts C3. My general central-boson C4-graded zest gives the same exact based ring. It is recorded by the model-audit agent, so the three D40 positives above should not double-count R541.

Work on the twenty D32 cases was subsequently assigned to the positive-audit agent. The parent and integral-family agent address the remaining D24 cases; their later models/exclusions supersede my exploratory attempts. In particular, no negative conclusion was drawn from the unsuccessful H4 trial phase construction in this directory.

The experimental discovery scripts and bounded attempts are kept for research provenance. Accepted classification uses only `results.json`, `d40_classification.md`, `verify.py`, the exact precursor certificates, relative cocycle data and the actual bimodule/quotient implementations. No repository or website was changed.
