"""Build a disjoint ledger; identifiers are never passed to obstruction functions."""
import json,collections,hashlib
from existence import positive_registry,all_values,status_from_existence,verify_ledger,unresolved_existence
from pathlib import Path
P=Path(__file__).resolve().parents[1]
def load(path):
    if path.suffix=='.jsonl':
        out=[]
        for l in open(path):
            try:out.append(json.loads(l))
            except json.JSONDecodeError as e:raise ValueError(f"malformed frozen certificate record in {path}") from e
        return out
    o=json.load(open(path));return o if isinstance(o,list) else [o]
def build():
    files=['classification.jsonl'];neg={};diagnostics={}
    canonical=P/'certificates/classification.jsonl'
    if not canonical.exists():raise ValueError('the canonical classification certificates are required; run software/classify.py first')
    from classify import STAGES
    summary_path=P/'verification/classification/summary.json'
    if not summary_path.exists():raise ValueError('classification campaign is incomplete; resume it before rebuilding the ledger')
    summary=json.loads(summary_path.read_text())
    if summary.get('stages')!=len(STAGES) or summary.get('missing_retained_exclusions'):
        raise ValueError('classification stages or previously certified exclusions are incomplete')
    if summary.get('census_sha256')!=hashlib.sha256((P/'data/census.json').read_bytes()).hexdigest():
        raise ValueError('classification summary does not match the current source import')
    if summary.get('certificates_sha256')!=hashlib.sha256(canonical.read_bytes()).hexdigest():
        raise ValueError('classification certificates changed since the completed campaign')
    diagnostics={rid:'The applicable recorded finite criteria did not produce a complete general exclusion; detailed eligibility and budget outcomes are in verification/classification/attempts.jsonl.' for rid in summary['unresolved_ids']}
    for fn in files:
        path=P/'certificates'/fn
        if not path.exists():continue
        for o in load(path):
            if 'certificate' in o and o.get('status') in (None,'excluded'):
                neg.setdefault(o['id'],o['certificate'])
            elif o.get('reason'):diagnostics[o['id']]=o['reason']
    pos=positive_registry()
    rows=json.load(open(P/'data/census.json'));m1=[r for r in rows if r['m']==1];remain=[r for r in m1 if r['id'] not in neg]
    if len(m1)!=39 or len(remain)!=21:raise ValueError('multiplicity-one classification count mismatch')
    if {r['id'] for r in remain}!={r['id'] for r in m1 if r['id'] in pos}:raise ValueError('explicit multiplicity-one models do not cover the positive complement')
    if set(neg)&set(pos):raise ValueError('positive/negative contradiction: '+str(set(neg)&set(pos)))
    ledger=[]
    for r in rows:
        o={k:r[k] for k in ['id','m','index','source_label','dual','commutative']}
        if r['id'] in neg:o.update(status='excluded',certificate=neg[r['id']],existence=all_values('no'))
        elif r['id'] in pos:o.update(status=status_from_existence(pos[r['id']]['existence']),**pos[r['id']])
        else:
            state=unresolved_existence(r['id'])
            if state['pseudo_unitary']=='no':
                detail='Pseudo-unitary and unitary nonexistence certified; general, pivotal and spherical existence remain unresolved.'
            else:
                detail='No complete general resolution. '+diagnostics.get(r['id'],'No complete certificate is recorded.')
            o.update(status='unresolved',diagnostic=detail,existence=state)
        ledger.append(o)
    verify_ledger(ledger)
    (P/'data/decisions.json').write_text(json.dumps(ledger,separators=(',',':'))+'\n')
    counts=[{'multiplicity':m,'classes':sum(r['m']==m for r in rows),**{k:sum(r['m']==m and r['status']==k for r in ledger) for k in ['excluded','unitarily_realized','spherically_realized_nonpseudounitary','unresolved']}} for m in range(1,max(r['m'] for r in rows)+1)]
    (P/'data/classification_counts.json').write_text(json.dumps(counts,indent=2)+'\n')
    print(json.dumps(counts,indent=2));return ledger
if __name__=='__main__':build()
