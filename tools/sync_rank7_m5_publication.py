#!/usr/bin/env python3
"""Refresh current report text and the static status page from the M5 ledger."""
import json
import re
from pathlib import Path
from rank7_publication import extension, summary, remaining_ids

ROOT=Path(__file__).resolve().parents[1]

def main():
    ext=extension(ROOT)
    if ext is None:raise ValueError('Integrate the rank-seven M5 ledger first')
    status=json.loads((ROOT/'data/classification_status.json').read_text())
    rank7=status['inputs']['rank7']['status_totals']
    path=ROOT/'docs/prepublication_review_content.json'
    content=json.loads(path.read_text())
    content['date']='19 October 2026'
    content['version']='Rank-seven multiplicity-five extension and current verification scope'
    content['summary']=summary(ROOT)+' The two earlier rank-six categorification problems also remain open. The historical 38-case continuation has 36 decisions; its inventory is separate from this extension.'
    item=next(row for row in content['rank_counts'] if row['rank']==7)
    item.update(bound=5,rings=sum(rank7.values()),excluded=rank7['excluded'],models=rank7['unitarily_realized'],open=rank7['unresolved'])
    content['coverage_notes']=[text for text in content['coverage_notes'] if not text.startswith('The rank-seven M5')]
    content['coverage_notes'].append('The rank-seven M5 tensor identities, fusion axioms and preservation of the earlier tensor set passed independent computational checks. Completeness of the exhaustive enumeration relies on the supplied producer completion record; the optimized enumerator was not independently rerun.')
    content['open_cases']=[item for item in content['open_cases'] if item['id'].startswith('R6_')]
    if ext['unresolved']:
        content['open_cases'].append({'id':f"Rank seven: {ext['unresolved']} rings",'heading':'Exact multiplicity five',
            'paragraphs':[f"The supplied new band has {ext['rings']:,} records. Recorded general criteria exclude {ext['excluded']:,}; the ledger records {ext['realized']} unitary model{'s' if ext['realized']!=1 else ''}. The remaining {ext['unresolved']} records retain unresolved status in the general complex scope; any obstruction requiring pivotality or another additional hypothesis is recorded separately.",
                          'The complete identifiers and exact tensors are in data/remaining_cases.py and supplements/rank7/output/m5/survivors.json. The rank-seven manuscript records the criterion allocation and residual analysis. Passing necessary conditions does not give coherent associators; unsuccessful model searches are not exclusions.']})
    content['open_case_count']=len(remaining_ids(ROOT))
    content['replay_sections']=[item for item in content['replay_sections'] if item['heading']!='Rank seven: multiplicity-five extension']
    content['replay_sections'].insert(0, {'heading':'Rank seven: multiplicity-five extension','paragraphs':[
        'The extension is kept separate from all frozen earlier proof stages. The preserved M4 ledger is restored for historical replay; current status partitions and reader downloads include the M5 records.',
        'Run supplements/rank7/software/verify_m5.py for the extension and consult its normal and optimized receipts under supplements/rank7/output/m5/. These checks certify the implemented input identities, criterion certificates and preserved historical decisions; they do not independently prove categorical coherence or exhaustive-enumeration completeness.']})
    path.write_text(json.dumps(content,indent=2,ensure_ascii=False)+'\n')
    path=ROOT/'site/dist/review.html';text=path.read_text()
    text=re.sub(r'Research status · \d+ October 2026','Research status · 19 October 2026',text)
    text=text.replace('its classification scope, two remaining questions and the limits', 'its classification scope, remaining questions and the limits')
    replacement=(f'<div class="review-panel" id="review-outcome"><h2>Rank seven through multiplicity five · {len(remaining_ids(ROOT))} open questions</h2>'
                 f'<p>{summary(ROOT)}</p><p>The two rank-six cases <code>R6_4_155</code> and <code>R6_8_1660</code> also remain open. '
                 'The historical 38-case continuation records 36 decisions; it does not include the new M5 band.</p>'
                 '<p>Rank eight is complete through multiplicity two, with 896 exclusions and 77 unitary models.</p></div>')
    text,n=re.subn(r'<div class="review-panel" id="review-outcome">.*?</div>',replacement,text,flags=re.S)
    if n!=1:raise ValueError('Unique current research panel required')
    block=(f'<section id="rank-seven-m5"><h3>Rank seven · multiplicity five</h3><p>{ext["unresolved"]} rings remain unresolved after the recorded criteria and model searches. '
           '<a href="./downloads/remaining_cases.py" download>Download every open fusion tensor</a>, or read the '
           '<a href="./papers/rank7.pdf">updated rank-seven manuscript</a>. A surviving necessary-condition system does not construct a fusion category.</p>'
           '<p>The 5,805 new tensors and agreement with the earlier 4,201 tensors passed independent computational checks. Exhaustive enumeration completeness relies on the producer completion record; the optimized enumeration was not independently rerun.</p></section>')
    text=re.sub(r'<section id="rank-seven-m5">.*?</section>\s*','',text,flags=re.S)
    text=text.replace('    <h2 id="rank-eight">', '    '+block+'\n    <h2 id="rank-eight">')
    path.write_text(text)
    index=ROOT/'site/dist/index.html'
    index.write_text(index.read_text().replace('>17 OCT 2026<','>19 OCT 2026<'))
    print('Refreshed current research-report source and static research-status page.')

if __name__=='__main__':main()
