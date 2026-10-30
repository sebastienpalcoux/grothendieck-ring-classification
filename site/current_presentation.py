"""Render the single current reader account after all publication stages.

This module changes presentation only. Accepted ledgers and proof archives
remain the responsibility of their publication modules.
"""
from pathlib import Path
import re,json,sys,html
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from frontier import FINDINGS,REMAINING

HERE = Path(__file__).resolve().parent
PROOFS = "https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/frontier/README.md"


def review_body():
    body = '''
    <nav class="review-nav" aria-label="Research navigation"><a href="./">← Ring atlas</a><a href="./unresolved.html">Open cases</a><a href="./#papers">Manuscripts</a><a href="./constructions.html">New constructions</a><a href="./theory.html">Theory &amp; definitions</a></nav>
    <p class="review-meta">Research status · 29 October 2026</p>
    <h1>Research status<br><em>&amp; verification</em></h1>
    <p class="lead">One current account of the classification, its remaining questions, and what the available checks establish.</p>
    <aside class="review-panel" aria-labelledby="caution-heading"><h2 id="caution-heading">AI-generated research · verification pending</h2><p>The proofs and computations have not yet received independent human verification or Lean formalization. Exact checks establish their stated computational scope; they do not replace the categorical arguments.</p></aside>
    <section class="review-panel" id="current-frontier"><h2>Current classification · 6 open questions</h2><p><strong>R8_3_1768 is excluded from complex fusion categorification.</strong> A pivotal conjugation-pairing lemma forces even multiplicities that contradict its complete necessary indicator system. The proof uses the established sphericalization/Galois existence reduction. Six exact separation certificates have been replayed.</p><p>The remaining cases are <strong>R6_4_155, R6_8_1660, R8_3_928, R8_3_941, R8_3_1154 and R9_2_137</strong>. Their strengthened restrictions supply neither another general exclusion nor a new model.</p><p><a href="./unresolved.html">Explore the six open cases →</a> · <a href="./papers/frontier.pdf">Current proofs and research report · PDF</a> · <a href="PROOFS">Proof notes and exact commands ↗</a> · <a href="./downloads/Fusion-Ring-Frontier-Proofs-and-Checks.zip" download>Proofs and checks · ZIP</a></p></section>
    <div class="review-panel" id="review-outcome"><h2>Classification counts and scope</h2><p>Rank eight through multiplicity three has <strong>4,404 general exclusions, 93 unitary models and 3 unresolved cases</strong>. Exact multiplicity three contributes 3,508 exclusions, 16 unitary models and 3 unresolved.</p><p>Rank nine through multiplicity two has 2,148 general exclusions, 76 unitary models and one unresolved case. Exact multiplicity two contributes 2,046 exclusions, 36 models and one unresolved.</p><p>The full census remains <strong>1,434,042 rings</strong>, within its published rank and multiplicity bounds. Changing a categorification decision does not add or remove a census ring.</p><p><a href="./records.html">Full census and individual records →</a> · <a href="./#classification">Classification by rank →</a></p></div>
    <h2>The six remaining questions</h2>
    <details class="review-details"><summary>Rank six · R6_4_155</summary><p>FINDING_R6_4_155</p><p><a href="./case.html?id=R6_4_155">Case record and proof →</a></p></details>
    <details class="review-details"><summary>Rank six · R6_8_1660</summary><p>FINDING_R6_8_1660</p><p><a href="./case.html?id=R6_8_1660">Case record and proof →</a></p></details>
    <section id="rank-eight-m3"><details class="review-details"><summary>Rank eight · three remaining cases</summary><p><a href="./case.html?id=R8_3_928"><strong>R8_3_928.</strong></a> FINDING_R8_3_928 <a href="https://anyonatlas.org/data/B20-02148" target="_blank" rel="noopener">B20-02148 in The Anyon Atlas ↗</a></p><p><a href="./case.html?id=R8_3_941"><strong>R8_3_941.</strong></a> FINDING_R8_3_941</p><p><a href="./case.html?id=R8_3_1154"><strong>R8_3_1154.</strong></a> FINDING_R8_3_1154</p><p><a href="./papers/rank8.pdf">Unified rank-eight manuscript →</a></p></details></section>
    <section id="rank-nine-m2"><details class="review-details"><summary>Rank nine · R9_2_137</summary><p>FINDING_R9_2_137</p><p><a href="./case.html?id=R9_2_137">Case record and proof →</a> · <a href="./papers/rank9-m2.pdf">Unified rank-nine multiplicity-two manuscript</a></p></details></section>
    <h2>Completed ranges</h2>
    <p>Ranks two through four have unrestricted classification claims. Higher ranks retain the explicit multiplicity bounds shown in the Atlas; completeness outside those bounds is not asserted.</p>
    <section id="rank-seven-m5"><details class="review-details"><summary>Rank seven · complete through multiplicity five</summary><p>The 10,006 supplied rings have 9,976 general exclusions and 30 unitary models. Tensor validity and uniqueness were checked independently. Enumeration completeness relies on the supplied producer completion record; the full enumeration was not repeated.</p><p><a href="./papers/rank7.pdf">Rank-seven manuscript →</a></p></details></section>
    <section id="rank-ten-m1"><details class="review-details"><summary>Rank ten · multiplicity one complete</summary><p>All 194 rings are decided: 136 general exclusions and 58 unitary models. R10_1_189 is identified in the classical SU(4)_6 conformal-embedding module category by matching all 1,000 tensor coefficients.</p><p><a href="./papers/rank9-rank10-m1.pdf">Ranks nine–ten manuscript →</a></p></details></section>
    <section id="rank-eleven-m1"><details class="review-details"><summary>Rank eleven · multiplicity one complete</summary><p>All 182 supplied rings are decided: 155 general exclusions and 27 unitary models.</p><p><a href="./papers/rank11.pdf">Rank-eleven manuscript →</a></p></details></section>
    <section id="rank-twelve"><details class="review-details"><summary>Rank twelve · multiplicity one complete</summary><p>All 632 supplied rings are decided: 480 general exclusions and 152 models. Exactly 151 models are known unitary. R12_1_623 has a complex and pseudo-unitary realization; its unitarity remains unproved.</p><p><a href="./papers/rank12.pdf">Rank-twelve manuscript →</a></p></details></section>
    <h2>What has been verified</h2>
    <p>The project distinguishes categorical hypotheses and cited theorems from tensor identities, finite-domain certificates, source hashes and publication checks. Passing scalar or matrix checks does not establish a missing categorical premise.</p>
    <p>The current R1768 exclusion has two separate agent proof reviews and a complete replay of the six required rational certificates. All 28 current finite checks passed, including nine exact certificates excluding the positive TY sign for R137 and the complete B20-02148 modular-data comparison. The negative-sign rational witness remains a necessary-system witness. The inherited general-complex gates and center-domain theorems remain explicit mathematical dependencies.</p>
    <details class="review-details"><summary>Proof repairs and reproducibility</summary><p>For R8_3_436, the earlier unitarity-dependent parameterization premise remains withdrawn; its current general exclusion uses an independent spherical-equivariantization and formal-codegree proof. The rank-eight manuscript also includes the R8_2_24 rigidity argument. Current manuscripts incorporate the accepted proof repairs.</p><p>Original evidence retains its source context. The published runner checks current tensors, source bindings and saved certificates without treating an obsolete research snapshot as a new classification decision.</p><p><a href="PROOFS">Current commands and dependencies ↗</a> · <a href="https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/docs/VERIFY.md">Complete verification guide ↗</a></p></details>
    <h3>Read and reproduce</h3><p><a href="./#papers">Current manuscripts</a> · <a href="./data/current_publication_revision.json" download>Publication checksums</a> · <a href="./downloads/current_remaining_cases.py" download>All 6 open fusion tensors</a> · <a href="./downloads/Fusion-Ring-Frontier-Proofs-and-Checks.zip" download>Current proof archive</a></p>
    <p>If you find an error, a <a href="https://github.com/sebastienpalcoux/grothendieck-ring-classification/issues">repository issue</a> naming the ring, theorem and failing step will support a precise mathematical review.</p>
    <hr><nav class="review-nav" aria-label="Continue reading"><a href="./#papers">Read the manuscripts →</a><a href="./records.html">Explore case records →</a><a href="./unresolved.html">Open questions →</a></nav>
    '''.replace("PROOFS", PROOFS)
    for rid in REMAINING:
        marker="FINDING_"+rid
        if body.count(marker)!=1:raise ValueError("Missing current case paragraph: "+rid)
        body=body.replace(marker,html.escape(FINDINGS[rid][0]))
    return body



def apply(site=HERE):
    site = Path(site)
    dist = site / "dist"
    path = dist / "review.html"
    html = path.read_text()
    html, n = re.subn(r'(<main id="review"[^>]*>).*?(</main>)',
                      lambda m: m[1] + review_body() + m[2], html, flags=re.S)
    if n != 1:
        raise ValueError("Expected one research-status main region")
    path.write_text(html)
    path = dist / "index.html"
    html = path.read_text()
    inventory=json.loads((dist/'downloads/current_manuscript_page_counts.json').read_text())
    totals=inventory['totals']
    page_summary=f"12 mathematical manuscripts: {totals['mathematical_manuscript']} pages; with the three verification guides: {totals['mathematical_manuscripts_and_guides']}; with the current research-status report: {totals['all_distinct_documents']}. Each distinct document is counted once. "
    html=re.sub(r'(<p class="scope-note" id="current-manuscript-page-summary">).*?(<a href=)',lambda m:m[1]+page_summary+m[2],html,flags=re.S)

    html = re.sub(r'<p class="scope-note" id="(?:frontier-update|correctness-update)">.*?</p>\s*', '', html, flags=re.S)
    notice = '<p class="scope-note" id="frontier-update"><strong>Current frontier: six unresolved rings.</strong> Three R928 center patterns and the positive TY branch for R137 are excluded. R928’s surviving positive spherical center must have rank 40: Sem⁻ ⊠ B, with B of rank 20 (or the conjugate orientation). Anyon Atlas B20-02148 supplies candidate data for B; full-data uniqueness is unproved. <a href="./review.html#rank-eight-m3">Center decomposition and remaining questions →</a></p>'
    anchor = '<p class="scope-note" id="fusion-census-status" hidden></p>'
    if anchor not in html:
        raise ValueError("Missing census-status presentation anchor")
    html = html.replace(anchor, anchor + '\n' + notice, 1)
    html = html.replace('EARLIER RESEARCH UPDATE', 'CURRENT CLASSIFICATION').replace('Earlier research details ↗', 'Current research scope ↗').replace('Earlier rank-six to rank-eight research', 'Current research scope')
    html = re.sub(r'<div class="paper-review-note"><p><strong>A concise introduction to the project\.</strong>.*?</div>', '<div class="paper-review-note"><p><strong>A concise introduction to the project.</strong> The Hexagon overview introduces the classification programme and constructions catalogue. The rank manuscripts and current research report give the latest results.</p><a href="https://hexagonmath.org/2610.00300" target="_blank" rel="noopener">Hexagon · 2610.00300 ↗</a> · <a href="./papers/announcement.pdf" target="_blank" rel="noopener">Research announcement · PDF ↗</a></div>', html, flags=re.S)
    html = html.replace('./downloads/theoretical-continuation-2026-10-24.zip', './downloads/Fusion-Ring-Frontier-Proofs-and-Checks.zip')
    html = re.sub(r'<details class="reading-panel"><summary>Earlier manuscript inventory</summary>.*?</details>', '', html, flags=re.S)
    html = re.sub(r'<p class="scope-note">Every <a href="\./records.html">individual case record</a>.*?</p>', '<p class="scope-note">Every <a href="./records.html">individual case record</a> includes a fusion tensor download. The <a href="./downloads/current_remaining_cases.py" download>six open fusion tensors · Python ↓</a> use their original source bases and checksums.</p>', html, flags=re.S)
    html = html.replace('All 7 open rings', 'All 6 open rings').replace('Current manuscript · 26 October 2026', 'Hexagon project overview')
    path.write_text(html)
    path = dist / "unresolved.html"
    html = path.read_text()
    html = re.sub(r'<noscript><p class="static-note">.*?</p></noscript>', '<noscript><p class="static-note">This directory uses JavaScript. Download <a href="./downloads/current_remaining_cases.py">all six open fusion tensors</a>, or read the <a href="' + PROOFS + '">current case summaries and proofs</a>.</p></noscript>', html, flags=re.S)
    path.write_text(html)


if __name__ == "__main__":
    apply()
    print("Current Atlas presentation consolidated: six open cases, one canonical proof route.")
