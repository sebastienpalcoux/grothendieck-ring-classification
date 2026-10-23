# Rank-ten multiplicity-one categorification

**136 general complex exclusions, 57 unitary models and one unresolved ring among 194 inputs.**
The continuation settles five formerly unresolved rings; no new model is claimed.

| Cases | Current result | Proof |
|---|---|---|
| R10_1_114, R10_1_115 | Excluded over the complex numbers | [Ordinary factors and the two swap descents](new/quadratic_models/ORDINARY_FACTOR_EXCLUSION.md) |
| R10_1_152, R10_1_153, R10_1_179 | Excluded over the complex numbers | [Relative factorization and the odd superfusion obstruction](new/rank16_dual/PSEUDO_BRANCH_EXCLUSION.md) |
| R10_1_189 | Unresolved | [Pointed associator theorem](new/case189/POINTED_ASSOCIATOR.md) · [Morita restriction](new/case189/MORITA_REDUCTION.md) |

> **AI-generated research · independent human verification pending.** Independent agent audits and exact automated checks have their stated scope and do not constitute independent human review or formal proof verification.

## Read and verify

The [current rank-nine/ten manuscript](../../publications/rank9-rank10/paper/rank9-rank10.pdf) presents the proofs in one account. [Accepted decisions](accepted_ledger.json) · [CSV](accepted_ledger.csv) · [Tensor-bound changes](classification_updates.json).

The [uniform Morita reduction](new/quadratic_obstructions/MORITA_REDUCTION.md), its [finite-completeness audit](new/quadratic_obstructions/REDUCTION_AUDIT.md), and the [relative-factorization lemma](new/rank16_dual/RELATIVE_FACTORIZATION.md) precede both exclusions. The pseudo branch imports the published finite superpentagon exclusion for the odd rank-two family (1,1); that calculation was not independently rerun here. Its precise scope and applicability were [audited](new/pseudo_psu_central_fermion_audit.md). The ordinary branch has a separate [descent audit](new/rank16_dual/ORDINARY_DESCENT_AUDIT.md).

For case 189, no braided categorification exists. The pointed subcategory is necessarily untwisted Vec(C5), and the regular-algebra Morita dual has the same fusion ring. These facts do not supply a model or a nonexistence proof.

Run the exact checks with Python, NumPy and SymPy:

```bash
python new/quadratic_obstructions/parity_morita_reduction.py
python new/quadratic_obstructions/module_action.py
python new/quadratic_obstructions/commutant_candidates.py
python new/quadratic_obstructions/dual_products.py
python new/quadratic_obstructions/complete_dual_tensor.py
python new/rank16_dual/verify_subcategories.py
python new/case189/verify_structure.py
python new/case189/verify_pointed_associator.py
python new/case189/verify_morita_reduction.py
python prior/rank9_rank10_m1_20261023/work/audit_new_models/verify_model21.py
```

The [research record](RESEARCH_RECORD.md) indexes the full exploratory material and earlier signed-sphericalization replays. [Verification summary](verification_summary.json). The earlier [rank-nine/ten package](../rank9_rank10_m1_20261023/README.md) and its frozen replay retain their original decisions. The accepted ledger here supersedes those decisions for exactly the six specified cases. The census tensors and enumeration qualifications are unchanged.
