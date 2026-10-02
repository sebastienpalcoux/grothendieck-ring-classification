"""Exact necessary B3 central-character check, NOT a categorification proof.

Uses only integer arithmetic after reading the exact previously audited
self-braiding multiplicities. Tuba-Wenzl's irreducible central characters
in dimensions 1,2,3 and the necessary determinant relation in dimension 4
are tested on possible Jordan-Hoelder constituent eigenvalue multisets.
Passing does not assert that these constituents, associators, or categories exist.
"""
import hashlib
import itertools
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]/'supplements/rank6/research/frontier'
HERE=Path(__file__).resolve().parent
sources=[ROOT/'new_research/r155_modular/reconstruction.json',ROOT/'R6_4_155/forced_twists_certificate.json',ROOT/'new_research/r155_generalized/B_certificate.json']
rec,twists,indicators=[json.loads(p.read_text()) for p in sources]
N=rec['fusion_rules'];tt=twists['B_twist_exponents_mod24']
pm={(x['base'],x['target'][0]):list(map(int,x['multiplicities'])) for x in indicators['rows'] if x['target'][1]==1}

def partition(ev,central):
    if not ev:return []
    n=len(ev)
    for size in range(1,min(n,4)+1):
        for tail in itertools.combinations(range(1,n),size-1):
            ids=(0,)+tail
            summation=sum(ev[j] for j in ids)
            necessary={1:6*summation-central,2:3*summation+24-central,3:2*summation-central,4:3*summation-2*central}[size]
            if necessary%48:continue
            rest=partition([ev[j] for j in range(n) if j not in ids],central)
            if rest is not None:return [[ev[j] for j in ids]]+rest
    return None

rows=[]
for a in range(26):
    for b in range(26):
        exponents=[]
        for c in range(26):
            for sign in range(2):
                exponents.extend([(tt[c]-2*tt[a]+24*sign)%48]*(pm[a,c][sign]*N[c][a][b]))
        dimension=sum(N[a][a][c]*N[c][a][b] for c in range(26))
        if len(exponents)!=dimension:raise ValueError('Fusion / R multiplicity mismatch')
        if not 0<dimension<=4:continue
        central=(2*tt[b]-6*tt[a])%48
        parts=partition(exponents,central)
        rows.append({'a':a,'b':b,'dimension':dimension,'R_exps_mod48':exponents,'central_exp_mod48':central,'necessary_partition':parts,'passed':parts is not None})
receipt={'scope':'necessary central-character partition check only; no B3 representation or category constructed','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'blocks':len(rows),'passed':all(r['passed'] for r in rows),'rows':rows}
(HERE/'braid3_small.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:receipt[k] for k in ['scope','blocks','passed']}))
