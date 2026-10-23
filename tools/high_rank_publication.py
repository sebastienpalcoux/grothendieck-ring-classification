"""Add current high-rank publications while retaining frozen lower-rank receipts."""
import json,re
from pathlib import Path
ATLAS='https://sebastienpalcoux.github.io/grothendieck-ring-classification/'

def active(repo):return (repo/'data/current_publication_revision.json').is_file()

def banner():
    return ('**Current high-rank results · 23 October 2026.** Rank 11 at multiplicity one is complete for the supplied census: '
            '**155 excluded, 27 unitary models, 0 unresolved among 182 rings**. '
            'Ranks 9–10 have 238 exclusions, 97 unitary models and 1 unresolved among 336 rings. '
            'The project has 7 open cases in total: 2 at rank 6, 4 at rank 8 and 1 at rank 10. '
            '[Rank-nine/ten manuscript](../publications/rank9-rank10/paper/rank9-rank10.pdf) · [Rank-11 manuscript](../publications/rank11/paper/rank11.pdf) · '
            '[Rank-ten proofs and replay](../evidence/rank10_m1_exclusions_20261023/README.md) · [Rank-11 proofs and replay](../evidence/rank11_m1_20261023/README.md) · '
            '[All current manuscripts](../manuscripts/README.md).')

def extend_document(text):
    start='<!-- current-high-rank-publication -->';end='<!-- /current-high-rank-publication -->'
    text=re.sub(re.escape(start)+r'.*?'+re.escape(end)+r'\n*','',text,flags=re.S)
    at=text.find('\n\n')
    return text[:at+2]+start+'\n\n'+banner()+'\n\n'+end+'\n\n'+text[at+2:]

def extend_front(front,repo):
    if not active(repo):return front
    front=re.sub(r'<!-- rank(?:9-rank10|11)-release -->.*?<!-- /rank(?:9-rank10|11)-release -->\n*','',front,flags=re.S)
    front=re.sub(r'^\| (?:9|10|11) \| Multiplicity 1 \|.*\n','',front,flags=re.M)
    rows='''| 9 | Multiplicity 1 | **Complete at multiplicity 1** | 102 excluded, 40 realized, 0 unresolved. |
| 10 | Multiplicity 1 | **Partial at multiplicity 1** | 136 excluded, 57 realized, [1 unresolved](https://sebastienpalcoux.github.io/grothendieck-ring-classification/unresolved.html?rank=10&m=1). |
| 11 | Multiplicity 1 | **Complete at multiplicity 1** | 155 excluded, 27 realized, 0 unresolved. |
'''
    front=re.sub(r'(^\| 8 \|[^\n]*\n)',lambda m:m[1]+rows,front,count=1,flags=re.M)
    front=re.sub(r'\*\*(?:Six|\d+) open cases(?:\.|:)[^\n]*','**7 open cases.** General categorification remains undecided for these rings.',front,count=1)
    matrix=re.search(r'\| Multiplicity \| Rank 2[^\n]*\n(?:\|[^\n]*\n)+',front)
    if matrix:
        lines=[]
        for n,line in enumerate(matrix[0].strip().splitlines()):
            cells=[v.strip() for v in line.strip('|').split('|')][:8]
            cells+=['Rank 9','Rank 10','Rank 11'] if n==0 else ['---:']*3 if n==1 else ['40','≥57','27'] if cells[0]=='1' else ['—']*3
            lines.append('| '+' | '.join(cells)+' |')
        front=front[:matrix.start()]+'\n'.join(lines)+'\n'+front[matrix.end():]
    front=front.replace('[Full count data](data/grothendieck_counts.csv)',
        '[Ranks 2–8 counts](data/grothendieck_counts.csv) · [Ranks 9–10 ledger](evidence/rank10_m1_exclusions_20261023/accepted_ledger.csv) · [Rank-11 ledger](evidence/rank11_m1_20261023/work/rank11/ledger.csv)')
    front=front.replace('[Decision ledger](data/classification_status.csv)',
        '[Current decision records](data/current_publication_revision.json)')
    front=front.replace('Candidates and open cases · PDF','Earlier construction-candidates report · PDF')
    return front

def manuscript_index(repo,historical):
    page=json.loads((repo/'data/current_manuscript_page_counts.json').read_text())
    manifest=json.loads((repo/'data/current_publication_revision.json').read_text())
    lines=['# Manuscripts','',
        '**Current classification through rank eleven: seven unresolved rings, including R10_1_189.**','',
        '> **AI-generated research · independent verification pending.** Exact automated checks establish only their stated computational scope.','',
        'Current manuscripts appear once, in increasing rank order. Realized counts refer to based rings with at least one model; they do not count inequivalent associators.','',
        '| Manuscript | PDF | Source | Pages |','|---|---|---|---:|']
    for d in page['documents']:
        if d['kind']!='mathematical_manuscript':continue
        import os
        p=os.path.relpath(repo/d['path'],repo/'manuscripts');tex=p.removesuffix('.pdf')+'.tex'
        lines.append(f"| {d['title']} | [PDF]({p}) | [TeX]({tex}) | {d['pages']} |")
    sums=page['totals'];count=page['document_counts']
    lines+=['',f"**{count['mathematical_manuscripts']} mathematical manuscripts, {sums['mathematical_manuscript']} pages.** With three verification guides: {sums['mathematical_manuscripts_and_guides']} pages. With the rank-two through rank-eight research-status report: {sums['all_distinct_documents']} pages. Each distinct document is counted once.",
        '', '[Page inventory and checksums](../data/current_manuscript_page_counts.json) · [Current publication manifest](../data/current_publication_revision.json)',
        '', '## Scope and verification','',
        '**Ranks 2–4:** unrestricted in multiplicity; the rank-four theorem has 15 realized rings and automatic sphericality. The finite-range rank-four census through multiplicity 128 is a separate companion.',
        '', '**Ranks 5–8:** explicit census bounds are 20, 9, 5 and 3. Two rank-six and four rank-eight categorification questions remain open.',
        '', '**Ranks 9–11:** multiplicity one only. Rank 9 has 102 exclusions and 40 unitary models; rank 10 has 136 exclusions, 57 unitary models and 1 unresolved; rank 11 has 155 exclusions and 27 unitary models.',
        '', '[Rank-11 proofs and replay](../evidence/rank11_m1_20261023/README.md) · [Ranks 9–10 proofs and replay](../evidence/rank10_m1_exclusions_20261023/README.md) · [All open cases]('+ATLAS+'unresolved.html)',
        '', '## Verification guides','', '| Guide | PDF | Pages |','|---|---|---:|']
    for d in page['documents']:
        if d['kind']!='verification_guide':continue
        lines.append(f"| {d['title']} | [PDF]({d['path'].removeprefix('manuscripts/')}) | {d['pages']} |")
    lines+=['','<details><summary>Earlier lower-rank reading notes and research history</summary>','',historical.strip(),'','</details>','']
    return '\n'.join(lines)

def extend_outputs(out,repo):
    if not active(repo):return out
    for name in ('docs/VERIFY.md','docs/RESEARCH_STATUS.md','docs/PROVENANCE.md','docs/PREPUBLICATION_REVIEW.md'):
        if name in out:out[name]=extend_document(out[name])
    out['manuscripts/README.md']=manuscript_index(repo,out['manuscripts/README.md'])
    return out
