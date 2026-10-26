"""Replay exhaustive quotient search with every valid tensor bound independently.

The categorical and search-completeness audit is documented separately.
No census completeness is used. Every affirmative isomorphism returned by
the utility is verified on all structure constants, before deduplication.
"""
from pathlib import Path
from itertools import product
import sys,json,importlib.util,time,hashlib
import numpy as np
from audit_liptrap import HERE,FIRST,need

def main():
    start=time.monotonic();folder=HERE/'d48_quotient_frozen';sys.path.insert(0,str(folder))
    spec=importlib.util.spec_from_file_location('quotient_reconstruction_frozen',folder/'quotient_reconstruct.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    original=json.loads((FIRST/'tensors.json').read_text())
    for rid,row in m.INPUTS['records'].items():need(row['tensor']==original[rid],'frozen input equals physical source tensor')
    expected=json.loads((folder/'quotient_reconstruction.json').read_text())
    raw_iso=m.common.based_iso;checked=0
    def exact_iso(A,B):
        nonlocal checked
        p=raw_iso(A,B)
        if p is not None:
            n=len(A);need(sorted(p)==list(range(n)),'isomorphism bijection')
            need(np.array_equal(np.asarray(A),np.asarray(B)[np.ix_(p,p,p)]),'all coefficients of every returned isomorphism')
            checked+=1
        return p
    m.common.based_iso=exact_iso
    valid=[]
    def bind(N):
        hits=[]
        for rid in ['R12_1_351','R12_1_513']:
            p=exact_iso(N.tolist(),original[rid])
            if p is not None:hits.append(rid)
        need(len(hits)==1,'every valid table belongs to exactly one proved categorical quotient type')
        valid.append(hits[0])
    m.independent_bind=bind
    rows=json.loads(json.dumps(m.source_branches()));need(len(rows)==len(expected['source_binding']),'all source central involutions')
    for a,b in zip(rows,expected['source_binding']):
        need(a['id']==b['id'] and a['sha256']==b['sha256'],'source receipt binding')
        need(len(a['branches'])==len(b['branches']),'no central involution omitted')
        for x,y in zip(a['branches'],b['branches']):
            need(all(x[k]==y[k] for k in x),'all branch orbit/invariant data')
    outputs=[]
    for cls in expected['reconstruction_classes']:
        c=cls['source'];before=len(valid);found,stats=m.reconstruct(c['tensor'],c['dimensions'])
        need(stats==cls['statistics'],'fresh exhaustive search accounting')
        need(len(found)==len(cls['reconstructions'])==1,'one quotient ring per invariant class')
        need(exact_iso(found[0]['tensor'],cls['reconstructions'][0]['tensor']) is not None,'fresh representative equality')
        outputs.append(dict(first_source=c['first_source'],statistics=stats,valid_tensors=len(valid)-before,known_type=valid[-1]))
    need(len(valid)==704,'all valid tables independently checked before deduplication')
    result=dict(status='PASS',source_rings=len(rows),central_involution_branches=sum(len(r['branches']) for r in rows),invariant_ring_classes=len(outputs),valid_tables_fully_bound=len(valid),returned_isomorphisms_fully_checked=checked,classes=outputs,scope='Exhaustive rank12 quotient reconstruction, without assuming census completeness; no rank9 grading premise inferred',seconds=time.monotonic()-start)
    (HERE/'quotient_reconstruction_independent.json').write_text(json.dumps(result,indent=2)+'\n');print({k:v for k,v in result.items() if k!='classes'})

if __name__=='__main__':main()
