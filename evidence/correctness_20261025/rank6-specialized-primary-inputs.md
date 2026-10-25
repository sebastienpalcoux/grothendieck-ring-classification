# Remaining rank6 specialized primary inputs: LPR, Haagerup, CLS

2026-10-25, rank7 auditor; coordinated with rank6 auditor. Repository pinned8014c749. No repository or online edits.

**Conclusion: no additional categorical-existence gap found.** The three Ising variants and the zested metaplectic model match the precise published unitary examples. The Haagerup category has a direct primary existence theorem. The H8 extension citation supplies explicit pentagon solutions and is additionally redundant for the census ring, because the independently audited sign-swap construction gives the same tensor.

## Exact source scope

Primary PDFs inspected and retained locally:

- Liu–Palcoux–Ren, arXiv:2010.10264v5, `LPR2010.pdf/.txt`: §§3.6,4.3,4.5,4.6; rendered p17 to inspect the three dense matrix tables and parameter conditions.
- Grossman–Snyder, arXiv:1102.2631v2, `GSHaagerup.pdf/.txt`: Theorem1.4, the H6 fusion-ring relations in the Haagerup-background section, Lemma3.14, Lemma3.23 and Corollary3.24.
- Choi–Lu–Sun, arXiv:2310.19867v2 (header verified), `CLS2310.pdf/.txt`: Eq(1.4), §7.1, Tables3–4, and the accompanying existence discussion. Direct source URLs are <https://arxiv.org/pdf/2010.10264v5>, <https://arxiv.org/pdf/1102.2631>, and <https://arxiv.org/pdf/2310.19867>.

| Census ID | Actual primary input | Hypotheses and exact match |
|---|---|---|
| R6_1_1 | LPR §4.3, first table, printedp17 | Cyclic invertibles C4, dual noninvertible pair. Explicit pentagon family has a unitary choice r=2^(-1/4). All216 source coefficients match. |
| R6_1_3 | LPR §4.3, second table, printedp17 | Cyclic invertibles C4, individually self-dual noninvertibles. Choose r1=2^(-1/4), r2=2^(-1/2), satisfying the stated unitary modulus conditions. All216 match. |
| R6_1_9 | LPR §4.3, third table, printedp17, unitary condition continuingp18 | Klein-four invertibles, dual noninvertible pair. The same positive r1,r2 choices satisfy the explicit unitary family. All216 match. |
| R6_1_10 | LPR §4.5 printedp18; Theorem4.7 and §4.6 printedp19 | The N=5 metaplectic ring with unit and z interchanged in the odd-odd products. §4.5 supplies explicit unitary solutions; §4.6 supplies the zesting interpretation using the actual braided SO(5)2 category and its C2 grading. All216 match. |
| R6_1_15 | LPR §3.6 printedp13; Grossman–Snyder Theorem1.4, Lemma3.23 and Corollary3.24 printedp24 | GS explicitly proves a unitary H3 with the same ring as H2. The ring is called H6 in their notation; its relations are alpha³=1, alpha xi=xi alpha², xi²=1+xi+alpha xi+alpha²xi. These are exactly the constructor relations. The LPR H6 table matches all216 coefficients. |
| R6_2_69 | CLS Eq(1.4), §7.1 and Tables3–4 printedpp43–45 | Four invertibles, N²=sum(g), ND=DN=2D, D²=sum(g)+2N. §7.1 provides eight exact pentagon-solution families, rather than just a hypothetical fusion algebra. The already audited Ising sign-swap construction independently realizes this same ring; all216 entries match with the last two labels interchanged. |

The LPR Ising modulus conditions are not free unsupported choices: the first family requires |r|^4=1/2; the next two require |r1|^4=|r2|²=1/2. The displayed nonzero positive real choices meet these. No claim is needed that every solution in the algebraic families is unitary or that all variations are inequivalent. The fourth dimension-eight ring, R6_1_20, is the ordinary Ising product and was already covered separately.

For H3, the categorical distinction between H2 and H3 does not change the fusion ring. GS Corollary3.24 explicitly gives unitarity; this check does not rely on a numerical center identification. The Q-system on 1+alpha+alpha² is established in their Lemma3.14 using the actual untwisted pointed subcategory, rather than inferring an algebra from its object dimension.

For CLS, the introduction's physical argument alone would not suffice for this audit. The independent content used is the explicit solution of the pentagon equations in §7.1 and Tables3–4. Moreover, R6_2_69 does not depend on accepting this input: the manuscript's sign-swap equivariantization theorem, reviewed in full by the rank6 auditor, constructs a unitary category from actual Ising input. Its tensor `sign_swap_equivariantization(0)` equals the CLS-formula tensor under `(0,1,2,3,5,4)`. This is a categorical alternative already in the project, not a newly assumed reconstruction. The existing nilpotency argument may also transfer any categorical existence to unitarizability; nilpotency itself is not used to infer existence.

## Fresh table-to-code/census check

`rank6-specialized-source-match.py` extracts the six-by-six binary matrices directly from the pinned LPR PDF's text blocks, groups the actual six-matrix tables, and checks every coefficient under explicit unital permutations against both current constructors and the census. The selected source tables are unique within the specified pages. It also independently checks the H8-rule tensor against the sign-swap construction and census.

Receipt: `rank6-specialized-source-match.json`, statusPASS, six IDs. PDF hashes and all maps are recorded. This is a fresh exact source-table comparison, beyond the root's generic constructor replays. The checks do not reread a project-supplied copy of the purported LPR matrices.

## Minor citation precision, no classification change

- `supplements/rank6/software/complete_models.py:114` labels H3 with “LPR Theorem1.1.” A precise reference is LPR §3.6 p13 plus GS Theorem1.4/Corollary3.24. The current catalog already cites GS for this ID.
- `supplements/rank6/papers/chapters/06.tex:921–923` cites LPR §4.3 and says the metaplectic examples are treated there too. The metaplectic unitary example is actually §4.5 and its zesting explanation §4.6. This is an editorial citation correction, not an absent construction.

Scope limit: I verified the primary existence statements, relevant hypotheses/parameters, displayed fusion tables, and full table-to-code identities. I did not independently rerun every pentagon equation in these external papers; that was expressly outside this final specialized-source assignment. Their exact published solutions remain explicit external categorical inputs.
