#!/usr/bin/env python3
"""Refresh current report text and the static status page from the M5 ledger."""
import json
import re
from pathlib import Path
from rank7_publication import extension, summary, remaining_ids, replay_status, PUBLICATION_DATE_LONG, STATUS_REPORT

ROOT=Path(__file__).resolve().parents[1]

def main():
    ext=extension(ROOT)
    if ext is None:raise ValueError('Integrate the rank-seven M5 ledger first')
    status=json.loads((ROOT/'data/classification_status.json').read_text())
    rank7=status['inputs']['rank7']['status_totals']
    path=ROOT/'docs/prepublication_review_content.json'
    content=json.loads(path.read_text())
    content['date']=PUBLICATION_DATE_LONG
    content['version']='Rank-seven multiplicity-five continuation and current verification scope'
    content['summary']=summary(ROOT)+' The two earlier rank-six categorification problems also remain open. The historical 38-case continuation has 36 decisions; its inventory is separate from this extension.'
    item=next(row for row in content['rank_counts'] if row['rank']==7)
    item.update(bound=5,rings=sum(rank7.values()),excluded=rank7['excluded'],models=rank7['unitarily_realized'],open=rank7.get('unresolved',0))
    content['coverage_notes']=[text for text in content['coverage_notes'] if not text.startswith('The rank-seven M5')]
    content['coverage_notes'].append('The rank-seven M5 tensor identities, fusion axioms and preservation of the earlier tensor set passed independent computational checks. Completeness of the exhaustive enumeration relies on the supplied producer completion record; the optimized enumerator was not independently rerun.')
    content['open_cases']=[item for item in content['open_cases'] if item['id'].startswith('R6_')]
    if ext['unresolved']:
        content['open_cases'].append({'id':f"Rank seven: {ext['unresolved']} ring{'s' if ext['unresolved']!=1 else ''}",'heading':'Exact multiplicity five',
            'paragraphs':[f"The supplied new band has {ext['rings']:,} records. Recorded general criteria exclude {ext['excluded']:,}; the ledger records {ext['realized']} unitary model{'s' if ext['realized']!=1 else ''}. The remaining {ext['unresolved']} {'record retains' if ext['unresolved']==1 else 'records retain'} unresolved status in the general complex scope; any obstruction requiring pivotality or another additional hypothesis is recorded separately.",
                          'The complete identifiers and exact tensors are in data/remaining_cases.py and supplements/rank7/output/m5/survivors.json. The rank-seven manuscript records the criterion allocation and residual analysis. Passing necessary conditions does not give coherent associators; unsuccessful model searches are not exclusions.']})
        if set(ext['remaining_ids']) == {'R7_5_3895', 'R7_5_5039'}:
            content['open_cases'][-1]['paragraphs'].append('The remaining tensors are R7_5_3895 and R7_5_5039. Each now has one surviving low induction frame. For R3895, a complete canonical-source integer certificate excludes the frame with distinct codegree-sixteen rows, leaving the repeated-row frame. For R5039, the conductor-eight ladder through order eight gives two sign-safe alternatives: active twist orders divide forty, or belong to {16,32,64,80,160,320}. Full-source phase multiplicities impose additional parity and divisibility conditions. Necessary-data witnesses are not coherent models, and neither whole ring has a general exclusion.')
            content['open_cases'][-1]['paragraphs'].append('Both remaining rings admit no braided categorification. R5039 lacks a formal codegree required by modularity. For R3895, an all-order Galois argument bounds twists by order forty; every exact balancing candidate then violates the second Frobenius–Schur indicator. These independently replayed obstructions require a braiding and leave both general problems open. Higher-word and Gram searches remain diagnostic until a complete general certificate is accepted.')
        elif len(ext['remaining_ids']) == 1 and ext['remaining_ids'][0] in {'R7_5_3895', 'R7_5_5039'}:
            content['open_cases'][-1]['paragraphs'].append('The remaining tensor is '+ext['remaining_ids'][0]+'. Its braided categorification is excluded, while general categorification remains open. The manuscript and proof inventory distinguish its necessary-condition reductions from accepted general exclusions.')
    content['open_case_count']=len(remaining_ids(ROOT))
    content['replay_sections']=[item for item in content['replay_sections'] if item['heading']!='Rank seven: multiplicity-five extension']
    content['replay_sections'].insert(0, {'heading':'Rank seven: multiplicity-five extension','paragraphs':[
        'The extension is kept separate from all frozen earlier proof stages. The preserved M4 ledger is restored for historical replay; current status partitions and reader downloads include the M5 records.',
        replay_status(ROOT),
        'Run supplements/rank7/software/verify_m5.py for the extension and consult its normal and optimized receipts under supplements/rank7/output/m5/. These checks certify the implemented input identities, criterion certificates and preserved historical decisions; they do not independently prove categorical coherence or exhaustive-enumeration completeness.']})
    content['theoretical_results']=[item for item in content.get('theoretical_results',[])
                                    if item['heading']!='Rank-seven multiplicity-five continuation']
    content['theoretical_results'].insert(0, {
        'heading':'Rank-seven multiplicity-five continuation',
        'paragraphs':[
            'The new continuation combines quadratic Casimir compression, complete signed sphericalization, Galois reduction to positive dimensions, and exact simultaneous first and second center-twist moments. A separate integral case is excluded by a complete cyclic-module Morita-dual calculation and descent to dimension 148. The current manuscript gives the categorical reductions and the finite domains checked by the programs.',
            'The center-trace certificates impose no arbitrary cutoff on root orders. The conductor-sixty extension pairs relative-trace values under modular Galois symmetry; it does not assume equality of individual paired twists. Structural reductions and unsuccessful model searches alone do not change a case to excluded.']})
    content['theoretical_results'][0]['paragraphs'].append('A general equality criterion applies at any prime p congruent to one modulo four: a twist-fixed quadratic-torus vector with saturated compression eigenvalue plus or minus 1/sqrt(p) generates a representation of level p, and its nontrivial twist support lies in the corresponding Legendre class of primitive pth roots. The manuscript proves this at every prime-power level and applies p=5 to the quadratic pair.')
    content['theoretical_results'][0]['paragraphs'].append('A second uniform criterion treats the odd conductor-eight character. Its partial projections give exact mass ratios for two-primary twist orders one, two, four and eight. Duality and Galois actions fixing the complete source field then yield two finite alternatives for active twist orders. Both criteria are proved at all congruence levels and supply necessary conditions for the complete finite-certificate arguments.')
    if any(item['id']=='R7_5_5039' for item in ext.get('continuation_decisions', [])):
        content['theoretical_results'][0]['paragraphs'].append('R7_5_5039 is now excluded in the general complex scope by coupled fourth and eighth rotations and an integral fusion-norm inequality. An all-order relative-phase inventory covers arbitrary twist orders. Two conductor-eight branches have exact modular contradictions; the complementary branches reduce exhaustively to 48 integer trees with 96 exact separating leaves. The eighth indicators force the finite packet domain, while the final separators use fourth-rotation and fusion-integrality constraints. This is a complete source-bound argument, distinct from rejecting an individual necessary-data witness.')
    path.write_text(json.dumps(content,indent=2,ensure_ascii=False)+'\n')
    path=ROOT/'site/dist/review.html';text=path.read_text()
    text=re.sub(r'Research status · \d+ October 2026','Research status · '+PUBLICATION_DATE_LONG,text)
    text=text.replace('prepublication-review-2026-10-19.pdf',STATUS_REPORT)
    text=text.replace('19 October research-status report','20 October research-status report')
    text=text.replace('its classification scope, two remaining questions and the limits', 'its classification scope, remaining questions and the limits')
    replacement=(f'<div class="review-panel" id="review-outcome"><h2>Current classification · {len(remaining_ids(ROOT))} open questions</h2>'
                 f'<p>{summary(ROOT)}</p><p>The two rank-six cases <code>R6_4_155</code> and <code>R6_8_1660</code> also remain open. '
                 'The historical 38-case continuation records 36 decisions; it does not include the new M5 band.</p>'
                 '<p>Rank eight is complete through multiplicity two, with 896 exclusions and 77 unitary models.</p></div>')
    text,n=re.subn(r'<div class="review-panel" id="review-outcome">.*?</div>',replacement,text,flags=re.S)
    if n!=1:raise ValueError('Unique current research panel required')
    if ext['unresolved']:
        outcome=f'{ext["unresolved"]} '+('ring remains' if ext['unresolved']==1 else 'rings remain')+' unresolved after the recorded criteria and model searches. '
        outcome+='<a href="./downloads/remaining_cases.py" download>Download every open fusion tensor</a>, or read the <a href="./papers/rank7.pdf">updated rank-seven manuscript</a>. A surviving necessary-condition system does not construct a fusion category.'
    else:
        outcome='Every supplied rank-seven ring through multiplicity five has a recorded general exclusion or unitary model. Read the <a href="./papers/rank7.pdf">complete rank-seven manuscript</a> and its exact verification data.'
    braided=''
    if ext['remaining_ids'] and set(ext['remaining_ids']) <= {'R7_5_3895','R7_5_5039'}:
        braided=('<p>The remaining ring admits no braided categorification. Its general categorification remains open.</p>' if ext['unresolved']==1 else '<p>The two remaining rings admit no braided categorification. Their categorification as general fusion categories remains open.</p>')
    block=('<section id="rank-seven-m5"><h3>Rank seven · multiplicity five</h3><p>'+outcome+'</p>'+braided+
           '<p>The 5,805 new tensors and agreement with the earlier 4,201 tensors passed independent computational checks. Exhaustive enumeration completeness relies on the producer completion record; the optimized enumeration was not independently rerun.</p></section>')
    text=re.sub(r'<section id="rank-seven-m5">.*?</section>\s*','',text,flags=re.S)
    text=text.replace('    <h2 id="rank-eight">', '    '+block+'\n    <h2 id="rank-eight">')
    path.write_text(text)
    index=ROOT/'site/dist/index.html'
    index.write_text(re.sub(r'>\d+ OCT 2026<','>20 OCT 2026<',index.read_text()))
    manuscript=ROOT/'manuscripts/rank7/papers/manuscript.tex'
    text=manuscript.read_text()
    text,n=re.subn(r'of exact multiplicity five: \$\d+\$ are excluded, one has the unitary\n'
                   r'model \$\\operatorname\{Rep\}\(C_7\\rtimes C_6\)\$, and (?:\$\d+\$ remains? open|all cases are resolved)\.',
        lambda _:f"of exact multiplicity five: ${ext['excluded']}$ are excluded, one has the unitary\n"
                 r'model $\operatorname{Rep}(C_7\rtimes C_6)$, and '
                 + (f"${ext['unresolved']}$ {'remains' if ext['unresolved']==1 else 'remain'} open." if ext['unresolved'] else 'all cases are resolved.'),text)
    if n!=1:raise ValueError('Unique M5 abstract status required')
    manuscript.write_text(text)
    print('Refreshed current research-report source and static research-status page.')

if __name__=='__main__':main()
